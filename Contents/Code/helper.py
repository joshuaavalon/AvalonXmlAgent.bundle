import re
import urllib
import urllib2
from os.path import dirname, join, splitext, exists, basename

from log import *

IMAGE_EXTS = ['jpg', 'png', 'jpeg', 'tbn']
MOVIE_REGEX = "^(.*\S)\s+\((\d*)\).*$"
EPISODE_REGEX = "^(.*\S)\s+-\s+s\d{2,}e\d{2,}.*$"


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
    season_directory = dirname(file_path)
    return dirname(season_directory)


def get_movie_directory(media):
    file_path = get_movie_path(media)
    return dirname(file_path)


def get_movie_path(media):
    return media.items[0].parts[0].file


def get_artist_directory(media):
    for album in media.children:
        for track in album.children:
            track_dir = dirname(track.items[0].parts[0].file)
            return dirname(track_dir)
    return None


def get_album_directory(media):
    for track in media.children:
        return dirname(track.items[0].parts[0].file)
    return None


def get_show_xml_path(show_directory):
    """
    Get the tvshow.nfo from show directory.

    :param show_directory:
    :type show_directory: str
    :return: tvshow.nfo path
    """
    return select_exist(join(show_directory, "tvshow.xml"), join(show_directory, "tvshow.nfo"))


def get_show_title(media):
    return getattr(media, "show", getattr(media, "title", "Unknown"))


def get_movie_title(media):
    return getattr(media, "name", getattr(media, "title", "Unknown"))


def get_show_xml(media):
    show_directory = get_show_directory(media)
    if show_directory is None:
        return None
    nfo_path = get_show_xml_path(show_directory)
    if nfo_path is not None:
        xml_str = Core.storage.load(nfo_path)
        return XML.ElementFromString(xml_str)
    else:
        return None


def get_episode_xml(media, season, episode):
    standard_xml_path, fallback_xml_path = guess_episode_asset(media, season, episode, "xml")
    standard_nfo_path, fallback_nfo_path = guess_episode_asset(media, season, episode, "nfo")
    file_path = select_exist(standard_xml_path, standard_nfo_path, fallback_xml_path, fallback_nfo_path)
    if file_path is not None:
        xml_str = Core.storage.load(file_path)
        return XML.ElementFromString(xml_str)
    else:
        return None


def get_movie_xml(media):
    standard_xml_path, fallback_xml_path = guess_movie_asset(media, "xml")
    standard_nfo_path, fallback_nfo_path = guess_movie_asset(media, "nfo")
    file_path = select_exist(standard_xml_path, standard_nfo_path, fallback_xml_path, fallback_nfo_path)
    if file_path is not None:
        xml_str = Core.storage.load(file_path)
        return XML.ElementFromString(xml_str)
    else:
        return None


def get_artist_xml(media):
    file_directory = get_artist_directory(media)
    file_path = join(file_directory, "artist.xml")
    if exists(file_path):
        xml_str = Core.storage.load(file_path)
        return XML.ElementFromString(xml_str)
    else:
        return None


def get_album_xml(media):
    file_directory = get_album_directory(media)
    file_path = join(file_directory, "album.xml")
    if exists(file_path):
        xml_str = Core.storage.load(file_path)
        return XML.ElementFromString(xml_str)
    else:
        return None


def get_summary_txt(media, season, episode):
    file_path = media.seasons[season].episodes[episode].items[0].parts[0].file
    file_directory = dirname(file_path)
    standard_path = join(file_directory, "Summary.txt")
    if exists(standard_path):
        return Core.storage.load(standard_path)
    else:
        return None


def debug_print_object(obj):
    PlexLog.debug("debug_print_object")
    for attr in dir(obj):
        PlexLog.debug("obj.%s = %s" % (attr, getattr(obj, attr)))


