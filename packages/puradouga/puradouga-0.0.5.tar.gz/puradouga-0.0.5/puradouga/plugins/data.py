from datetime import datetime
from typing import List


class FilenameParsed:
    title: str = None
    season: str = None
    episode: str = None
    source: str = None


class Title:
    english: str = None
    romaji: str = None
    native: str = None


class Image:
    title: str = None
    description: str = None
    file: str = None
    type: str = None


class SeriesResponse:
    title: Title = None
    description: str = None
    images: List[Image] = []
    start_date: datetime = None
    end_date: datetime = None
    url: str = None
    nsfw: bool = None


class SeasonResponse:
    series: SeriesResponse = None
    season: int = None


class EpisodeResponse:
    season: SeasonResponse = None
    title: Title = None
    episode: int = None
    description: str = None
    images: List[Image] = []
    airdate: datetime = None
    length: float = None
