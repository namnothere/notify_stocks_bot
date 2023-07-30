import { Test, TestingModule } from '@nestjs/testing';
import { TeleController } from './tele.controller';

describe('TeleController', () => {
  let controller: TeleController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [TeleController],
    }).compile();

    controller = module.get<TeleController>(TeleController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
