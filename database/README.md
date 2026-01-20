# Database

This folder contains the PostgreSQL schema for Signal Jam.

## Schema Overview

The database consists of two main tables:

### `accounts`
Stores social media accounts that are being tracked.

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial | Primary key |
| `platform` | enum | twitter, tiktok, or facebook |
| `platform_id` | varchar | The account's ID on the platform |
| `username` | varchar | Handle/username |
| `display_name` | varchar | Display name (optional) |
| `created_at` | timestamptz | When we added this account |

### `posts`
Stores all scraped posts across platforms.

| Column | Type | Description |
|--------|------|-------------|
| `id` | serial | Primary key |
| `platform` | enum | twitter, tiktok, or facebook |
| `platform_id` | varchar | The post's ID on the platform |
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
| `contains_misinformation` | boolean | Whether misinformation was found |
| `platform_data` | jsonb | Platform-specific metadata |

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

## Notes

- The `platform_data` JSONB column can store any platform-specific fields (e.g., video duration for TikTok, hashtags, media URLs)
- Posts are uniquely identified by `(platform, platform_id)` to prevent duplicates
- The `contains_misinformation` field is nullable: `NULL` means not yet determined, `FALSE` means checked and clean, `TRUE` means flagged
