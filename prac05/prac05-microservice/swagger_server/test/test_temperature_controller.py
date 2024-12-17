# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.bodytemplate import Bodytemplate  # noqa: E501
from swagger_server.models.temperature import Temperature  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTemperatureController(BaseTestCase):
    """TemperatureController integration test stubs"""

    def test_add_measurement(self):
        """Test case for add_measurement

        Add a new measurement (Avg temperature for the day) to the database
        """
        body = Bodytemplate()
        response = self.client.open(
            '/temperature',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_temp_bytimeframe(self):
        """Test case for delete_temp_bytimeframe

        Delete temperature data for a given day
        """
        response = self.client.open(
            '/temperature/{timeframe}'.format(timeframe='timeframe_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_temp_bytimeframe(self):
        """Test case for get_temp_bytimeframe

        Get temperature data  by timeframe(previous 1hr,6hr,1day,1week)
        """
        response = self.client.open(
            '/temperature/{timeframe}'.format(timeframe='timeframe_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_avg_temperature(self):
        """Test case for update_avg_temperature

        Update an existing average temperature value for the day
        """
        body = Bodytemplate()
        response = self.client.open(
            '/temperature',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
