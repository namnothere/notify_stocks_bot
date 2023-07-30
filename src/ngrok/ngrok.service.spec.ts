import { Test, TestingModule } from '@nestjs/testing';
import { NgrokService } from './ngrok.service';

describe('NgrokService', () => {
  let service: NgrokService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [NgrokService],
    }).compile();

    service = module.get<NgrokService>(NgrokService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
