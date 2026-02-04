from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Post:
    platform: str
    account_id: int
    posted_at: datetime
    url: Optional[str] = None
    content: Optional[str] = None
    post_type: str = 'original'
    parent_post_id: Optional[int] = None
    likes: int = 0
    reposts: int = 0
    comments: int = 0
    is_checked: bool = False
    contains_misinformation: Optional[bool] = None
    platform_data: Optional[dict] = None
    id: Optional[int] = None
    scraped_at: Optional[datetime] = field(default=None)
