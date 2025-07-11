import { Injectable, Logger } from '@nestjs/common';
import TelegramBot = require('node-telegram-bot-api');
import { notifyDto } from '../dtos';
import { TradingviewService } from 'src/tradingview/tradingview.service';
import * as fs from 'fs';
import { HttpsProxyAgent } from 'https-proxy-agent';
import { SocksProxyAgent } from 'socks-proxy-agent';

export enum TELEGRAM_PROXY {
  HTTP = 'HTTP',
  SOCKS5 = 'SOCKS5',
  FALSE = 'FALSE'
}

@Injectable()
export class TeleService {
  private bot: TelegramBot;
  private readonly botToken: string;

  constructor(private readonly tvService: TradingviewService) {
    this.botToken = process.env.TELEGRAM_API_TOKEN;
    // this.bot = new TelegramBot(this.botToken, { polling: true });

    if (process.env.TELEGRAM_PROXY === TELEGRAM_PROXY.SOCKS5 && process.env.PROXY_FILE_PATH) {
      const proxyFilePath = process.env.PROXY_FILE_PATH;
      let proxies: string[] = [];
      try {
        proxies = fs.readFileSync(proxyFilePath, 'utf-8')
          .split('\n')
          .map(line => line.trim())
          .filter(line => line.length > 0);
      } catch (err) {
        console.error('Failed to read proxy file:', err.message);
      }
      this.tryProxies(proxies).then(bot => {
        this.bot = bot;
        this.setupBot();
      }).catch(() => {
        console.error('No working proxy found. Bot will not start.');
      });
    } else if (process.env.TELEGRAM_PROXY == TELEGRAM_PROXY.HTTP && process.env.PROXY_FILE_PATH) {
      const proxyFilePath = process.env.PROXY_FILE_PATH;
      let proxies: string[] = [];
      try {
        proxies = fs.readFileSync(proxyFilePath, 'utf-8')
          .split('\n')
          .map(line => line.trim())
          .filter(line => line.length > 0);
      } catch (err) {
        console.error('Failed to read proxy file:', err.message);
      }
      this.tryHttpProxies(proxies).then(bot => {
        this.bot = bot;
        this.setupBot();
      }).catch(() => {
        console.error('No working HTTP proxy found. Bot will not start.');
      });
    } else {
      this.bot = new TelegramBot(this.botToken, {
        polling: true
      });
      this.setupBot();
    }
  }

  private async tryProxies(proxies: string[]): Promise<TelegramBot> {
    for (const proxy of proxies) {
      try {
        console.log("Trying SOCKS proxy:", proxy);
        const agent = new SocksProxyAgent(proxy);
        const bot = new TelegramBot(this.botToken, {
          polling: true,
          request: { agent } as any
        });
        // Test connection
        await bot.getMe();
        console.log(`Connected using proxy: ${proxy}`);
        return bot;
      } catch (err) {
        console.warn(`Proxy failed: ${proxy}`, err.message);
      }
    }
    throw new Error('All proxies failed');
  }

  private async tryHttpProxies(proxies: string[]): Promise<TelegramBot> {
    for (const proxy of proxies) {
      try {
        let proxyUrl = proxy;
        if (!/^https?:\/\//i.test(proxy)) {
          proxyUrl = 'http://' + proxy;
        }
        console.log("proxyUrl", proxyUrl);
        const agent = new HttpsProxyAgent(proxyUrl);
        console.log("agent", agent);
        const bot = new TelegramBot(this.botToken, {
          polling: true,
          request: { agent } as any
        });
        // Test connection
        await bot.getMe();
        console.log(`Connected using HTTP proxy: ${proxyUrl}`);
        return bot;
      } catch (err) {
        console.warn(`HTTP Proxy failed: ${proxy}`, err.message);
      }
    }
    throw new Error('All HTTP proxies failed');
  }

