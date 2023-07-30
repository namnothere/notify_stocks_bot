import { Test, TestingModule } from '@nestjs/testing';
import { TeleService } from './tele.service';

describe('TeleService', () => {
  let service: TeleService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [TeleService],
    }).compile();

    service = module.get<TeleService>(TeleService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
