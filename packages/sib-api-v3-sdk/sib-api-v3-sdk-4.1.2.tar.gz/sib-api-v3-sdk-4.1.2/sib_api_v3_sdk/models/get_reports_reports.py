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


class GetReportsReports(object):
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
        'date': 'date',
        'requests': 'int',
        'delivered': 'int',
        'hard_bounces': 'int',
        'soft_bounces': 'int',
        'clicks': 'int',
        'unique_clicks': 'int',
        'opens': 'int',
        'unique_opens': 'int',
        'spam_reports': 'int',
        'blocked': 'int',
        'invalid': 'int',
        'unsubscribed': 'int'
    }

    attribute_map = {
        'date': 'date',
        'requests': 'requests',
        'delivered': 'delivered',
        'hard_bounces': 'hardBounces',
        'soft_bounces': 'softBounces',
        'clicks': 'clicks',
        'unique_clicks': 'uniqueClicks',
        'opens': 'opens',
        'unique_opens': 'uniqueOpens',
        'spam_reports': 'spamReports',
        'blocked': 'blocked',
        'invalid': 'invalid',
        'unsubscribed': 'unsubscribed'
    }

    def __init__(self, date=None, requests=None, delivered=None, hard_bounces=None, soft_bounces=None, clicks=None, unique_clicks=None, opens=None, unique_opens=None, spam_reports=None, blocked=None, invalid=None, unsubscribed=None):  # noqa: E501
        """GetReportsReports - a model defined in Swagger"""  # noqa: E501

        self._date = None
        self._requests = None
        self._delivered = None
        self._hard_bounces = None
        self._soft_bounces = None
        self._clicks = None
        self._unique_clicks = None
        self._opens = None
        self._unique_opens = None
        self._spam_reports = None
        self._blocked = None
        self._invalid = None
        self._unsubscribed = None
        self.discriminator = None

        self.date = date
        self.requests = requests
        self.delivered = delivered
        self.hard_bounces = hard_bounces
        self.soft_bounces = soft_bounces
        self.clicks = clicks
        self.unique_clicks = unique_clicks
        self.opens = opens
        self.unique_opens = unique_opens
        self.spam_reports = spam_reports
        self.blocked = blocked
        self.invalid = invalid
        self.unsubscribed = unsubscribed

    @property
    def date(self):
        """Gets the date of this GetReportsReports.  # noqa: E501

        Date of the statistics  # noqa: E501

        :return: The date of this GetReportsReports.  # noqa: E501
        :rtype: date
        """
        return self._date

    @date.setter
    def date(self, date):
        """Sets the date of this GetReportsReports.

        Date of the statistics  # noqa: E501

        :param date: The date of this GetReportsReports.  # noqa: E501
        :type: date
        """
        if date is None:
            raise ValueError("Invalid value for `date`, must not be `None`")  # noqa: E501

        self._date = date

    @property
    def requests(self):
        """Gets the requests of this GetReportsReports.  # noqa: E501

        Number of requests for the date  # noqa: E501

        :return: The requests of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._requests

    @requests.setter
    def requests(self, requests):
        """Sets the requests of this GetReportsReports.

        Number of requests for the date  # noqa: E501

        :param requests: The requests of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if requests is None:
            raise ValueError("Invalid value for `requests`, must not be `None`")  # noqa: E501

        self._requests = requests

    @property
    def delivered(self):
        """Gets the delivered of this GetReportsReports.  # noqa: E501

        Number of delivered emails for the date  # noqa: E501

        :return: The delivered of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._delivered

    @delivered.setter
    def delivered(self, delivered):
        """Sets the delivered of this GetReportsReports.

        Number of delivered emails for the date  # noqa: E501

        :param delivered: The delivered of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if delivered is None:
            raise ValueError("Invalid value for `delivered`, must not be `None`")  # noqa: E501

        self._delivered = delivered

    @property
    def hard_bounces(self):
        """Gets the hard_bounces of this GetReportsReports.  # noqa: E501

        Number of hardbounces for the date  # noqa: E501

        :return: The hard_bounces of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._hard_bounces

    @hard_bounces.setter
    def hard_bounces(self, hard_bounces):
        """Sets the hard_bounces of this GetReportsReports.

        Number of hardbounces for the date  # noqa: E501

        :param hard_bounces: The hard_bounces of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if hard_bounces is None:
            raise ValueError("Invalid value for `hard_bounces`, must not be `None`")  # noqa: E501

        self._hard_bounces = hard_bounces

    @property
    def soft_bounces(self):
        """Gets the soft_bounces of this GetReportsReports.  # noqa: E501

        Number of softbounces for the date  # noqa: E501

        :return: The soft_bounces of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._soft_bounces

    @soft_bounces.setter
    def soft_bounces(self, soft_bounces):
        """Sets the soft_bounces of this GetReportsReports.

        Number of softbounces for the date  # noqa: E501

        :param soft_bounces: The soft_bounces of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if soft_bounces is None:
            raise ValueError("Invalid value for `soft_bounces`, must not be `None`")  # noqa: E501

        self._soft_bounces = soft_bounces

    @property
    def clicks(self):
        """Gets the clicks of this GetReportsReports.  # noqa: E501

        Number of clicks for the date  # noqa: E501

        :return: The clicks of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._clicks

    @clicks.setter
    def clicks(self, clicks):
        """Sets the clicks of this GetReportsReports.

        Number of clicks for the date  # noqa: E501

        :param clicks: The clicks of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if clicks is None:
            raise ValueError("Invalid value for `clicks`, must not be `None`")  # noqa: E501

        self._clicks = clicks

    @property
    def unique_clicks(self):
        """Gets the unique_clicks of this GetReportsReports.  # noqa: E501

        Number of unique clicks for the date  # noqa: E501

        :return: The unique_clicks of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._unique_clicks

    @unique_clicks.setter
    def unique_clicks(self, unique_clicks):
        """Sets the unique_clicks of this GetReportsReports.

        Number of unique clicks for the date  # noqa: E501

        :param unique_clicks: The unique_clicks of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if unique_clicks is None:
            raise ValueError("Invalid value for `unique_clicks`, must not be `None`")  # noqa: E501

        self._unique_clicks = unique_clicks

    @property
    def opens(self):
        """Gets the opens of this GetReportsReports.  # noqa: E501

        Number of openings for the date  # noqa: E501

        :return: The opens of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._opens

    @opens.setter
    def opens(self, opens):
        """Sets the opens of this GetReportsReports.

        Number of openings for the date  # noqa: E501

        :param opens: The opens of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if opens is None:
            raise ValueError("Invalid value for `opens`, must not be `None`")  # noqa: E501

        self._opens = opens

    @property
    def unique_opens(self):
        """Gets the unique_opens of this GetReportsReports.  # noqa: E501

        Number of unique openings for the date  # noqa: E501

        :return: The unique_opens of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._unique_opens

    @unique_opens.setter
    def unique_opens(self, unique_opens):
        """Sets the unique_opens of this GetReportsReports.

        Number of unique openings for the date  # noqa: E501

        :param unique_opens: The unique_opens of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if unique_opens is None:
            raise ValueError("Invalid value for `unique_opens`, must not be `None`")  # noqa: E501

        self._unique_opens = unique_opens

    @property
    def spam_reports(self):
        """Gets the spam_reports of this GetReportsReports.  # noqa: E501

        Number of complaints (spam reports) for the date  # noqa: E501

        :return: The spam_reports of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._spam_reports

    @spam_reports.setter
    def spam_reports(self, spam_reports):
        """Sets the spam_reports of this GetReportsReports.

        Number of complaints (spam reports) for the date  # noqa: E501

        :param spam_reports: The spam_reports of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if spam_reports is None:
            raise ValueError("Invalid value for `spam_reports`, must not be `None`")  # noqa: E501

        self._spam_reports = spam_reports

    @property
    def blocked(self):
        """Gets the blocked of this GetReportsReports.  # noqa: E501

        Number of blocked emails for the date  # noqa: E501

        :return: The blocked of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._blocked

    @blocked.setter
    def blocked(self, blocked):
        """Sets the blocked of this GetReportsReports.

        Number of blocked emails for the date  # noqa: E501

        :param blocked: The blocked of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if blocked is None:
            raise ValueError("Invalid value for `blocked`, must not be `None`")  # noqa: E501

        self._blocked = blocked

    @property
    def invalid(self):
        """Gets the invalid of this GetReportsReports.  # noqa: E501

        Number of invalid emails for the date  # noqa: E501

        :return: The invalid of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._invalid

    @invalid.setter
    def invalid(self, invalid):
        """Sets the invalid of this GetReportsReports.

        Number of invalid emails for the date  # noqa: E501

        :param invalid: The invalid of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if invalid is None:
            raise ValueError("Invalid value for `invalid`, must not be `None`")  # noqa: E501

        self._invalid = invalid

    @property
    def unsubscribed(self):
        """Gets the unsubscribed of this GetReportsReports.  # noqa: E501

        Number of unsubscribed emails for the date  # noqa: E501

        :return: The unsubscribed of this GetReportsReports.  # noqa: E501
        :rtype: int
        """
        return self._unsubscribed

    @unsubscribed.setter
    def unsubscribed(self, unsubscribed):
        """Sets the unsubscribed of this GetReportsReports.

        Number of unsubscribed emails for the date  # noqa: E501

        :param unsubscribed: The unsubscribed of this GetReportsReports.  # noqa: E501
        :type: int
        """
        if unsubscribed is None:
            raise ValueError("Invalid value for `unsubscribed`, must not be `None`")  # noqa: E501

        self._unsubscribed = unsubscribed

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
        if not isinstance(other, GetReportsReports):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
