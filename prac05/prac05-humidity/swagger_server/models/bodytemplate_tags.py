# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class BodytemplateTags(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, station: str=None, _date: str=None):  # noqa: E501
        """BodytemplateTags - a model defined in Swagger

        :param station: The station of this BodytemplateTags.  # noqa: E501
        :type station: str
        :param _date: The _date of this BodytemplateTags.  # noqa: E501
        :type _date: str
        """
        self.swagger_types = {
            'station': str,
            '_date': str
        }

        self.attribute_map = {
            'station': 'station',
            '_date': 'date'
        }
        self._station = station
        self.__date = _date

    @classmethod
    def from_dict(cls, dikt) -> 'BodytemplateTags':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The bodytemplate_tags of this BodytemplateTags.  # noqa: E501
        :rtype: BodytemplateTags
        """
        return util.deserialize_model(dikt, cls)

    @property
    def station(self) -> str:
        """Gets the station of this BodytemplateTags.


        :return: The station of this BodytemplateTags.
        :rtype: str
        """
        return self._station

    @station.setter
    def station(self, station: str):
        """Sets the station of this BodytemplateTags.


        :param station: The station of this BodytemplateTags.
        :type station: str
        """

        self._station = station

    @property
    def _date(self) -> str:
        """Gets the _date of this BodytemplateTags.


        :return: The _date of this BodytemplateTags.
        :rtype: str
        """
        return self.__date

    @_date.setter
    def _date(self, _date: str):
        """Sets the _date of this BodytemplateTags.


        :param _date: The _date of this BodytemplateTags.
        :type _date: str
        """

        self.__date = _date