  private setupBot() {
    this.bot.on('polling_error', Logger.error);

    this.bot.onText(/\/ping/, (msg) => {
      this.ping(msg);
    });

    this.bot.onText(/test/, (msg) => {
      this.bot.sendChatAction(msg.chat.id, 'upload_photo');
      this.tvService.takeScreenshot('VNM', '1h').then(async (data: any) => {
        try {
          if (!data) throw new Error('Cannot take screenshot');
          if (data.error) throw new Error(data.error);
          if (data.data[0].screenshot_path) {
            data = data.data;
            const promises = data.map((item: any) => {
              const img = fs.readFileSync(item.screenshot_path);
              const fileOptions = {
                filename: String(item.screenshot_path).split('/').pop(),
                contentType: 'application/octet-stream',
              };
              return this.bot.sendPhoto(msg.chat.id, img, {}, fileOptions);
            });
            await Promise.all(promises);

            data.map((item: any) => {
              // check if path exists and remove it
              fs.unlinkSync(item.screenshot_path);
              Logger.log(`Removed ${item.screenshot_path}`);
            })

          } else {
            const imageURL = data.imageURL;
            this.bot.sendPhoto(msg.chat.id, imageURL);
          }
        } catch (e) {
          Logger.error('[sendChart] Error:', e);
          this.bot.sendMessage(msg.chat.id, `[sendChart] Error: ${e}`);
        }
      });
    });
  }

  async sendNotify(notiDto: notifyDto) {
    try {
      this.tvService
        .takeScreenshot(`${notiDto.ticker}`, notiDto.interval)
        .then(async (data: any) => {
          try {
            if (data.error) {
              return this.bot.sendMessage(
                process.env.PUBLISH_CHANNEL_ID,
                `[sendNotify] Error: ${data.error}\n${notiDto.message}`,
              );
            }

            if (
              data.data[0].screenshot_path != null &&
              data.data[0].screenshot_path != ''
            ) {
              data = data.data;

              const promises = data.map((item: any) => {
                const img = fs.readFileSync(item.screenshot_path);
                const fileOptions = {
                  filename: String(item.screenshot_path).split('/').pop(),
                  contentType: 'application/octet-stream',
                };
                return this.bot.sendPhoto(process.env.PUBLISH_CHANNEL_ID, img, {
                  caption: `[${notiDto.ticker}] ${notiDto.message}`,
                }, fileOptions);
              });
              await Promise.all(promises);

              data.map((item: any) => {
                // check if path exists and remove it
                fs.unlinkSync(item.screenshot_path);
                Logger.log(`Removed ${item.screenshot_path}`);
              })

            } else {
              const imageURL = data.imageURL;
              this.bot.sendPhoto(process.env.PUBLISH_CHANNEL_ID, imageURL, {
                caption: `[${notiDto.ticker}] ${notiDto.message}`,
              });
            }
          } catch (e) {
            Logger.error('[sendChart] Error:', e);
            return this.bot.sendMessage(
              process.env.PUBLISH_CHANNEL_ID,
              `[sendNotify] Error: ${e}`,
            );
          }
        });
    } catch (e) {
      Logger.error('[sendNotify] Error:', e);
      await this.bot.sendMessage(
        process.env.PUBLISH_CHANNEL_ID,
        `[sendNotify] Error: ${e}`,
      );
    }
  }

  async sendChart(notiDto: notifyDto, image: Buffer) {
    try {
      await this.bot.sendChatAction(
        process.env.PUBLISH_CHANNEL_ID,
        'upload_photo',
      );
      await this.bot.sendPhoto(process.env.PUBLISH_CHANNEL_ID, image, {
        caption: notiDto.message ? notiDto.message : undefined,
      });
    } catch (e) {
      Logger.error('[sendChart] Error:', e);
      await this.bot.sendMessage(
        process.env.PUBLISH_CHANNEL_ID,
        `[sendChart] Error: ${e}`,
      );
    }
  }

  async ping(msg: any) {
    const chatId = msg.chat.id;
    this.bot.sendMessage(chatId, 'Pong!');
  }

  async sendMessage(msg: string) {
    this.bot.sendMessage(process.env.PUBLISH_CHANNEL_ID, msg);
  }
}