def guess_episode_asset(media, season, episode, ext):
    file_path = media.seasons[season].episodes[episode].items[0].parts[0].file
    file_directory = dirname(file_path)
    title = guess_episode_name(file_path)
    standard_name = "%s - s%se%s.%s" % (title, season.zfill(2), episode.zfill(2), ext)
    standard_path = join(file_directory, standard_name)
    fallback_path = "%s.%s" % (splitext(file_path)[0], ext)
    return standard_path, fallback_path


def guess_movie_asset(media, ext):
    file_path = get_movie_path(media)
    file_directory = get_movie_directory(media)
    name, year = guess_movie_name_year(file_path)
    standard_name = "%s (%s).%s" % (name, year, ext)
    standard_path = join(file_directory, standard_name)
    fallback_path = "%s.%s" % (splitext(file_path)[0], ext)
    return standard_path, fallback_path


def guess_episode_name(file_path):
    file_name = basename(file_path)
    file_name_without_ext = splitext(file_name)[0]
    result = re.search(EPISODE_REGEX, file_name_without_ext)
    return result.group(1)


def guess_movie_name_year(file_path):
    file_name = basename(file_path)
    file_name_without_ext = splitext(file_name)[0]
    result = re.search(MOVIE_REGEX, file_name_without_ext)
    return result.group(1), result.group(2)


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
        if exists(path):
            thumb = Core.storage.load(path)
            return path, Proxy.Media(thumb)
    return None


def get_actor_thumb(name):
    actor_directory = Prefs["ActorsDirectory"]
    if not actor_directory or not exists(actor_directory):
        return ""
    for ext in IMAGE_EXTS:
        image_path = join(actor_directory, "%s.%s" % (name, ext))
        if exists(image_path):
            return image_path
    return ""


def select_exist(*args):
    for index, path in enumerate(args):
        print(path)
        if exists(path):
            return path
    return None


def put_update(media_id, update_type, title=None, tagline=None, summary=None):
    token = Prefs["Token"]
    if (title is None and tagline is None and summary is None) or not token:
        return
    page_url = "http://127.0.0.1:32400/library/metadata/" + media_id
    xml_element = XML.ElementFromURL(page_url)
    section = String.Unquote(xml_element.xpath("//MediaContainer")[0].get("librarySectionID").encode("utf-8"))
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    query = {"type": update_type, "id": media_id, "X-Plex-Token": token}  # Movie Type 1
    request_url = "http://127.0.0.1:32400/library/sections/" + section + "/all?"
    if title is not None:
        query["originalTitle.value"] = title
    if tagline is not None:
        query["tagline.value"] = tagline
    if summary is not None:
        query["summary.value"] = summary
    request_url += urllib.urlencode(query)
    request = urllib2.Request(request_url)
    request.get_method = lambda: 'PUT'
    try:
        url = opener.open(request)
        url.read()
    except urllib2.HTTPError as e:
        PlexLog.error("request_url %s" % request_url)
        PlexLog.error(str(e))


def update_album(media_id, title, album_xml):
    token = Prefs["Token"]
    if not token:
        return
    PlexLog.debug("DTIEL:" + title)
    page_url = "http://127.0.0.1:32400/library/metadata/" + media_id
    xml_element = XML.ElementFromURL(page_url)
    section = String.Unquote(xml_element.xpath("//MediaContainer")[0].get("librarySectionID").encode("utf-8"))
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    query = {"type": 9, "id": media_id, "X-Plex-Token": token}  # Movie Type 1
    request_url = "http://127.0.0.1:32400/library/sections/" + section + "/all?"
    query["titleSort.value"] = title
    # required to prevent Plex bug override
    query["titleSort.locked"] = 1
    i = 0
    for collection in album_xml.collections:
        query["collection[" + str(i) + "].tag.tag"] = collection
        i += 1
    request_url += urllib.urlencode(query)
    request = urllib2.Request(request_url)
    request.get_method = lambda: 'PUT'
    try:
        url = opener.open(request)
        url.read()
    except urllib2.HTTPError as e:
        PlexLog.error("request_url %s" % request_url)
        PlexLog.error(str(e))
