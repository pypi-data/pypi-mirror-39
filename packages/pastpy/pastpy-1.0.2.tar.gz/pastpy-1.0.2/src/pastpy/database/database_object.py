from abc import ABC, abstractproperty


class DatabaseObject(ABC):
    @abstractproperty
    def date(self):
        """
        @return date of the object
        @rtype object or None
        """
        pass

    @abstractproperty
    def description(self):
        """
        @return description of the object
        @rtype str or None
        """
        pass

    @abstractproperty
    def id(self):
        """
        @return id of the object
        @rtype str
        """
        pass

    @abstractproperty
    def impl_attributes(self):
        """
        @return dict of implementation-defined attributes
        @rtype dict where neither keys nor values is None
        """
        pass

    @abstractproperty
    def images(self):
        """
        @return iterable of DatabaseImage instances
        @rtype iterable of DatabaseImage instances
        """
        pass

    @abstractproperty
    def name(self):
        """
        @return name of object
        @rtype str or None
        """
        pass

    @abstractproperty
    def othername(self):
        """
        @return alternative name of object
        @rtype str or None
        """
        pass

    @abstractproperty
    def title(self):
        """
        @return title of object
        @rtype str or None
        """
        pass
