import { Module } from '@nestjs/common';
import * as controllers from './controllers';
import * as providers from './providers';
import { TradingviewModule } from '../tradingview';

@Module({
  imports: [TradingviewModule],
  controllers: Object.values(controllers),
  providers: Object.values(providers),
})
export class TeleModule {}
