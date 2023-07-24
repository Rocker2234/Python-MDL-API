from __future__ import annotations
from enum import Enum

__all__ = ['SearchType', 'LocalEnum', 'TitleType', 'TitleStatus', 'TitleSortedByType']


class LocalEnum(Enum):
    def __str__(self):
        return f'{self.value}'


class SearchType(LocalEnum):
    """
    Enumerator representing adv search type
    * **TITLE** - White
    * **PEOPLE** - Gray
    * **ARTICLES** - Black
    """
    TITLE = 'titles'
    PEOPLE = 'people'
    ARTICLES = 'articles'


class TitleType(LocalEnum):
    DRAMAS = 68
    DRAMA_SPECIAL = 83
    TV_SHOWS = 86
    MOVIES = 77


class TitleStatus(LocalEnum):
    ONGOING = 1
    COMPLETED = 3
    UPCOMING = 2


class TitleSortedByType(LocalEnum):
    RELEVANCE = "relevance"
    MOST_POPULAR = "popular"
    TOP_RANKED = "top"
    TOP_RATED = "rated"
    NEWEST = "newest"
    RELEASE_DATE = "date"
    RECENTLY_ADDED = "recently"
