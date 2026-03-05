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

## Deployment (Netlify)

1. Connect your repository to Netlify.
2. Set the build command to `yarn build` and the publish directory to `dist`.
3. Add all environment variables from `.env.example` under _Site settings → Environment variables_, using your production Supabase credentials and setting `VITE_AUTH_REDIRECT_URL` to your Netlify domain.

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
