import json
from datetime import date, timedelta
from pathlib import Path


def load_articles_for_week(articles_dir: Path, week_start: date, week_end: date) -> list[dict]:
    """Load source-desk's exported articles (see source-desk/scripts/export_articles.py)
    for each day in [week_start, week_end], skipping days with no export file."""
    articles = []
    day = week_start
    while day <= week_end:
        day_file = articles_dir / f"{day.isoformat()}.json"
        if day_file.exists():
            articles.extend(json.loads(day_file.read_text(encoding='utf-8')))
        day += timedelta(days=1)
    return articles
