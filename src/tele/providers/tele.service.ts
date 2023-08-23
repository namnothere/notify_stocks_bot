import { Injectable, Logger } from '@nestjs/common';
import TelegramBot = require('node-telegram-bot-api');
import { notifyDto } from '../dtos';
import { TradingviewService } from 'src/tradingview/tradingview.service';

@Injectable()
export class TeleService {
  private bot: TelegramBot;
  private readonly botToken: string;

  constructor(private readonly tvService: TradingviewService) {
    this.botToken = process.env.TELEGRAM_API_TOKEN;
    this.bot = new TelegramBot(this.botToken, { polling: true });

    this.bot.on('polling_error', Logger.error);

    this.bot.onText(/\/ping/, (msg) => {
      this.ping(msg);
    });

    this.bot.onText(/test/, (msg) => {
      this.bot.sendChatAction(msg.chat.id, 'upload_photo');
      tvService.takeScreenshot('HOSE:VNM', '1h').then((data: any) => {
        try {
          if (!data) throw new Error('Cannot take screenshot');
          if (data.error) throw new Error(data.error);
          const imageURL = data.imageURL;
          this.bot.sendPhoto(msg.chat.id, imageURL);
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
        .then((data: any) => {
          try {
            if (data.error) {
              return this.bot.sendMessage(
                process.env.PUBLISH_CHANNEL_ID,
                `[sendNotify] Error: ${data.error}\n${notiDto.message}`,
              );
            }
            const imageURL = data.imageURL;
            this.bot.sendPhoto(process.env.PUBLISH_CHANNEL_ID, imageURL, {
              caption: `[${notiDto.ticker}] ${notiDto.message}`,
            });
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
