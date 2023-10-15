import 'dotenv/config';

import { createEnv } from "@t3-oss/env-core";
import { z } from 'zod';

export const env = createEnv({
  server: {
    DISCORD_TOKEN: z.string(),
    OSU_CLIENT_ID: z.string(),
    OSU_CLIENT_SECRET: z.string(),
    TARGET_COUNTRY: z.string().default('MY'),
    TOP_AMOUNT: z.coerce.number().default(30),
    CHANNEL_IDS_OSU: z.string().default('')
      .transform(text => {
        text = text.trim();
        if (!text)
          return [];
        return text.split(',');
      }),
    CHANNEL_IDS_TAIKO: z.string().default('')
      .transform(text => {
        text = text.trim();
        if (!text)
          return [];
        return text.split(',');
      }),
    CHANNEL_IDS_CATCH: z.string().default('')
      .transform(text => {
        text = text.trim();
        if (!text)
          return [];
        return text.split(',');
      }),
    CHANNEL_IDS_MANIA: z.string().default('')
      .transform(text => {
        text = text.trim();
        if (!text)
          return [];
        return text.split(',');
      }),
  },
  client: {},
  runtimeEnv: process.env,
  clientPrefix: '',
});
