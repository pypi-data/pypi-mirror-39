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


class PostSendSmsTestFailed(object):
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
        'code': 'int',
        'message': 'str',
        'unexisting_sms': 'list[str]',
        'without_list_sms': 'list[str]'
    }

    attribute_map = {
        'code': 'code',
        'message': 'message',
        'unexisting_sms': 'unexistingSms',
        'without_list_sms': 'withoutListSms'
    }

    def __init__(self, code=None, message=None, unexisting_sms=None, without_list_sms=None):  # noqa: E501
        """PostSendSmsTestFailed - a model defined in Swagger"""  # noqa: E501

        self._code = None
        self._message = None
        self._unexisting_sms = None
        self._without_list_sms = None
        self.discriminator = None

        self.code = code
        self.message = message
        if unexisting_sms is not None:
            self.unexisting_sms = unexisting_sms
        if without_list_sms is not None:
            self.without_list_sms = without_list_sms

    @property
    def code(self):
        """Gets the code of this PostSendSmsTestFailed.  # noqa: E501

        Response code  # noqa: E501

        :return: The code of this PostSendSmsTestFailed.  # noqa: E501
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this PostSendSmsTestFailed.

        Response code  # noqa: E501

        :param code: The code of this PostSendSmsTestFailed.  # noqa: E501
        :type: int
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501

        self._code = code

    @property
    def message(self):
        """Gets the message of this PostSendSmsTestFailed.  # noqa: E501

        Response message  # noqa: E501

        :return: The message of this PostSendSmsTestFailed.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this PostSendSmsTestFailed.

        Response message  # noqa: E501

        :param message: The message of this PostSendSmsTestFailed.  # noqa: E501
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

    @property
    def unexisting_sms(self):
        """Gets the unexisting_sms of this PostSendSmsTestFailed.  # noqa: E501


        :return: The unexisting_sms of this PostSendSmsTestFailed.  # noqa: E501
        :rtype: list[str]
        """
        return self._unexisting_sms

    @unexisting_sms.setter
    def unexisting_sms(self, unexisting_sms):
        """Sets the unexisting_sms of this PostSendSmsTestFailed.


        :param unexisting_sms: The unexisting_sms of this PostSendSmsTestFailed.  # noqa: E501
        :type: list[str]
        """

        self._unexisting_sms = unexisting_sms

    @property
    def without_list_sms(self):
        """Gets the without_list_sms of this PostSendSmsTestFailed.  # noqa: E501


        :return: The without_list_sms of this PostSendSmsTestFailed.  # noqa: E501
        :rtype: list[str]
        """
        return self._without_list_sms

    @without_list_sms.setter
    def without_list_sms(self, without_list_sms):
        """Sets the without_list_sms of this PostSendSmsTestFailed.


        :param without_list_sms: The without_list_sms of this PostSendSmsTestFailed.  # noqa: E501
        :type: list[str]
        """

        self._without_list_sms = without_list_sms

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
        if not isinstance(other, PostSendSmsTestFailed):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
