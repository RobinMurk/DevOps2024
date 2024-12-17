# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.bodytemplate import Bodytemplate  # noqa: E501
from swagger_server.models.humidity import Humidity  # noqa: E501
from swagger_server.test import BaseTestCase


class TestHumidityController(BaseTestCase):
    """HumidityController integration test stubs"""

    def test_add_humidity_measurement(self):
        """Test case for add_humidity_measurement

        Add a new measurement (Avg humidity for the day) to the database
        """
        body = Bodytemplate()
        response = self.client.open(
            '/humidity',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_hum_bytimeframe(self):
        """Test case for delete_hum_bytimeframe

        Delete humidity data for a given day
        """
        response = self.client.open(
            '/humidity/{timeframe}'.format(timeframe='timeframe_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_humidity_bytimeframe(self):
        """Test case for get_humidity_bytimeframe

        Get humidity data  by timeframe(previous 1hr,6hr,1day,1week)
        """
        response = self.client.open(
            '/humidity/{timeframe}'.format(timeframe='timeframe_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_avg_humidity(self):
        """Test case for update_avg_humidity

        Update an existing average humidity value for the day
        """
        body = Bodytemplate()
        response = self.client.open(
            '/humidity',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
