from apitest.tests.test_config import BaseTest
import json 


class TestPostLocation(BaseTest):

    def test_post_correct_parameters(self):

        data = {
            "Latitude": "28.6333",
            "Longitude": "77.2167",
            "pin": "IN/110080",
            "address": "Khanpur",
            "city": "New Delhi",
            "accuracy": "4"
            }
        
        response = self.client.post("/post_location", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_wrong_parameters1(self):

        data = {
            "Latitude": "28.6a333",
            "Longitude": "77.2167",
            "pin": "IN/110080",
            "address": "Khanpur",
            "city": "New Delhi",
            "accuracy": "4"
        }
        response = self.client.post("/post_location", data=json.dumps(data), content_type="application/json")
        self.assertIn(b"Wrong Latitude entered", response.data)
        self.assertEqual(response.status_code, 404)

    def test_wrong_parameters2(self):

        data = {
            "Latitude": "28.6333",
            "Longitude": "7g7.2167",
            "pin": "IN/110080",
            "address": "Khanpur",
            "city": "New Delhi",
            "accuracy": "4"
        }
        response = self.client.post("/post_location", data=json.dumps(data), content_type="application/json")
        self.assertIn(b"Wrong longitude entered",response.data)
        self.assertEqual(response.status_code, 404)

    def test_wrong_parameters3(self):

        data = {
            "Latitude": "28.6333",
            "Longitude": "77.2167",
            "pin": "IF/110080",
            "address": "Khanpur",
            "city": "New Delhi",
            "accuracy": "4"
        }
        response = self.client.post("/post_location", data=json.dumps(data), content_type="application/json")
        self.assertIn(b"Wrong Pincode entered",response.data)
        self.assertEqual(response.status_code, 404)

    def test_wrong_parameters4(self):

        data = {
            "Latitude": "28.6333",
            "Longitude": "77.2167",
            "pin": "IN/110080",
            "address": "Khanpur",
            "city": "New Delhi",
            "accuracy": "a"
        }
        response = self.client.post("/post_location", data=json.dumps(data), content_type="application/json")
        self.assertIn(b"Wrong accuracy entered", response.data)
        self.assertEqual(response.status_code, 404)

