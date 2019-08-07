from __future__ import unicode_literals, division, absolute_import
from builtins import *  # noqa pylint: disable=unused-import, redefined-builtin

import logging

from datetime import datetime, timedelta

from flexget import plugin
from flexget.event import event
from flexget.manager import Session
from flexget.utils.tools import split_title_year

log = logging.getLogger('est_series_trakt')


class EstimatesSeriesTrakt(object):
    @plugin.priority(3)
    def estimate(self, entry):
        if not all(field in entry for field in ['series_name', 'series_season']):
            return
        series_name = entry['series_name']
        season = entry['series_season']
        episode_number = entry.get('series_episode')
        title, year_match = split_title_year(series_name)

        # This value should be added to input plugins to trigger a season lookup
        season_pack = entry.get('season_pack_lookup')

        kwargs = {
            'title': title,
            'year': entry.get('trakt_series_year')
            or entry.get('year')
            or entry.get('imdb_year')
            or year_match,
            'trakt_slug': entry.get('trakt_slug'),
            'tmdb_id': entry.get('tmdb_id'),
            'tvdb_id': entry.get('tvdb_id') or entry.get('trakt_series_tvdb_id'),
            'imdb_id': entry.get('imdb_id'),
            'tvrage_id': entry.get('tvrage_id') or entry.get('trakt_series_tvrage_id'),
        }

        api_trakt = plugin.get_plugin_by_name('api_trakt').instance
        log.debug('Searching api_trakt for series')
        for k, v in list(kwargs.items()):
            if v:
                log.debug('%s: %s', k, v)

        with Session(expire_on_commit=False) as session:
            try:
                trakt_series = api_trakt.lookup_series(session=session, **kwargs)
                if trakt_series is None:
                    return

                trakt_season = trakt_series.get_season(season, session)
                if trakt_season is None:
                    log.debug('%s doesn\'t have a season %s in trakt' %
                            (series_name, season))
                    return datetime.max
                if season_pack:
                    entity = trakt_season
                else:
                    entity = trakt_series.get_episode(season, episode_number, session)
                    if entity is None:
                        log.debug('%s doesn\'t have a season %s episode %s in trakt' %
                                (series_name, season, episode_number))
                        return datetime.max
            except LookupError as e:
                log.debug(str(e))
                return
        if entity and entity.first_aired:
            log.debug('received first-aired: %s', entity.first_aired)
            return entity.first_aired
        return


@event('plugin.register')
def register_plugin():
    plugin.register(EstimatesSeriesTrakt, 'est_series_trakt', interfaces=['estimate_release'], api_ver=2)
