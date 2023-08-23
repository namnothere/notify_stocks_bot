import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { NgrokService } from './ngrok/ngrok.service';
import { Logger, ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const context = 'MAIN';
  const app = await NestFactory.create(AppModule);

  const ngrokService = app.get(NgrokService);
  const ngrokUrl = await ngrokService.start();

  app.useGlobalPipes(
    new ValidationPipe({
      transform: true,
    }),
  );
  await app.listen(process.env.LOCAL_PORT).then(() => {
    Logger.log(
      `Application is running on: localhost:${process.env.LOCAL_PORT}`,
      context,
    );
  });

  if (!ngrokUrl) {
    Logger.log(
      'Ngrok setup failed. The NestJS application is still running without ngrok.',
      context,
    );
  } else {
    Logger.log(`Public URL: ${ngrokUrl}`, context);
  }
}
bootstrap();
