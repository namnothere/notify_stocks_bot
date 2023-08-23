import { IsString, IsOptional } from '@nestjs/class-validator';

export class notifyDto {
  @IsOptional()
  @IsString()
  chatId: string;

  @IsOptional()
  @IsString()
  message: string;

  @IsOptional()
  @IsString()
  error: string;

  @IsOptional()
  @IsString()
  ticker: string = null;

  @IsOptional()
  @IsString()
  exchange: string = null;

  @IsOptional()
  @IsString()
  interval = '1h';
}
