from puradouga.core import PluginBase
from puradouga.plugins import data as d


class TvMetaProvider(PluginBase):
    def series_from_filename(self, filename_parsed: d.FilenameParsed) -> d.SeriesResponse:
        pass

    def season_from_filename(self, filename_parsed: d.FilenameParsed, series: d.SeriesResponse) -> d.SeasonResponse:
        pass

    def episode_from_filename(self, filename_parsed: d.FilenameParsed, season: d.SeasonResponse) -> d.EpisodeResponse:
        pass
