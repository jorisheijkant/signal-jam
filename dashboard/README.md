# Vue Dashboard
The front-end of the application consists of a Vue dashboard, presenting the data to authenticated users. It is built in the same _provider agnostic_ way as the other parts of the application, allowing you to swap out different tools for authentication and database integration.

## Pages
- **Dashboard** — shows labeled posts with misinformation highlighted, along with stats modules (daily activity, most active accounts, topics).
- **Labeling** — authenticated users can review scraped posts and label them: mark as irrelevant (deletes the post), flag for misinformation, add notes, and mark as checked. Only checked posts appear on the dashboard.

## Setup

```bash
cd dashboard
yarn install
cp .env.example .env
# fill in your .env values (see below)
yarn dev
```

The dev server runs at `http://localhost:5173` by default.

## Environment variables

See the `.env.example` for the needed environment variables. 

## Database

For your database of choice, make sure you use the correct RLS-policies. Updating and deleting permissions (to authenitcated users!) are needed for a proper content labeling workflow.

### Authentication
Make sure to install your authentication method of choice before running the app. By default it uses Supabase Auth, with a magic link workflow. 

## Deployment

SPA routing requires every URL to serve `index.html` — the configs below handle this for each platform.

### Netlify

Zero config beyond connecting the repo. The `public/_redirects` file handles SPA routing automatically.

1. Connect your repository to Netlify.
2. Set the build command to `yarn build` and the publish directory to `dist`.
3. Add all environment variables from `.env.example` under _Site settings → Environment variables_, setting `VITE_AUTH_REDIRECT_URL` to your Netlify domain.

### Vercel

Zero config — Vercel auto-detects Vite. The `vercel.json` in this folder handles SPA routing.

1. Import your repository in Vercel and set the root directory to `dashboard`.
2. Add all environment variables from `.env.example` under _Project settings → Environment variables_, setting `VITE_AUTH_REDIRECT_URL` to your Vercel domain.

### Cloudflare Pages

The same `public/_redirects` file used by Netlify also works on Cloudflare Pages.

1. Connect your repository in Cloudflare Pages.
2. Set the build command to `yarn build`, the build output directory to `dist`, and the root directory to `dashboard`.
3. Add all environment variables under _Settings → Environment variables_, setting `VITE_AUTH_REDIRECT_URL` to your Cloudflare Pages domain.

### DIY (copy dist to a server)

Run `yarn build` locally and copy the `dist/` folder to your server. Configure your web server to serve `index.html` for all routes:

**nginx**
```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

**Apache** (`.htaccess`)
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

## Provider agnostic layer

Auth and database access are abstracted behind provider modules:

- **Auth**: `src/auth/index.js` — swap providers via `VITE_AUTH_PROVIDER`
- **Database**: `src/database/index.js` — swap providers via `VITE_DB_PROVIDER`

To add a new provider, implement the same interface as the existing Supabase provider and register it in the respective `index.js`.

## Dashboard start date

Older posts are kept in the database but excluded from the dashboard and labeling queue. The cutoff is set in `src/database/index.js`:

```js
const DASHBOARD_START_DATE = '2026-01-01'
```

Change this value to widen or narrow which posts are shown. The format is `YYYY-MM-DD`. This constant lives in `index.js` (not inside a provider) so it applies automatically to any database provider you add.
