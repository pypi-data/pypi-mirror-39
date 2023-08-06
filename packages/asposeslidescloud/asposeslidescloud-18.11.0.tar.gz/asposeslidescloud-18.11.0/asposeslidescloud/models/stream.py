# coding: utf-8

# -----------------------------------------------------------------------------------
# <copyright company="Aspose">
#   Copyright (c) 2018 Aspose.Slides for Cloud
# </copyright>
# <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# -----------------------------------------------------------------------------------

import pprint
import re  # noqa: F401

import six

from asposeslidescloud.models.marshal_by_ref_object import MarshalByRefObject

class Stream(MarshalByRefObject):


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'can_read': 'bool',
        'can_seek': 'bool',
        'can_timeout': 'bool',
        'can_write': 'bool',
        'length': 'int',
        'position': 'int',
        'read_timeout': 'int',
        'write_timeout': 'int',
        'null': 'Stream'
    }

    attribute_map = {
        'can_read': 'CanRead',
        'can_seek': 'CanSeek',
        'can_timeout': 'CanTimeout',
        'can_write': 'CanWrite',
        'length': 'Length',
        'position': 'Position',
        'read_timeout': 'ReadTimeout',
        'write_timeout': 'WriteTimeout',
        'null': 'Null'
    }

    def __init__(self, can_read=None, can_seek=None, can_timeout=None, can_write=None, length=None, position=None, read_timeout=None, write_timeout=None, null=None):  # noqa: E501
        """Stream - a model defined in Swagger"""  # noqa: E501
        super(Stream, self).__init__()

        self._can_read = None
        self._can_seek = None
        self._can_timeout = None
        self._can_write = None
        self._length = None
        self._position = None
        self._read_timeout = None
        self._write_timeout = None
        self._null = None

        if can_read is not None:
            self.can_read = can_read
        if can_seek is not None:
            self.can_seek = can_seek
        if can_timeout is not None:
            self.can_timeout = can_timeout
        if can_write is not None:
            self.can_write = can_write
        if length is not None:
            self.length = length
        if position is not None:
            self.position = position
        if read_timeout is not None:
            self.read_timeout = read_timeout
        if write_timeout is not None:
            self.write_timeout = write_timeout
        if null is not None:
            self.null = null

    @property
    def can_read(self):
        """Gets the can_read of this Stream.  # noqa: E501


        :return: The can_read of this Stream.  # noqa: E501
        :rtype: bool
        """
        return self._can_read

    @can_read.setter
    def can_read(self, can_read):
        """Sets the can_read of this Stream.


        :param can_read: The can_read of this Stream.  # noqa: E501
        :type: bool
        """

        self._can_read = can_read

    @property
    def can_seek(self):
        """Gets the can_seek of this Stream.  # noqa: E501


        :return: The can_seek of this Stream.  # noqa: E501
        :rtype: bool
        """
        return self._can_seek

    @can_seek.setter
    def can_seek(self, can_seek):
        """Sets the can_seek of this Stream.


        :param can_seek: The can_seek of this Stream.  # noqa: E501
        :type: bool
        """

        self._can_seek = can_seek

    @property
    def can_timeout(self):
        """Gets the can_timeout of this Stream.  # noqa: E501


        :return: The can_timeout of this Stream.  # noqa: E501
        :rtype: bool
        """
        return self._can_timeout

    @can_timeout.setter
    def can_timeout(self, can_timeout):
        """Sets the can_timeout of this Stream.


        :param can_timeout: The can_timeout of this Stream.  # noqa: E501
        :type: bool
        """

        self._can_timeout = can_timeout

    @property
    def can_write(self):
        """Gets the can_write of this Stream.  # noqa: E501


        :return: The can_write of this Stream.  # noqa: E501
        :rtype: bool
        """
        return self._can_write

    @can_write.setter
    def can_write(self, can_write):
        """Sets the can_write of this Stream.


        :param can_write: The can_write of this Stream.  # noqa: E501
        :type: bool
        """

        self._can_write = can_write

    @property
    def length(self):
        """Gets the length of this Stream.  # noqa: E501


        :return: The length of this Stream.  # noqa: E501
        :rtype: int
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this Stream.


        :param length: The length of this Stream.  # noqa: E501
        :type: int
        """

        self._length = length

    @property
    def position(self):
        """Gets the position of this Stream.  # noqa: E501


        :return: The position of this Stream.  # noqa: E501
        :rtype: int
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this Stream.


        :param position: The position of this Stream.  # noqa: E501
        :type: int
        """

        self._position = position

    @property
    def read_timeout(self):
        """Gets the read_timeout of this Stream.  # noqa: E501


        :return: The read_timeout of this Stream.  # noqa: E501
        :rtype: int
        """
        return self._read_timeout

    @read_timeout.setter
    def read_timeout(self, read_timeout):
        """Sets the read_timeout of this Stream.


        :param read_timeout: The read_timeout of this Stream.  # noqa: E501
        :type: int
        """

        self._read_timeout = read_timeout

    @property
    def write_timeout(self):
        """Gets the write_timeout of this Stream.  # noqa: E501


        :return: The write_timeout of this Stream.  # noqa: E501
        :rtype: int
        """
        return self._write_timeout

    @write_timeout.setter
    def write_timeout(self, write_timeout):
        """Sets the write_timeout of this Stream.


        :param write_timeout: The write_timeout of this Stream.  # noqa: E501
        :type: int
        """

        self._write_timeout = write_timeout

    @property
    def null(self):
        """Gets the null of this Stream.  # noqa: E501


        :return: The null of this Stream.  # noqa: E501
        :rtype: Stream
        """
        return self._null

    @null.setter
    def null(self, null):
        """Sets the null of this Stream.


        :param null: The null of this Stream.  # noqa: E501
        :type: Stream
        """

        self._null = null

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Stream):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
