# Scripts
This folder contains the scraping scripts that collect social media posts and push them to the database. Currently only X (Twitter) is supported.

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
cp .env.example .env
# fill in your database credentials
```

Set up your source data files (see [Source data](#source-data) below):
```bash
cp source_data/x_users_to_scrape.example.json source_data/x_users_to_scrape.json
cp source_data/terms_to_scrape.example.json source_data/terms_to_scrape.json
cp source_data/filter_terms.example.json source_data/filter_terms.json
```

Then edit each file with your actual values before running.

## Running

```bash
python scrape_x.py
```

## Source data

Configuration for what to scrape lives in `source_data/`. These files are gitignored — only the `.example.json` versions are committed. Copy them and fill in your own values.

| File | Description |
|---|---|
| `x_users_to_scrape.json` | List of X accounts to scrape, as `{name, url}` objects |
| `terms_to_scrape.json` | List of search terms used for X term searches |
| `filter_terms.json` | Word filter applied to user scrape results (see below) |

### Word filter
Posts from **user scrapes** are only pushed to the database if their content contains at least one word from `filter_terms.json`. This keeps the dataset focused on relevant content when scraping accounts that post about many topics.

Posts from **term scrapes** are not filtered — they are already targeted by the search term itself.

The filter is case-insensitive.

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
