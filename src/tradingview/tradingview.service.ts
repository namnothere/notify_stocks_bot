import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { AxiosResponse } from 'axios';

@Injectable()
export class TradingviewService {
  constructor(private readonly httpService: HttpService) {}

  async takeScreenshot(ticker: string, interval: string) {
    try {
      const res: AxiosResponse<string> = await this.httpService.get(process.env.TRADINGVIEW_ENDPOINT, {
        params: {
          chart: process.env.CHART_ID,
          ticker: ticker,
          interval: interval,
        },
      }).toPromise();
      console.log(res.data);
      return res.data;
    } catch (e) {
      return {
        error: e,
      };
    }
  }

  // {
  //   "message": "BTCUSD, 1h Di chuyển Lên 0.01% trong 1 thanh",
  //   "ticker": "{{ticker}}",
  //   "exchange": "{{exchange}}"
  //   }

}
