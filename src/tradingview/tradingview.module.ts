import { Module } from '@nestjs/common';
import { TradingviewService } from './tradingview.service';
import { HttpModule } from '@nestjs/axios';

@Module({
  imports: [HttpModule],
  providers: [TradingviewService],
  exports: [TradingviewService],
})
export class TradingviewModule {}
