from abc import ABC, abstractmethod
from typing import Optional

from core.conf import CoreSettings
from db.models.news import News
from db.models.session import SessionLocal
from parsers.parser import Api, NewsApi
from sqlalchemy.orm import Session


class ArticleManager(ABC):
    api_cls = None

    def __init__(self, db_session: Optional[Session] = None) -> None:
        if db_session is None:
            self.db_session = SessionLocal()
        else:
            self.db_session = db_session

    def create_api(self, **kwargs) -> Api:
        """Return news API class"""
        return self.api_cls(**kwargs)

    @abstractmethod
    def sync_news(self):
        """Use url news like unique key. The class is responsible for
        applying filters, process already saved news, update changed news"""


class NewsApiManager(ArticleManager):
    api_cls = NewsApi

    def sync_news(self):
        # create model for set up Api provided with data with access to news
        # model source shows only possible newsmaker portal
        # configurate filters
        settings = CoreSettings()
        api = self.create_api(
            base_url="https://newsapi.org/v2/top-headlines", creds={"api_key": settings.API_KEY}
        )

        news = api.get_news()
        news_emails = {item.original_link: item for item in news}

        uploaded_news = (
            self.db_session.query(News.uploaded_at, News.original_link)
            .filter(News.original_link.in_(news_emails.keys()))
            .all()
        )
        length_prepared_news = len(news)

        for uploaded_at, link in uploaded_news:
            if news_emails.get(link) is None:
                continue
            del news_emails[link]

        length_uploaded_news = len(news_emails.keys())

        self.db_session.add_all((News(**item.dict()) for item in news_emails.values()))
        self.db_session.commit()
        return (
            f"{length_prepared_news - length_uploaded_news}/"
            f"{length_prepared_news} news have been uploaded."
        )
        # second approach
        # for item in news:
        #     try:
        #         self.db_session.add(News(**item.dict()))
        #         self.db_session.commit()
        #     except Exception as e:
        #         print(e)
        # to do: connect news to source. Manage amount uploaded
        #  news, check last uploaded news, then stop uploading


a = NewsApiManager()
a.sync_news()
