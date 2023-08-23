import { Module } from '@nestjs/common';
import * as controllers from './controllers';
import * as providers from './providers';
import { TradingviewModule } from '../tradingview';
import { QueueModule } from '../queue';

@Module({
  imports: [TradingviewModule, QueueModule],
  controllers: Object.values(controllers),
  providers: Object.values(providers),
})
export class TeleModule {}
