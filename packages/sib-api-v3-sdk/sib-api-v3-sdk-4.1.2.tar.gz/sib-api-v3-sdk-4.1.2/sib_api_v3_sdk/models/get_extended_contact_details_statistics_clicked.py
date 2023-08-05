# coding: utf-8

"""
    SendinBlue API

    SendinBlue provide a RESTFul API that can be used with any languages. With this API, you will be able to :   - Manage your campaigns and get the statistics   - Manage your contacts   - Send transactional Emails and SMS   - and much more...  You can download our wrappers at https://github.com/orgs/sendinblue  **Possible responses**   | Code | Message |   | :-------------: | ------------- |   | 200  | OK. Successful Request  |   | 201  | OK. Successful Creation |   | 202  | OK. Request accepted |   | 204  | OK. Successful Update/Deletion  |   | 400  | Error. Bad Request  |   | 401  | Error. Authentication Needed  |   | 402  | Error. Not enough credit, plan upgrade needed  |   | 403  | Error. Permission denied  |   | 404  | Error. Object does not exist |   | 405  | Error. Method not allowed  |   # noqa: E501

    OpenAPI spec version: 3.0.0
    Contact: contact@sendinblue.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from sib_api_v3_sdk.models.get_extended_contact_details_statistics_links import GetExtendedContactDetailsStatisticsLinks  # noqa: F401,E501


class GetExtendedContactDetailsStatisticsClicked(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'campaign_id': 'int',
        'links': 'list[GetExtendedContactDetailsStatisticsLinks]'
    }

    attribute_map = {
        'campaign_id': 'campaignId',
        'links': 'links'
    }

    def __init__(self, campaign_id=None, links=None):  # noqa: E501
        """GetExtendedContactDetailsStatisticsClicked - a model defined in Swagger"""  # noqa: E501

        self._campaign_id = None
        self._links = None
        self.discriminator = None

        self.campaign_id = campaign_id
        self.links = links

    @property
    def campaign_id(self):
        """Gets the campaign_id of this GetExtendedContactDetailsStatisticsClicked.  # noqa: E501

        ID of the campaign which generated the event  # noqa: E501

        :return: The campaign_id of this GetExtendedContactDetailsStatisticsClicked.  # noqa: E501
        :rtype: int
        """
        return self._campaign_id

    @campaign_id.setter
    def campaign_id(self, campaign_id):
        """Sets the campaign_id of this GetExtendedContactDetailsStatisticsClicked.

        ID of the campaign which generated the event  # noqa: E501

        :param campaign_id: The campaign_id of this GetExtendedContactDetailsStatisticsClicked.  # noqa: E501
        :type: int
        """
        if campaign_id is None:
            raise ValueError("Invalid value for `campaign_id`, must not be `None`")  # noqa: E501

        self._campaign_id = campaign_id

    @property
    def links(self):
        """Gets the links of this GetExtendedContactDetailsStatisticsClicked.  # noqa: E501

        Listing of the clicked links for the campaign  # noqa: E501

        :return: The links of this GetExtendedContactDetailsStatisticsClicked.  # noqa: E501
        :rtype: list[GetExtendedContactDetailsStatisticsLinks]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this GetExtendedContactDetailsStatisticsClicked.

        Listing of the clicked links for the campaign  # noqa: E501

        :param links: The links of this GetExtendedContactDetailsStatisticsClicked.  # noqa: E501
        :type: list[GetExtendedContactDetailsStatisticsLinks]
        """
        if links is None:
            raise ValueError("Invalid value for `links`, must not be `None`")  # noqa: E501

        self._links = links

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
        if not isinstance(other, GetExtendedContactDetailsStatisticsClicked):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
