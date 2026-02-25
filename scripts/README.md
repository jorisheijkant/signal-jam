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
