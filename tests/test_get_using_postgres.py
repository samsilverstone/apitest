from apitest.tests.test_config import BaseTest
import json 


class TestGetPostgres(BaseTest):

    def test_with_correct_request(self):
        """
        tests the '/get_using_postgres' GET request with correct parameters
        """
        data = {
            "Latitude": "28.6333",
	        "Longitude": "77.2167",
            "Value": 5
        }
        response = self.client.get("/get_using_postgres", content_type="application/json", data=json.dumps(data))
        self.assertEqual( response.status_code, 200 )

    def test_with_wrong_request(self):
        data = {

        }
        response = self.client.get("/get_using_postgres",content_type="application/json",data=json.dumps(data))
        self.assertEqual(response.status_code, 404)

    def test_right_latitude_format1(self):
        """
        Tests the '/get_using_postgres' GET request
        Uses wrong format for the Latitude which is supposed to be 'xxx.xxx' where x is an integer
        """

        data = {
            "Latitude": "28",
            "Longitude": "77.2167",
            "Value": 5
        }

        response = self.client.get("/get_using_postgres", content_type="application/json", data=json.dumps(data))
        self.assertEqual( response.status_code, 200 )


    def test_wrong_latitude_format1(self):
        data = {
            "Latitude": "28.232a",
            "Longitude": "67.3423",
            "Value": 5
        }
        response = self.client.get("/get_using_postgres", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong latitude entered", response.data)
        self.assertEqual(response.status_code, 404)

    def test_wrong_latitude_format2(self):
        data = {
            "Latitude": "28.232.6767",
            "Longitude": "67.3423",
            "Value": 5
        }
        response = self.client.get("/get_using_postgres", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong latitude entered", response.data)
        self.assertEqual(response.status_code, 404)

    def test_right_longitude_format1(self):
        """
        Tests the '/get_using_postgres' GET request
        Uses wrong format for the Longitude which is supposed to be 'xxx.xxx' where x is an integer
        """

        data = {
            "Latitude": "28.6333",
            "Longitude": "77",
            "Value": 5
        }

        response = self.client.get("/get_using_postgres", content_type="application/json", data=json.dumps(data))
        self.assertEqual( response.status_code, 200 )

    def test_wrong_longitude_format1(self):
        """
        Tests the '/get_using_postgres' GET request
        Uses wrong format for the Longitude which is supposed to be 'xxx.xxx' where x is an integer
        """

        data = {
            "Latitude": "28.4345",
            "Longitude": "77.3a5345",
            "Value": 5
        }

        response = self.client.get("/get_using_postgres", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong longitude entered", response.data)
        self.assertEqual(response.status_code, 404)


    def test_wrong_longitude_format2(self):

        data={
            "Latitude": "28.4345",
            "Longitude": "77.3534.543",
            "Value": 5
        }
        response = self.client.get("/get_using_postgres", content_type="application/json", data=json.dumps(data))

        self.assertIn( b"Wrong longitude entered", response.data )
        self.assertEqual( response.status_code, 404 )

    def test_wrong_value1(self):

        data = {
            "Latitude": "28.4345",
            "Longitude": "77.3534",
            "Value": "5.6.3"
        }

        response = self.client.get("/get_using_postgres", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong value entered", response.data)
        self.assertEqual(response.status_code, 404)

    def test_wrong_value2(self):

        data = {
            "Latitude": "28.4345",
            "Longitude": "77.3534",
            "Value": "5a.6"
        }

        response = self.client.get("/get_using_postgres", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong value entered", response.data)
        self.assertEqual(response.status_code, 404)

    def test_wrong_value3(self):
        data = {
            "Latitude": "28.6333",
            "Longitude": "77.3453",
            "Value": ""
        }

        response = self.client.get("/get_using_postgres", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong value entered", response.data)
        self.assertEqual(response.status_code, 404)