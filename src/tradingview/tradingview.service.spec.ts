import { Test, TestingModule } from '@nestjs/testing';
import { TradingviewService } from './tradingview.service';

describe('TradingviewService', () => {
  let service: TradingviewService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [TradingviewService],
    }).compile();

    service = module.get<TradingviewService>(TradingviewService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
