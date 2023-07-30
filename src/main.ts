import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { NgrokService } from './ngrok/ngrok.service';
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const ngrokService = app.get(NgrokService);
  const ngrokUrl = await ngrokService.start();

  // await app.listen(3000);
  app.useGlobalPipes(new ValidationPipe({
    transform: true
  }));
  await app.listen(process.env.LOCAL_PORT);
  
  if (!ngrokUrl) {
    console.log('Ngrok setup failed. The NestJS application is still running without ngrok.');
  } else {
    console.log('Public URL:', ngrokUrl);
  }
}
bootstrap();
