# Signal jam 
This _monorepo_ hosts the software suite of the _Signal Jam_ project. With this software you can monitor disinformation on social media around certain topics. It consists of two parts: a set of scripts that scrape social media and save the data to a database, and a dashboard that shows the data gathered. 

## Provider agnostic
The software suite is tailored for use with cloud providers for ease of use, but is built as _provider agnostic_ as possible. This means that you can decide on yourself what to use for each part of the application. Each part has a self-hosted or open source alternative so that you can run this software without relying on big tech. That being said, using the recommended options makes setting things up a lot easier and most alternatives have not been tested in production. 

#### The database
- Supabase (recommended, tested in production).
- Neon (implemented, not yet tested).
- Railway (implemented, not yet tested).
- Any local postgres instance. This is the self-hosted / DIY solution (implemented, not yet tested).

#### Script deployment
- With a cronjob on a local VPS or a local machine. This is the self-hosted / DIY solution (recommended).
- Railway (implemented, not yet tested).
- Render (implemented, not yet tested).
- Fly.io (implemented, not yet tested).

#### Dashboard deployment 
- Netlify (recommended, tested in production).
- Vercel (implemented, not yet tested).
- Cloudflare pages (implemented, not yet tested).
- Locally generated dist folder copied to a server. This is the self-hosted option / DIY solution.

#### Authentication
- Supabase Auth (recommended, tested in production).
- Auth0 (implemented, not yet tested).
- Clerk (implemented, not yet tested).
- Keycloak. This is the self-hosted, open source option (implemented, not yet tested).

## Default architecture
```
┌─────────────┐      ┌──────────────┐      ┌───────────┐
│  Scraper    │─────▶│  PostgreSQL  │◀─────│ Dashboard │
│ (cronjob)   │      │  (Supabase)  │      │ (Netlify) │
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
