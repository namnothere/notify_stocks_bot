import { Module } from '@nestjs/common';
import { QueueService } from './providers/queue.service';

@Module({
  providers: [QueueService],
  exports: [QueueService],
})
export class QueueModule {}
