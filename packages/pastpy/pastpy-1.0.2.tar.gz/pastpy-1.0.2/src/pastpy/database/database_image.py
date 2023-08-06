from abc import ABC, abstractproperty


class DatabaseImage(ABC):
    @abstractproperty
    def full_size_url(self):
        """
        @return full size URL of the image
        @rtype str or None
        """
        pass

    @abstractproperty
    def thumbnail_url(self):
        """
        @return thumbnail URL of the image
        @rtype str or None
        """
        pass

    @abstractproperty
    def title(self):
        """
        @return title of the image
        @rtype str or None
        """
        pass
