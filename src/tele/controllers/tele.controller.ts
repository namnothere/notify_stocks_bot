import { Body, Controller, Inject, Post, UploadedFile, UseInterceptors } from '@nestjs/common';
import { notifyDto } from '../dtos';
import { TeleService } from '../providers';
import { FileInterceptor } from '@nestjs/platform-express';
@Controller('tele')
export class TeleController {

  constructor(
    @Inject(TeleService)
    private readonly teleService: TeleService
  ) {}

  @Post('alert')
  async notify(@Body() notiDto: notifyDto) {
    console.log("alert", JSON.stringify(notiDto));
    await this.teleService.sendNotify(notiDto);
  }

  @Post('chart')
  @UseInterceptors(FileInterceptor('image'))
  async chart(@UploadedFile() image: Buffer, @Body() notiDto: notifyDto) {
    console.log("chart", JSON.stringify(notiDto));
    if (image) console.log("Received image", image);
    await this.teleService.sendChart(notiDto, image);
  }
}