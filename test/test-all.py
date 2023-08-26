import requests
import unittest


class Test(unittest.TestCase):
    base_url = "http://localhost:5000"

    def test_ping(self):
        content = requests.get(f"{self.base_url}/ping/").text
        self.assertEqual(content, "PONG")

    def test_split_selected(self):
        url = f"{self.base_url}/pdf/split/"

        payload = {
            "mode": "selected",
            "selection": "1,3-5;10-14;3-5,8,9",
        }
        file = open("./raw/sample_1MB.pdf", "rb")
        files = [
            (
                "file",
                (
                    "sample.pdf",
                    file,
                    "application/pdf",
                ),
            )
        ]
        headers = {}

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
            files=files,
        )

        file.close()
        self.assertTrue(len(response.content) > 0)


if __name__ == "__main__":
    unittest.main()
