# Scripts
This folder contains the scraping scripts that collect social media posts and push them to the database. X (Twitter), TikTok, and Instagram are supported; Facebook is not (Zeeschuimer, the browser extension these scripts rely on to capture posts, has no Facebook module).

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
cp .env.example .env
# fill in your database credentials
```

The accounts, search terms and filter terms to scrape live in the database: add them on the Instellingen page of the dashboard (see [Scrape settings](#scrape-settings)).

## Running

```bash
python scrape_x.py
python scrape_tiktok.py
python scrape_instagram.py
```

## Articles (Russian news outlets)

Besides social media, the scripts gather articles from Russian state media and propaganda sites into the `articles` table. `summarize_weeks.py` uses them for the weekly propaganda summary, and the dashboard shows them on the Artikelen page.

| Script | What it does |
|--------|--------------|
| `scrape_russian_rss.py` | Reads the RSS feeds in `source_data/articles/russian_feeds.json` and scrapes the full text of new articles |
| `scrape_pravda.py` | Scrapes the Pravda sites in `source_data/articles/pravda_sources.json` |
| `migrate_source_desk_articles.py` | One-off copy of the old Source Desk database (`SOURCE_DESK_DATABASE_URL` constant in the script) into `DATABASE_URL`. Run with `--dry-run` first; re-running is safe |

Copy the `*.example.json` files in `source_data/articles/` to the same name without `.example` to configure them. `search_terms.json` decides which articles end up in the weekly summary. Set `DNS_RESOLVER` / `DNS_OVER_HTTPS_URL` in `.env` if your ISP blocks the Russian domains.

## Scrape settings

What to scrape is stored in the database and managed by logged-in users on the Instellingen page of the dashboard. Every scraper run reads the current settings.

| Setting | Stored in | Description |
|---|---|---|
| Accounts | `accounts` with `is_watched = true` | The accounts whose posts are scraped |
| Search terms | `scrape_terms`, kind `search` | Terms searched on the platform: X search, TikTok search, or Instagram's `/explore/search/keyword/` page |
| Filter terms | `scrape_terms`, kind `filter` | Theme word filter applied to user scrape results (see below) |

To move an existing setup over, run `python import_source_data.py` once. It reads the old `source_data/<platform>/` JSON files (users, search terms and filter terms; missing files are skipped) into the database and can be re-run safely. After that those files are no longer used. Only `source_data/articles/` is still read from disk.

### Theme flag and account approval
Every post gets `relevant_for_signal_jam_theme`. It is true when the content contains at least one filter term (case-insensitive). Posts from **term scrapes** are always flagged, since they are already targeted by the search term itself.

Whether a post is stored depends on the account:
- **Approved accounts** (`accounts.is_approved`): all posts are stored, flagged or not.
- **Candidate accounts** (new or not yet approved): only flagged posts are stored, so they can be labeled by hand.

Watched accounts (`accounts.is_watched`) that are not yet approved are shown as cards on the labeling page. Accounts found only through search terms are reviewed post by post.

An account becomes approved automatically once it has three posts labeled `contains_misinformation` (database trigger, see `database/schema.sql`).

On X, replies are not scraped by default, to prevent overly long discussion from landing in the database in full.

## Cloud deployment

The scraper uses Selenium with Firefox and the Zeeschuimer browser extension, which means the container needs Firefox + geckodriver, and a Firefox profile that is already logged into X. The `Dockerfile` in this folder handles the first requirement; the profile requires a one-time manual setup step described below.

### Getting the Firefox profile to the cloud

The scraper authenticates to X through the cookies in your local Firefox profile. To deploy to the cloud you need to copy that profile to a persistent volume:

1. **Locate your local profile** — the script prints the path when you run it locally. Typically `~/.mozilla/firefox/<profile-id>` on Linux, `~/AppData/Roaming/Mozilla/Firefox/Profiles/<id>` on Windows, `~/Library/Application Support/Firefox/Profiles/<id>` on macOS.
2. **Archive it** — `tar -czf firefox-profile.tar.gz ~/.mozilla/firefox/<profile-id>` (do this while Firefox is closed)
3. **Upload** it to the persistent volume on your chosen platform (see platform-specific instructions below).
4. **Set `FIREFOX_PROFILE_PATH`** to point to the extracted directory on the volume.

> Re-upload the profile whenever X's session cookies expire and you need to log in again.

### Railway

1. In the Railway dashboard create a new project and choose **Deploy from GitHub repo**.
2. Set the **root directory** to `scripts/`.
3. Railway will detect `railway.toml` and use the `Dockerfile` automatically.
4. Add a **Volume** and mount it to `/data`. Upload your Firefox profile there and extract it to `/data/firefox-profile`.
5. Add environment variables: `DATABASE_URL`, `FIREFOX_PROFILE_PATH=/data/firefox-profile`, and any others from `.env.example`.
6. Under **Settings → Deploy**, set the **Cron schedule** (e.g. `0 */6 * * *` for every 6 hours).

### Render

1. Push `render.yaml` to your repo (it lives in `scripts/`).
2. In the Render dashboard click **New → Blueprint** and connect your repo, pointing to `scripts/render.yaml`.
3. Render will create a **Cron Job** service with a 1 GB persistent disk mounted at `/data`.
4. Use Render's shell or a one-off job to upload and extract your Firefox profile to `/data/firefox-profile`.
5. Add environment variables in the Render dashboard: `DATABASE_URL` and any others from `.env.example`.

### Fly.io

Fly.io has no native cron scheduler, so the container runs once per trigger. Use a GitHub Action or an external cron to schedule runs.

```bash
# One-time setup
fly auth login
fly apps create signal-jam-scraper
fly volumes create firefox_profile --region ams --size 1
fly deploy --config fly.toml

# Upload your Firefox profile to the volume
fly ssh console
# Inside the console:
# tar -xzf /tmp/firefox-profile.tar.gz -C /data/firefox-profile
```

Set secrets:
```bash
fly secrets set DATABASE_URL="postgresql://..." FIREFOX_PROFILE_PATH="/data/firefox-profile"
```

Trigger a run:
```bash
fly machines run signal-jam-scraper --region ams
```

To schedule it, add this to a GitHub Actions workflow:
```yaml
- name: Trigger scraper
  run: fly machines run signal-jam-scraper --region ams
  env:
    FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### Local / VPS cron job

Run the script directly and schedule it with cron. No Docker needed — just install dependencies and set up your `.env`:

```bash
pip install -r requirements.txt
cp /path/to/source_data/* source_data/
```

Example crontab entry (every 6 hours):
```
0 */6 * * * cd /path/to/signal-jam/scripts && /usr/bin/python3 scrape_x.py >> cronlog.log 2>&1
```
