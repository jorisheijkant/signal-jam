from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Account:
    platform: str
    username: str
    account_url: Optional[str] = None
    display_name: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = field(default=None)
