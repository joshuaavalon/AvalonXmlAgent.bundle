from datetime import datetime

from helper import get_actor_thumb


# noinspection PyClassHasNoInit
class XmlUtil:
    @staticmethod
    def get_text(element, tag, default=None):
        """
        Get the text of the first child tag's text
        :type element: _Element
        :type tag: str
        :param element:
        :param tag:
        :param default:
        :rtype: str
        :return:
        """
        tag_element = element.find(tag)
        text = default
        if tag_element is not None:
            text = tag_element.text
        return text

    @staticmethod
    def get_list(element, tag):
        tag_elements = element.findall(tag)
        tag_set = []
        for tag_element in tag_elements:
            tag_text = tag_element.text
            if tag_text:
                tag_set.append(tag_text)
        return tag_set

    @staticmethod
    def get_date(element, tag):
        text = XmlUtil.get_text(element, tag)
        if text is None:
            return None
        try:
            date = datetime.strptime(text, "%Y-%m-%d")
        except ValueError:
            return None
        return date

    @staticmethod
    def get_actors(element, tag):
        tag_elements = element.findall(tag)
        actors = []
        for tag_element in tag_elements:
            name = XmlUtil.get_text(tag_element, "name", "")
            role = XmlUtil.get_text(tag_element, "role", "")
            thumb = XmlUtil.get_text(tag_element, "thumb", "")
            if not thumb:
                thumb = get_actor_thumb
            actors.append((name, role, thumb))
        return actors

    @staticmethod
    def set_metadata_value_field(source, metadata, field, none_check=True):
        source_value = getattr(source, field)
        if not none_check or source_value is not None:
            setattr(metadata, field, source_value)

    @staticmethod
    def set_metadata_set_field(source, metadata, field):
        source_list = getattr(source, field)
        metadata_list = getattr(metadata, field)
        if source_list is not None and metadata_list is not None:
            metadata_list.clear()
            for value in source_list:
                metadata_list.add(value)

    @staticmethod
    def set_metadata_set_name_field(source, metadata, field):
        source_list = getattr(source, field)
        metadata_list = getattr(metadata, field)
        if source_list is not None and metadata_list is not None:
            metadata_list.clear()
            for value in source_list:
                metadata_list.new().name = value


class BaseXml:
    def __init__(self, root_element):
        self.root_element = root_element  # type: _Element
        self.value_fields = []
        self.set_fields = []

    def get_text_from_root(self, tag):
        return XmlUtil.get_text(self.root_element, tag)

    def get_list_from_root(self, tag):
        return XmlUtil.get_list(self.root_element, tag)

    def get_date_from_root(self, tag):
        return XmlUtil.get_date(self.root_element, tag)

    def get_rating_from_root(self, tag):
        rating_str = self.get_text_from_root(tag)
        if rating_str is None:
            return None
        # Round rating to 1 decimal place
        rating = round(float(rating_str), 1)
        return rating

    def set_metadata(self, metadata):
        for field in self.value_fields:
            XmlUtil.set_metadata_value_field(self, metadata, field)

        for field in self.set_fields:
            XmlUtil.set_metadata_set_field(self, metadata, field)

    def __repr__(self):
        repr_str = ""
        for field in self.value_fields:
            repr_str += "%s: %s\n" % (field, getattr(self, field))
        for field in self.set_fields:
            repr_str += "%s: %s\n" % (field, getattr(self, field))
        return repr_str


class TvXml(BaseXml):
    def __init__(self, root_element):
        BaseXml.__init__(self, root_element)
        self.value_fields = [
            "title",
            "title_sort",
            "original_title",
            "content_rating",
            "studio",
            "originally_available_at",
            "summary",
            "rating"
        ]
        self.set_fields = [
            "genres",
            "collections"
        ]
        self.title = self.extract_title()  # type: str
        self.title_sort = self.extract_title_sort()  # type: str
        self.original_title = self.extract_original_title()  # type: str
        self.content_rating = self.extract_content_rating()  # type: str
        self.tagline = self.extract_tagline()  # type: str
        self.studio = self.extract_studio()  # type: str
        self.originally_available_at = self.extract_originally_available_at()  # type: datetime
        self.summary = self.extract_summary()  # type: str
        self.rating = self.extract_rating()  # type: float
        self.genres = self.extract_genres()  # type: set
        self.collections = self.extract_collections()  # type: set
        self.actors = self.extract_actors()

    def extract_title(self):
        return self.get_text_from_root("title")

    def extract_originally_available_at(self):
        return self.get_date_from_root("premiered")

    def extract_title_sort(self):
        return self.get_text_from_root("sorttitle")

    def extract_original_title(self):
        return self.get_text_from_root("originaltitle")

    def extract_content_rating(self):
        return self.get_text_from_root("mpaa")

    def extract_studio(self):
        return self.get_text_from_root("studio")

    def extract_tagline(self):
        return self.get_text_from_root("tagline")

    def extract_summary(self):
        return self.get_text_from_root("plot")

    def extract_rating(self):
        return self.get_rating_from_root("rating")

    def extract_genres(self):
        return self.get_list_from_root("genre")

    def extract_collections(self):
        return self.get_list_from_root("set")

    def extract_actors(self):
        return XmlUtil.get_actors(self.root_element, "actor")

    def set_metadata(self, metadata):
        BaseXml.set_metadata(self, metadata)
        self.set_metadata_actors(metadata)

    def set_metadata_actors(self, metadata):
        metadata.roles.clear()
        for actor in self.actors:
            role = metadata.roles.new()
            role.name, role.role, role.photo = actor


