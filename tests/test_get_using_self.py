from apitest.tests.test_config import BaseTest
import json

class TestCase(BaseTest):
    
    def test_with_correct_request(self):
        data = {
            "Latitude": "28.6333", 
            "Longitude": "77.2167",
            "Value": 5
        }
        response = self.client.get("/get_using_self", content_type="application/json", data=json.dumps(data))
        self.assertEqual(response.status_code, 200)


    def test_right_latitude_format1(self):
        # tests for when the format entered for latitude and longitude is wrong 
        # the latitude and longitudes are supposed to be in the format "xx.xxxx" where "x" is an integer
        # we will keep the latitude in the format "xx" where x is an integer and see what happens. We expect a 404 response

        data = {
            "Latitude": "28",
            "Longitude": "77.2167",
            "Value": 5
        }

        response = self.client.get("/get_using_self", content_type="application/json", data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

    def test_wrong_latitude_format1(self):

        data={
            "Latitude": "28.a342",
            "Longitude": "67.2342",
            "Value":5
        }
        response = self.client.get("/get_using_self", content_type="application/json",data=json.dumps(data))
        self.assertIn(b"Wrong latitude entered", response.data)
        self.assertEqual(response.status_code,404)

    def test_wrong_latitude_format2(self):
        data = {
            "Latitude": "28.232.3453",
            "Longitude": "67.234",
            "Value":5
        }
        response = self.client.get("/get_using_self", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong latitude entered", response.data)
        self.assertEqual(response.status_code, 404)

    def test_right_longitude_format1(self):
        # tests for when the format entered for latitude and longitude is wrong 
        # the latitude and longitudes are supposed to be in the format "xx.xxxx" where "x" is an integer
        # we will keep the longitude in the format "xx" where x is an integer and see what happens. We expect a 404 response

        data = {
            "Latitude": "28.6333",
            "Longitude": "77",
            "Value": 5
        }

        response = self.client.get("/get_using_self", content_type="application/json", data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

    def test_wrong_longitude_format1(self):
        # tests for when the format entered for latitude and longitude is wrong
        # the latitude and longitudes are supposed to be in the format "xx.xxxx" where "x" is an integer
        # we will keep the longitude in the format "xx" where x is an integer and see what happens. We expect a 404 response

        data = {
            "Latitude": "28.345",
            "Longitude": "77.345.3343",
            "Value":5
        }

        response = self.client.get("/get_using_self", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong longitude entered", response.data)
        self.assertEqual(response.status_code, 404)

    def test_wrong_longitude_format2(self):
        # tests for when the format entered for latitude and longitude is wrong
        # the latitude and longitudes are supposed to be in the format "xx.xxxx" where "x" is an integer
        # we will keep the longitude in the format "xx" where x is an integer and see what happens. We expect a 404 response

        data = {
            "Latitude": "28.6333",
            "Longitude": "77.a3453",
            "Value": 5
        }

        response = self.client.get("/get_using_self", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong longitude entered", response.data)
        self.assertEqual(response.status_code, 404)

    def test_wrong_value1(self):
         data = {
             "Latitude": "28.6333",
             "Longitude": "77.3453",
             "Value": "5.54.23"
         }

         response = self.client.get("/get_using_self", content_type="application/json", data=json.dumps(data))
         self.assertIn(b"Wrong value entered", response.data)
         self.assertEqual(response.status_code, 404)

    def test_wrong_value2(self):
        data = {
            "Latitude": "28.6333",
            "Longitude": "77.3453",
            "Value": "5.a23"
        }

        response = self.client.get("/get_using_self", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong value entered", response.data)
        self.assertEqual(response.status_code, 404)

    def test_wrong_value3(self):
        data = {
            "Latitude": "28.6333",
            "Longitude": "77.3453",
            "Value": ""
        }

        response = self.client.get("/get_using_self", content_type="application/json", data=json.dumps(data))
        self.assertIn(b"Wrong value entered", response.data)
        self.assertEqual(response.status_code, 404)



