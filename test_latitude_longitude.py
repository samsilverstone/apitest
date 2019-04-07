from apitest.tests.test_config import BaseTest
import json


class TestLatLon(BaseTest):

    def test_with_correct_request(self):
        """
        tests the '/get_using_postgres' GET request with correct parameters
        """
        data = {
            "Latitude": "28.6333",
	        "Longitude": "77.2167"
        }
        response = self.client.get("/latitude_longitude", content_type="application/json", data=json.dumps(data))
        self.assertEqual( response.status_code, 200 )

    def test_with_wrong_request(self):
        data = {

        }
        response = self.client.get("/latitude_longitude",content_type="application/json",data=json.dumps(data))
        self.assertEqual(response.status_code, 404)

    def test_right_latitude_format1(self):
        """
        Tests the '/get_using_postgres' GET request
        Uses wrong format for the Latitude which is supposed to be 'xxx.xxx' where x is an integer
        """

        data = {
            "Latitude": "28",
            "Longitude": "77.2167"
        }

        response = self.client.get("/latitude_longitude", content_type="application/json", data=json.dumps(data))
        self.assertEqual( response.status_code, 200 )


    def test_wrong_latitude_format1(self):
        data = {
            "Latitude": "28.232a",
            "Longitude": "67.3423"
        }
        response = self.client.get("/latitude_longitude", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong latitude entered", response.data)
        self.assertEqual(response.status_code, 404)

    def test_wrong_latitude_format2(self):
        data = {
            "Latitude": "28.232.6767",
            "Longitude": "67.3423"
        }
        response = self.client.get("/latitude_longitude", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong latitude entered", response.data)
        self.assertEqual(response.status_code, 404)

    def test_right_longitude_format1(self):
        """
        Tests the '/get_using_postgres' GET request
        Uses wrong format for the Longitude which is supposed to be 'xxx.xxx' where x is an integer
        """

        data = {
            "Latitude": "28.6333",
            "Longitude": "77"
        }

        response = self.client.get("/latitude_longitude", content_type="application/json", data=json.dumps(data))
        self.assertEqual( response.status_code, 200 )
