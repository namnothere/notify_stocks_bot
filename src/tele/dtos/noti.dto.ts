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
  ticker: string;
  
  @IsOptional()
  @IsString()
  exchange: string;

  @IsOptional()
  @IsString()
  interval: string = '1h';
}

