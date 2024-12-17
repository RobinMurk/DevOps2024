import unittest 
import sys
import pandas as pd
sys.path.append('./') # path to flask-app modules
from flask_app.app import *

class test_analyze_app(unittest.TestCase):
    def setUp(self):       
        self.STUD_INFLUX_HOST_ADD=os.getenv('STUD_INFLUX_HOST_ADD')
        self.STUD_INFLUX_ORG=os.getenv('STUD_INFLUX_ORG')
        self.STUD_INFLUX_TOKEN=os.getenv('STUD_INFLUX_TOKEN')
        self.client = InfluxDBClient(url=STUD_INFLUX_HOST_ADD, token=STUD_INFLUX_TOKEN, org=STUD_INFLUX_ORG, debug=True)
        self.query= '''
                    from(bucket: "weather_data")
                    |> range(start:-60d, stop: now())
                    |> filter(fn: (r) => r._measurement == "weather")
                    |> filter(fn: (r) => r._field == "temp")
                    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''
        self.test_df = get_data(self.client,self.query)
        # print(df.empty)
    def test_get_data(self):
        self.assertFalse(get_data(self.client, self.query).empty) # we are expecting some data
    def test_convert_time(self):
        self.assertFalse(convert_time(self.test_df).empty)
    def test_is_df_empty(self):
        self.assertFalse(is_df_empty(self.test_df))

if __name__ == '__main__':
    unittest.main()
