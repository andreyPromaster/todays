# creds

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import uuid4

import requests
from dateutil.parser import isoparse
from schemas.news import News
from slugify import slugify

# creds will store on json field in postgres for each newsmaker


class Api(ABC):
    """Interface to get the data from newsmaker api"""

    def __init__(
        self, base_url: str, creds: Optional[dict] = None, filters: Optional[dict] = None
    ) -> None:
        self.base_url = base_url
        self.creds = creds
        self.filters = filters

    @abstractmethod
    def get_news(self, filters: Optional[dict] = None) -> list[News]:
        """Get news by key"""


class NewsApi(Api):
    def get_news(self, filters: Optional[dict] = None) -> list[News]:
        headers = {
            "X-Api-Key": self.creds["api_key"],
            "Accept": "application/json",
            "Content-type": "application/json",
        }
        filters = filters or dict()
        filters["pageSize"] = 100  # max items in one page
        filters["country"] = "us"
        response = requests.get(self.base_url, params=filters, headers=headers)
        data = response.json()
        if data["status"] == "error":
            raise Exception(f"Can`t fetch news from {response.url}")
        articles = data["articles"]
        result = []
        uploaded_at = datetime.now()
        for item in articles:
            slug = slugify(item["title"])
            result.append(
                News(
                    created_at=isoparse(item["publishedAt"]),
                    slug=slug,
                    text=item["content"] or item["description"],
                    uploaded_at=uploaded_at,
                    original_link=item["url"],
                    author=item["author"],
                    uid=str(uuid4()),
                )
            )
        return result
