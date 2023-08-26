import requests
import unittest


class Test(unittest.TestCase):
    base_url = "http://localhost:5000"

    def test_ping(self):
        content = requests.get(f"{self.base_url}/ping/").text
        self.assertEqual(content, "PONG")


if __name__ == "__main__":
    unittest.main()
