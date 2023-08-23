import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { TeleModule } from './tele/tele.module';
import { ConfigModule } from '@nestjs/config';
import { NgrokService } from './ngrok/ngrok.service';
import { TradingviewService } from './tradingview/tradingview.service';
import { TradingviewModule } from './tradingview/tradingview.module';
import { HttpModule } from '@nestjs/axios';
import { QueueService } from './queue/providers/queue.service';
@Module({
  imports: [
    TeleModule,
    ConfigModule.forRoot({ isGlobal: true }),
    TradingviewModule,
    HttpModule,
  ],
  controllers: [AppController],
  providers: [AppService, NgrokService, TradingviewService, QueueService],
})
export class AppModule {}
