from helper import *
from log import *
from nfo import *


# noinspection PyClassHasNoInit
class AvalonXmlTvAgent(Agent.TV_Shows):
    name = "Avalon XML TV Agent"
    ver = "1.0.0"
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = ["com.plexapp.agents.localmedia"]

    def search(self, results, media, lang, manual):
        PlexLog.debug("==================== Search Start ====================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)
        PlexLog.info("Search for %s" % get_show_title(media))

        # Get the root element in nfo
        root_element = get_show_nfo(media)

        if root_element is None:
            PlexLog.error("Cannot find tvshow.nfo in show directory.")
            return None

        if root_element.tag != "tvshow":
            PlexLog.error("Invalid format. The root tag should be <tvshow>.")
            return None

        tv_nfo = TvNfo(root_element)

        title = tv_nfo.title
        if title is None:
            PlexLog.error("Invalid format. Missing <title> tag.")
            return None

        year = tv_nfo.originally_available_at.year if tv_nfo.originally_available_at is not None else 0
        PlexLog.debug("Title: %s" % title)
        PlexLog.debug("Year: %d" % year)

        results.Append(MetadataSearchResult(id=media.id, name=title, year=year, lang=lang, score=100))

        PlexLog.debug("====================  Search end  ====================")

    def update(self, metadata, media, lang, force):
        PlexLog.debug("==================== Update Start ====================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)
        PlexLog.info("Search for %s" % get_show_title(media))

        # Get the root element in nfo
        root_element = get_show_nfo(media)

        if root_element is None:
            PlexLog.error("Cannot find tvshow.nfo in show directory.")
            return None

        if root_element.tag != "tvshow":
            PlexLog.error("Invalid format. The root tag should be <tvshow>.")
            return None

        tv_nfo = TvNfo(root_element)
        tv_nfo.set_metadata(metadata)
        self.update_episode(metadata, media, tv_nfo.title)

        PlexLog.debug("====================  Update end  ====================")

    @staticmethod
    def update_episode(metadata, media, title):
        for season in media.seasons:
            for episode in media.seasons[season].episodes:
                PlexLog.debug("Update %s (season: %s, episode: %s)" % (title, season, episode))
                episode_metadata = metadata.seasons[season].episodes[episode]
                root_element = get_episode_nfo(media, season, episode)
                if root_element is None:
                    PlexLog.warn("Cannot find episode nfo")
                    continue
                if root_element.tag != "episodedetails":
                    PlexLog.warn("Invalid format. The root tag should be <episodedetails>.")
                    continue

                episode_nfo = EpisodeNfo(root_element)
                episode_nfo.set_metadata(episode_metadata)
                thumb_path, thumb = get_episode_thumb(media, season, episode)
                episode_metadata.thumbs[thumb_path] = thumb


# noinspection PyClassHasNoInit
class AvalonXmlMovieAgent(Agent.Movies):
    name = "Avalon XML Movie Agent"
    ver = "1.0.0"
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = ["com.plexapp.agents.localmedia"]

    def search(self, results, media, lang, manual):
        PlexLog.debug("==================== Search Start ====================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)
        PlexLog.info("Search for %s" % get_movie_title(media))

        # Get the root element in nfo
        root_element = get_movie_nfo(media)

        if root_element is None:
            PlexLog.error("Cannot find nfo in movie directory.")
            return None

        if root_element.tag != "movie":
            PlexLog.error("Invalid format. The root tag should be <movie>.")
            return None

        movie_nfo = MovieNfo(root_element)

        title = movie_nfo.title
        if title is None:
            PlexLog.error("Invalid format. Missing <title> tag.")
            return None

        year = movie_nfo.originally_available_at.year if movie_nfo.originally_available_at is not None else 0
        PlexLog.debug("Title: %s" % title)
        PlexLog.debug("Year: %d" % year)

        results.Append(MetadataSearchResult(id=year, name=title, year=year, lang=lang, score=100))

        PlexLog.debug("====================  Search end  ====================")

    def update(self, metadata, media, lang, force):
        PlexLog.debug("==================== Update Start ====================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)
        PlexLog.info("Search for %s" % get_movie_title(media))

        # Get the root element in nfo
        root_element = get_movie_nfo(media)

        if root_element is None:
            PlexLog.error("Cannot find nfo in movie directory.")
            return None

        if root_element.tag != "movie":
            PlexLog.error("Invalid format. The root tag should be <movie>.")
            return None

        movie_nfo = MovieNfo(root_element)
        movie_nfo.set_metadata(metadata)

        PlexLog.debug("====================  Update end  ====================")
        pass
