import { Injectable } from '@nestjs/common';
import { TeleService } from '../../tele/providers';
import { Queue } from '../../shared/interfaces';
import { notifyDto } from '../../tele/dtos';

@Injectable()
export class QueueService {
  private messageQueue: Queue[] = [];
  private isProcessing = false;
  private processingInterval = +process.env.MESSAGE_DELAY;

  async queue(notiDto: notifyDto, teleService: TeleService): Promise<void> {
    return new Promise<void>((resolve) => {
      this.messageQueue.push({ notiDto, teleService, resolve });
      if (!this.isProcessing) {
        this.isProcessing = true;
        this.processQueue();
      }
    });
  }

  async processQueue() {
    if (this.messageQueue.length > 0) {
      this.isProcessing = true;

      const { notiDto, teleService, resolve } = this.messageQueue.shift();
      await teleService.sendNotify(notiDto);
      resolve();

      await new Promise((resolve) =>
        setTimeout(resolve, this.processingInterval),
      );
      // Logger.log('Queue processed');

      this.processQueue();
    } else {
      this.isProcessing = false;
    }
  }
}
