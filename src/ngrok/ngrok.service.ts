import { Injectable } from '@nestjs/common';
import * as ngrok from 'ngrok';

@Injectable()
export class NgrokService {
  async start() {
    const ngrokUrl = await ngrok.connect({
      addr: process.env.LOCAL_PORT || 3000,
      hostname: process.env.HOSTNAME || null,
    });
    
    return ngrokUrl;
  } catch (e: any) {
    console.error('Error starting ngrok:', e);
    return null;
  }
}
