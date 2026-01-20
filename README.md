# Signal jam 
This _monorepo_ hosts the software suite of the _Signal Jam_ project. With this software you can monitor disinformation on social media around certain topics. It consists of two parts: a set of scripts that scrape social media and save the data to a database, and a dashboard that shows the data gathered. 

## Provider agnostic
The software suite is tailored for use with cloud providers for ease of use, but is built as _provider agnostic_ as possible. This means that you can decide on yourself what to use for each part of the application.

N.B. This application is in a very early development stage. So don't take the list below too seriously yet.

#### The database
- Supabase (recommended) 
- Neon
- Railway 
- Any local postgres instance

#### Script deployment
- Railway 
- Render
- Fly.io 
- With a cronjob on a local VPS (check possible additional setup requirements)

#### Dashboard deployment 
- Netlify (recommended)
- Vercel 
- Cloudflare pages 

#### Authentication
- Supabase Auth (recommended)
- Auth0 
- Clerk

## Architecture
```
┌─────────────┐      ┌──────────────┐      ┌───────────┐
│  Scraper    │─────▶│  PostgreSQL  │◀─────│ Dashboard │
│ (Railway)   │      │  (Supabase)  │      │ (Netlify) │
└─────────────┘      └──────────────┘      └───────────┘
                            ▲
                            │
                     ┌──────┴──────┐
                     │  Auth       │
                     │ (Supabase)  │
                     └─────────────┘
```

You can swap any component with your preferred provider. See the `README`'s in each respective folder for more info on each part of the application.

## Configuration

All configuration is done through environment variables. See `.env.example`.

## Database Schema

There is a fixed schema in `database/schema.sql`. All providers must use this schema. See the `README` in this folder for more information and instruction on how to set things up with your provider.
