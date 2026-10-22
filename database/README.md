# Database

This folder contains the PostgreSQL schema for Signal Jam. You can use this schema to initialize the database of your choice.

## Schema Overview

The database consists of eight tables:

### `accounts`
Stores social media accounts that are being tracked.

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial | Primary key |
| `platform` | enum | twitter, tiktok, facebook, or instagram |
| `username` | varchar | Handle/username (unique per platform) |
| `account_url` | text | URL to the account profile (optional) |
| `display_name` | varchar | Display name (optional) |
| `is_watched` | boolean | True when the account is listed in a `source_data/*/…_users_to_scrape.json` file. Synced by the scrapers at the start of each run |
| `is_approved` | boolean | True once the account has 3 posts labeled as misinformation. Set by a trigger on `posts`, never by hand. Approved accounts get all their posts scraped; candidates only posts matching the theme filter terms |
| `created_at` | timestamptz | When we added this account |

### `posts`
Stores all scraped posts across platforms.

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial | Primary key |
| `url` | text | URL of the post (unique per platform) |
| `platform` | enum | twitter, tiktok, facebook, or instagram |
| `account_id` | integer | Foreign key to accounts |
| `content` | text | Post text content |
| `post_type` | enum | original, reply, repost, or quote |
| `parent_post_id` | integer | References original post (for replies/reposts/quotes) |
| `posted_at` | timestamptz | When the post was published |
| `scraped_at` | timestamptz | When we scraped the post |
| `likes` | integer | Like/favorite count |
| `reposts` | integer | Retweet/share count |
| `comments` | integer | Comment/reply count |
| `is_checked` | boolean | Whether the post has been reviewed |
| `is_relevant` | boolean | Moderation flag: false when a moderator marked the post as not belonging in the database |
| `relevant_for_signal_jam_theme` | boolean | Whether the post matches the theme filter terms (always true for term-search results) |
| `contains_misinformation` | boolean | Whether misinformation was found |
| `notes` | text | Free-text notes on the post (optional) |
| `frame_id` | integer | Foreign key to frames (optional) |
| `platform_data` | jsonb | Platform-specific metadata |

### `account_review_queue` (view)
Watched accounts that still need labeling, used by the labeling page. One row per account that is not yet approved, has unreviewed theme posts, and has enough own posts (confirmed + unreviewed) to reach the three needed for approval. Reposts are not counted, since they have no label of their own.

| Column | Type | Description |
|--------|------|-------------|
| `account_id`, `platform`, `username`, `account_url`, `display_name` | | The account |
| `confirmed_count` | bigint | Posts labeled as misinformation |
| `unreviewed_count` | bigint | Theme posts not yet reviewed |

### `frames`
Central misinformation themes that posts can be tagged with.

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial | Primary key |
| `name` | varchar | Unique frame name |
| `description` | text | Description of the frame (optional) |
| `created_at` | timestamptz | When the frame was created |

### `articles`
Articles scraped from Russian state media (RT, TASS, Lenta, Gazeta) and propaganda sites (Pravda NL). These are not social media posts, so they live outside of `posts`/`accounts`. The weekly propaganda summary in `summaries` is generated from them.

| Column | Type | Description |
|--------|------|-------------|
| `url` | text | Primary key, the URL of the article |
| `title` | text | Article title |
| `source` | text | Name of the outlet (e.g. `Tass`) |
| `author` | text | Author (optional) |
| `language` | varchar | Language code (optional) |
| `summary` | text | Summary as published in the feed (optional) |
| `content` | text | Full article text (optional) |
| `published_at` | timestamptz | When the article was published |
| `scraped_at` | timestamptz | When we scraped the article |

### `summaries`
Weekly AI-generated summaries of tracked content.

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial | Primary key |
| `week_start` | date | Monday of the summary week (unique) |
| `week_end` | date | Sunday of the summary week |
| `content` | text | Generated summary text |
| `llm_provider` | varchar | Which LLM generated the summary (optional) |
| `generated_at` | timestamptz | When the summary was generated |

## Setup by Provider

### Supabase (recommended)

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to the SQL Editor in your dashboard
3. Paste the contents of `schema.sql` and run it
4. Find your connection string under Settings > Database > Connection string
5. Add to your `.env`:
   ```
   DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
   ```

### Neon

1. Create a new project at [neon.tech](https://neon.tech)
2. Open the SQL Editor from your dashboard
3. Paste the contents of `schema.sql` and run it
4. Copy your connection string from the dashboard
5. Add to your `.env`:
   ```
   DATABASE_URL=postgresql://[user]:[password]@[host].neon.tech/[database]?sslmode=require
   ```

### Railway

1. Create a new project at [railway.app](https://railway.app)
2. Add a PostgreSQL database to your project
3. Connect using the provided credentials and run `schema.sql`
4. Copy the connection string from the Variables tab
5. Add to your `.env`:
   ```
   DATABASE_URL=postgresql://postgres:[password]@[host].railway.app:5432/railway
   ```

### Local PostgreSQL

1. Make sure PostgreSQL is installed and running
2. Create a new database:
   ```bash
   createdb signaljam
   ```
3. Run the schema:
   ```bash
   psql -d signaljam -f schema.sql
   ```
4. Add to your `.env`:
   ```
   DATABASE_URL=postgresql://localhost:5432/signaljam
   ```

### Neon, Railway, and local PostgreSQL — dashboard access via PostgREST

The dashboard runs in the browser and can't connect to a raw PostgreSQL database directly. Supabase handles this transparently via its built-in [PostgREST](https://postgrest.org) layer. For all other providers you need to run PostgREST yourself and set `VITE_DB_PROVIDER=postgrest` in the dashboard.

**Quick setup (Docker):**
```bash
docker run --rm -p 3000:3000 \
  -e PGRST_DB_URI="postgresql://user:password@host:5432/database" \
  -e PGRST_DB_SCHEMA="public" \
  -e PGRST_DB_ANON_ROLE="anon" \
  postgrest/postgrest
```

Then in `dashboard/.env`:
```
VITE_DB_PROVIDER=postgrest
VITE_POSTGREST_URL=http://localhost:3000
```

For production, deploy PostgREST as a container alongside your database and set `VITE_POSTGREST_URL` to its public URL. If you want to restrict access, configure a JWT secret in PostgREST and set `VITE_POSTGREST_ANON_KEY` to a signed anon token.

The `PGRST_DB_ANON_ROLE` must be a PostgreSQL role that has `SELECT` on the tables the dashboard reads, and `UPDATE`/`DELETE` on `posts` and `frames` for the labeling workflow. Create the role and grant permissions after running the schema:

```sql
CREATE ROLE anon NOLOGIN;
GRANT SELECT ON accounts, posts, summaries, frames, articles, post_reposts, account_review_queue TO anon;
GRANT UPDATE, DELETE ON posts, frames TO anon;
```

## Notes

- Adding a new platform to an existing database: the `platform` and `post_type` columns are Postgres enums, so new values need a migration rather than re-running `schema.sql`. For example, to add Instagram: `ALTER TYPE platform ADD VALUE 'instagram';` (run outside a transaction block; Postgres requires this for `ADD VALUE`).
- The `platform_data` JSONB column can store any platform-specific fields (e.g., video duration for TikTok, hashtags, media URLs)
- Posts are uniquely identified by `(platform, url)` to prevent duplicates
- Accounts are uniquely identified by `(platform, username)`
- The `contains_misinformation` field is nullable: `NULL` means not yet determined, `FALSE` means checked and clean, `TRUE` means flagged
- The `is_relevant` field defaults to `TRUE`; set to `FALSE` to exclude posts from analysis without deleting them
