import * as rawbody from 'raw-body';
import {
  Body,
  Controller,
  Inject,
  Logger,
  Post,
  Req,
  UploadedFile,
  UseInterceptors,
} from '@nestjs/common';
import { notifyDto } from '../dtos';
import { TeleService } from '../providers';
import { FileInterceptor } from '@nestjs/platform-express';
import { QueueService } from '../../queue/providers';
@Controller('tele')
export class TeleController {
  constructor(
    @Inject(TeleService)
    private readonly teleService: TeleService,
    private readonly queueService: QueueService,
  ) {}

  @Post('alert')
  async notify(@Body() notiDto: any, @Req() req) {
    if (req.readable) {
      const raw = await rawbody(req);
      Logger.log(`New message: ${raw}`);
      const text = raw.toString().trim();
      const ticker = this.extractStock(text);
      notiDto = {
        ticker: ticker,
        message: text,
      } as notifyDto;
      await this.queueService.queue(notiDto, this.teleService);
    } else {
      await this.teleService.sendMessage(notiDto);
    }
  }

  @Post('chart')
  @UseInterceptors(FileInterceptor('image'))
  async chart(@UploadedFile() image: Buffer, @Body() notiDto: notifyDto) {
    Logger.log('chart', JSON.stringify(notiDto));
    if (image) Logger.log('Received image', image);
    await this.teleService.sendChart(notiDto, image);
  }

  extractStock(message: string) {
    if (message.includes('-')) {
      return message.split('-')[0];
    } else {
      return message.split(' ')[0];
    }
  }
}
