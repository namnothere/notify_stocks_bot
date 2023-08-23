import { notifyDto } from '../../tele/dtos';
import { TeleService } from '../../tele/providers';

export interface Queue {
  notiDto: notifyDto;
  teleService: TeleService;
  resolve: () => void;
}