class EpisodeXml(BaseXml):
    def __init__(self, root_element):
        BaseXml.__init__(self, root_element)
        self.value_fields = [
            "title",
            "content_rating",
            "originally_available_at",
            "summary",
            "rating"
        ]
        self.title = self.extract_title()  # type: str
        self.content_rating = self.extract_content_rating()  # type: str
        self.originally_available_at = self.extract_originally_available_at()  # type: datetime
        self.summary = self.extract_summary()  # type: str
        self.rating = self.extract_rating()  # type: float
        self.producers = self.extract_producers()  # type: set
        self.writers = self.extract_writers()  # type: set
        self.guest_stars = self.extract_guest_stars()  # type: set
        self.directors = self.extract_directors()  # type: set

    def extract_title(self):
        return self.get_text_from_root("title")

    def extract_content_rating(self):
        return self.get_text_from_root("mpaa")

    def extract_originally_available_at(self):
        return self.get_date_from_root("aired")

    def extract_summary(self):
        return self.get_text_from_root("plot")

    def extract_rating(self):
        return self.get_rating_from_root("rating")

    def extract_producers(self):
        return self.get_list_from_root("producer")

    def extract_writers(self):
        return self.get_list_from_root("writer")

    def extract_guest_stars(self):
        return self.get_list_from_root("guest")

    def extract_directors(self):
        return self.get_list_from_root("director")

    def set_metadata(self, metadata):
        BaseXml.set_metadata(self, metadata)
        XmlUtil.set_metadata_set_name_field(self, metadata, "producers")
        XmlUtil.set_metadata_set_name_field(self, metadata, "writers")
        XmlUtil.set_metadata_set_name_field(self, metadata, "guest_stars")
        XmlUtil.set_metadata_set_name_field(self, metadata, "directors")


class MovieXml(TvXml):
    def __init__(self, root_element):
        TvXml.__init__(self, root_element)
        self.producers = self.extract_producers()  # type: set
        self.writers = self.extract_writers()  # type: set
        self.directors = self.extract_directors()  # type: set
        self.year = self.originally_available_at.year  # type: int
        self.value_fields.append("year")

    def extract_originally_available_at(self):
        return self.get_date_from_root("releasedate")

    def extract_producers(self):
        return self.get_list_from_root("producer")

    def extract_writers(self):
        return self.get_list_from_root("writer")

    def extract_directors(self):
        return self.get_list_from_root("director")

    def set_metadata(self, metadata):
        TvXml.set_metadata(self, metadata)
        XmlUtil.set_metadata_value_field(self, metadata, "tagline")
        XmlUtil.set_metadata_set_name_field(self, metadata, "producers")
        XmlUtil.set_metadata_set_name_field(self, metadata, "writers")
        XmlUtil.set_metadata_set_name_field(self, metadata, "directors")


class ArtistXml(BaseXml):
    def __init__(self, root_element):
        BaseXml.__init__(self, root_element)
        self.value_fields = [
            "summary",
            "rating"
        ]
        self.set_fields = [
            "genres",
            "collections",
            "similar"
        ]
        self.summary = self.extract_summary()  # type: str
        self.rating = self.extract_rating()  # type: float
        self.genres = self.extract_genres()  # type: set
        self.collections = self.extract_collections()  # type: set
        self.similar = self.extract_similar()  # type: set

    def extract_summary(self):
        return self.get_text_from_root("summary")

    def extract_genres(self):
        return self.get_list_from_root("genre")

    def extract_rating(self):
        return self.get_rating_from_root("rating")

    def extract_collections(self):
        return self.get_list_from_root("set")

    def extract_similar(self):
        return self.get_list_from_root("similar")


class AlbumXml(BaseXml):
    def __init__(self, root_element):
        BaseXml.__init__(self, root_element)
        self.value_fields = [
            "originally_available_at",
            "summary",
            "rating"
        ]
        self.set_fields = [
            "genres",
            "collections"
        ]
        self.originally_available_at = self.extract_originally_available_at()  # type: datetime
        self.summary = self.extract_summary()  # type: str
        self.rating = self.extract_rating()  # type: float
        self.genres = self.extract_genres()  # type: set
        self.collections = self.extract_collections()  # type: set

    def extract_originally_available_at(self):
        return self.get_date_from_root("aired")

    def extract_summary(self):
        return self.get_text_from_root("summary")

    def extract_genres(self):
        return self.get_list_from_root("genre")

    def extract_rating(self):
        return self.get_rating_from_root("rating")

    def extract_collections(self):
        return self.get_list_from_root("set")
