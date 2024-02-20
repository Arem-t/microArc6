import requests
import unittest

delivery_url = 'http://127.0.0.1:8000'
add_delivery_url = f'{delivery_url}/delivery'
get_delivery_url = f'{delivery_url}/delivery'

delivery = {"id": 2,
            "message": "Processing delivery for order 2", 
            "delivery_id": 1}

class TestComponent(unittest.TestCase):

    def test_create_delivery(self):
        res = requests.post(f"{add_delivery_url}/2", json=delivery)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"message": "Processing delivery for order 2", "delivery_id": 3})
    
    def test_get_data_of_delivery(self):
        res = requests.get(f"{get_delivery_url}/2").json()
        self.assertEqual(res["order_id"], 2)
        self.assertEqual(res["status"], "processed")
    
    def test_fetch_delivery(self):
        res = requests.get(get_delivery_url)
        self.assertTrue(res != "Delivery not found!")

if __name__ == '__main__':
    unittest.main()
