# coding: utf-8

"""
    SendinBlue API

    SendinBlue provide a RESTFul API that can be used with any languages. With this API, you will be able to :   - Manage your campaigns and get the statistics   - Manage your contacts   - Send transactional Emails and SMS   - and much more...  You can download our wrappers at https://github.com/orgs/sendinblue  **Possible responses**   | Code | Message |   | :-------------: | ------------- |   | 200  | OK. Successful Request  |   | 201  | OK. Successful Creation |   | 202  | OK. Request accepted |   | 204  | OK. Successful Update/Deletion  |   | 400  | Error. Bad Request  |   | 401  | Error. Authentication Needed  |   | 402  | Error. Not enough credit, plan upgrade needed  |   | 403  | Error. Permission denied  |   | 404  | Error. Object does not exist |   | 405  | Error. Method not allowed  |   # noqa: E501

    OpenAPI spec version: 3.0.0
    Contact: contact@sendinblue.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import sib_api_v3_sdk
from sib_api_v3_sdk.api.smtp_api import SMTPApi  # noqa: E501
from sib_api_v3_sdk.rest import ApiException


class TestSMTPApi(unittest.TestCase):
    """SMTPApi unit test stubs"""

    def setUp(self):
        self.api = sib_api_v3_sdk.api.smtp_api.SMTPApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_smtp_template(self):
        """Test case for create_smtp_template

        Create an smtp template  # noqa: E501
        """
        pass

    def test_delete_hardbounces(self):
        """Test case for delete_hardbounces

        Delete hardbounces  # noqa: E501
        """
        pass

    def test_delete_smtp_template(self):
        """Test case for delete_smtp_template

        Delete an inactive smtp template  # noqa: E501
        """
        pass

    def test_get_aggregated_smtp_report(self):
        """Test case for get_aggregated_smtp_report

        Get your SMTP activity aggregated over a period of time  # noqa: E501
        """
        pass

    def test_get_email_event_report(self):
        """Test case for get_email_event_report

        Get all your SMTP activity (unaggregated events)  # noqa: E501
        """
        pass

    def test_get_smtp_report(self):
        """Test case for get_smtp_report

        Get your SMTP activity aggregated per day  # noqa: E501
        """
        pass

    def test_get_smtp_template(self):
        """Test case for get_smtp_template

        Returns the template informations  # noqa: E501
        """
        pass

    def test_get_smtp_templates(self):
        """Test case for get_smtp_templates

        Get the list of SMTP templates  # noqa: E501
        """
        pass

    def test_send_template(self):
        """Test case for send_template

        Send a template  # noqa: E501
        """
        pass

    def test_send_test_template(self):
        """Test case for send_test_template

        Send a template to your test list  # noqa: E501
        """
        pass

    def test_send_transac_email(self):
        """Test case for send_transac_email

        Send a transactional email  # noqa: E501
        """
        pass

    def test_update_smtp_template(self):
        """Test case for update_smtp_template

        Updates an smtp templates  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
