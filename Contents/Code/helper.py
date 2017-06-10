import os

from log import *

IMAGE_EXTS = ['jpg', 'png', 'jpeg', 'tbn']


def get_show_directory(media):
    """
    Get the show directory.

    :param media: File path of a episode file.
    :type media: Media
    :return: Path of the show directory
    :rtype: str
    """
    file_path = None
    for season in media.seasons:
        for episode in media.seasons[season].episodes:
            file_path = media.seasons[season].episodes[episode].items[0].parts[0].file
    if file_path is None:
        return None
    season_directory = os.path.dirname(file_path)
    return os.path.dirname(season_directory)


def get_movie_directory(media):
    file_path = get_movie_path(media)
    return os.path.dirname(file_path)


def get_movie_path(media):
    return media.items[0].parts[0].file


def get_show_nfo_path(show_directory):
    """
    Get the tvshow.nfo from show directory.

    :param show_directory:
    :type show_directory: str
    :return: tvshow.nfo path
    """
    return os.path.join(show_directory, "tvshow.nfo")


def get_show_title(media):
    return getattr(media, "show", getattr(media, "title", "Unknown"))


def get_movie_title(media):
    return getattr(media, "name", getattr(media, "title", "Unknown"))


def get_movie_year(media):
    return getattr(media, "year", getattr(media, "id", -1))


def get_show_nfo(media):
    show_directory = get_show_directory(media)
    if show_directory is None:
        return None
    nfo_path = get_show_nfo_path(show_directory)
    if os.path.exists(nfo_path):
        xml_str = Core.storage.load(nfo_path)
        return XML.ElementFromString(xml_str)
    else:
        return None


def get_episode_nfo(media, season, episode):
    standard_nfo_path, fallback_nfo_path = guess_episode_asset(media, season, episode, "nfo")
    nfo_path = None
    if os.path.exists(standard_nfo_path):
        nfo_path = standard_nfo_path
    else:
        if os.path.exists(fallback_nfo_path):
            nfo_path = fallback_nfo_path
    if nfo_path is not None:
        xml_str = Core.storage.load(nfo_path)
        return XML.ElementFromString(xml_str)
    else:
        return None


def get_movie_nfo(media):
    standard_nfo_path, fallback_nfo_path = guess_movie_asset(media, "nfo")
    nfo_path = None
    if os.path.exists(standard_nfo_path):
        nfo_path = standard_nfo_path
    else:
        if os.path.exists(fallback_nfo_path):
            nfo_path = fallback_nfo_path
    if nfo_path is not None:
        xml_str = Core.storage.load(nfo_path)
        return XML.ElementFromString(xml_str)
    else:
        return None


def debug_print_object(obj):
    PlexLog.debug("debug_print_object")
    for attr in dir(obj):
        PlexLog.debug("obj.%s = %s" % (attr, getattr(obj, attr)))


def guess_episode_asset(media, season, episode, ext):
    file_path = media.seasons[season].episodes[episode].items[0].parts[0].file
    file_directory = os.path.dirname(file_path)
    title = get_show_title(media)
    standard_name = "%s - s%se%s.%s" % (title, season.zfill(2), episode.zfill(2), ext)
    standard_path = os.path.join(file_directory, standard_name)
    fallback_path = "%s.%s" % (os.path.splitext(file_path)[0], ext)
    return standard_path, fallback_path


def guess_movie_asset(media, ext):
    file_path = get_movie_path(media)
    file_directory = get_movie_directory(media)
    name = get_movie_title(media)
    debug_print_object(media)
    year = get_movie_year(media)
    standard_name = "%s (%s).%s" % (name, year, ext)
    standard_path = os.path.join(file_directory, standard_name)
    fallback_path = "%s.%s" % (os.path.splitext(file_path)[0], ext)
    return standard_path, fallback_path


def get_episode_thumb(media, season, episode):
    standard_thumb_paths = []
    fallback_thumb_paths = []
    for ext in IMAGE_EXTS:
        standard_thumb_path, fallback_thumb_path = guess_episode_asset(media, season, episode, ext)
        standard_thumb_paths.append(standard_thumb_path)
        fallback_thumb_paths.append(fallback_thumb_path)
    paths = []
    paths.extend(standard_thumb_paths)
    paths.extend(fallback_thumb_paths)
    for path in paths:
        if os.path.exists(path):
            thumb = Core.storage.load(path)
            return path, Proxy.Media(thumb)
    return None


def get_actor_thumb(name):
    actor_directory = Prefs["ActorsDirectory"]
    if not actor_directory or not os.path.exists(actor_directory):
        return ""
    for ext in IMAGE_EXTS:
        image_path = os.path.join(actor_directory, "%s.%s" % (name, ext))
        if os.path.exists(image_path):
            return image_path
    return ""
