import { Injectable, Logger } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { AxiosResponse } from 'axios';

@Injectable()
export class TradingviewService {
  constructor(private readonly httpService: HttpService) {}

  async takeScreenshot(ticker: string, _interval: string) {
    try {
      const res: AxiosResponse<string> = await this.httpService
        .get(process.env.TRADINGVIEW_ENDPOINT, {
          params: {
            chart: process.env.CHART_ID,
            ticker: ticker,
          },
        })
        .toPromise();
      // Logger.log(res.data);
      return res.data;
    } catch (e) {
      Logger.error(e);
      return {
        error: e,
      };
    }
  }
}
