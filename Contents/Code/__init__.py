from base64 import b64encode

from helper import *
from log import *
from xml import *

version = "2.0.0"


# noinspection PyClassHasNoInit
class AvalonXmlTvAgent(Agent.TV_Shows):
    name = "Avalon XML TV Agent"
    ver = version
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = ["com.plexapp.agents.localmedia"]

    def search(self, results, media, lang, manual):
        PlexLog.debug("==================== Search Start ====================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)
        PlexLog.info("Search for %s" % get_show_title(media))

        # Get the root element in nfo
        root_element = get_show_xml(media)

        if root_element is None:
            PlexLog.error("Cannot find tvshow.nfo in show directory.")
            return None

        if root_element.tag != "tvshow":
            PlexLog.error("Invalid format. The root tag should be <tvshow>.")
            return None

        tv_xml = TvXml(root_element)

        title = tv_xml.title
        if title is None:
            PlexLog.error("Invalid format. Missing <title> tag.")
            return None

        year = tv_xml.originally_available_at.year if tv_xml.originally_available_at is not None else 0
        PlexLog.debug("Title: %s" % title)
        PlexLog.debug("Year: %d" % year)

        # Plex throws exception that have "/" in ID
        mid = b64encode("%s:%d" % (title, year)).replace("/", "_")

        results.Append(MetadataSearchResult(id=mid, name=title, year=year, lang=lang, score=100))

        PlexLog.debug("====================  Search end  ====================")

    def update(self, metadata, media, lang, force):
        PlexLog.debug("==================== Update Start ====================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)
        PlexLog.info("Search for %s" % get_show_title(media))

        # Get the root element in xml
        root_element = get_show_xml(media)

        if root_element is None:
            PlexLog.error("Cannot find tvshow.nfo in show directory.")
            return None

        if root_element.tag != "tvshow":
            PlexLog.error("Invalid format. The root tag should be <tvshow>.")
            return None

        tv_xml = TvXml(root_element)
        put_update(str(media.id), "2", tv_xml.original_title, tv_xml.tagline)
        tv_xml.set_metadata(metadata)
        self.update_episode(metadata, media)

        PlexLog.debug("====================  Update end  ====================")

    @staticmethod
    def update_episode(metadata, media):
        title = get_show_title(media)
        for season in media.seasons:
            updated_summary = False
            for episode in media.seasons[season].episodes:
                if not updated_summary:
                    season_id = media.seasons[season].id
                    summary = get_summary_txt(media, season, episode)
                    if summary is not None:
                        put_update(season_id, "3", summary=summary)
                    updated_summary = True
                PlexLog.debug("Update %s (season: %s, episode: %s)" % (title, season, episode))
                episode_metadata = metadata.seasons[season].episodes[episode]
                root_element = get_episode_xml(media, season, episode)
                if root_element is None:
                    PlexLog.warn("Cannot find episode nfo (Season: %s, Episode: %s)" % (season, episode))
                    continue
                if root_element.tag != "episodedetails":
                    PlexLog.warn("Invalid format. The root tag should be <episodedetails>.")
                    continue

                episode_xml = EpisodeXml(root_element)
                episode_xml.set_metadata(episode_metadata)
                thumb_result = get_episode_thumb(media, season, episode)
                if thumb_result is not None:
                    thumb_path, thumb = thumb_result
                    episode_metadata.thumbs[thumb_path] = thumb


# noinspection PyClassHasNoInit
class AvalonXmlMovieAgent(Agent.Movies):
    name = "Avalon XML Movie Agent"
    ver = version
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = ["com.plexapp.agents.localmedia"]

    def search(self, results, media, lang, manual):
        PlexLog.debug("==================== Search Start ====================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)
        PlexLog.info("Search for %s" % get_movie_title(media))

        # Get the root element in xml
        root_element = get_movie_xml(media)

        if root_element is None:
            PlexLog.error("Cannot find xml in movie directory.")
            return None

        if root_element.tag != "movie":
            PlexLog.error("Invalid format. The root tag should be <movie>.")
            return None

        movie_xml = MovieXml(root_element)

        title = movie_xml.title
        if title is None:
            PlexLog.error("Invalid format. Missing <title> tag.")
            return None

        year = movie_xml.originally_available_at.year if movie_xml.originally_available_at is not None else 0
        PlexLog.debug("Title: %s" % title)
        PlexLog.debug("Year: %d" % year)

        # Plex throws exception that have "/" in ID
        mid = b64encode("%s:%d" % (title, year)).replace("/", "_")

        results.Append(MetadataSearchResult(id=mid, name=title, year=year, lang=lang, score=100))

        PlexLog.debug("====================  Search end  ====================")

    def update(self, metadata, media, lang, force):
        PlexLog.debug("==================== Update Start ====================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)
        PlexLog.info("Search for %s" % get_movie_title(media))

        # Get the root element in nfo
        root_element = get_movie_xml(media)

        if root_element is None:
            PlexLog.error("Cannot find nfo in movie directory.")
            return None

        if root_element.tag != "movie":
            PlexLog.error("Invalid format. The root tag should be <movie>.")
            return None

        movie_xml = MovieXml(root_element)
        movie_xml.set_metadata(metadata)

        PlexLog.debug("====================  Update end  ====================")


# noinspection PyClassHasNoInit
class AvalonXmlArtistAgent(Agent.Artist):
    name = "Avalon XML Artist Agent"
    ver = version
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = ["com.plexapp.agents.localmedia"]

    def search(self, results, media, lang, manual):
        PlexLog.debug("==================== Search Start ====================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)

        # Get the root element in xml
        root_element = get_artist_xml(media)

        if root_element is None:
            PlexLog.error("Cannot find xml in movie directory.")
            return None

        if root_element.tag != "artist":
            PlexLog.error("Invalid format. The root tag should be <artist>.")
            return None

        artist_xml = ArtistXml(root_element)

        title = artist_xml.title
        if title is None:
            PlexLog.error("Invalid format. Missing <title> tag.")
            return None

        PlexLog.debug("Artist: %s" % title)

        results.Append(MetadataSearchResult(id=media.id, name=title, lang=lang, year=None, score=100))

        PlexLog.debug("====================  Search end  ====================")

    def update(self, metadata, media, lang, force):
        PlexLog.debug("==================== Update Start ====================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)

        # Get the root element in xml
        root_element = get_artist_xml(media)

        if root_element is None:
            PlexLog.error("Cannot find xml in movie directory.")
            return None

        if root_element.tag != "artist":
            PlexLog.error("Invalid format. The root tag should be <artist>.")
            return None

        artist_xml = ArtistXml(root_element)
        artist_xml.set_metadata(metadata)

        PlexLog.debug("====================  Update end  ====================")
