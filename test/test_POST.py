import unittest
from unittest import mock
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
from main import MainWindow
import requests
import json


class TestMainWindowGetRequest(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.window = MainWindow()
        self.window.show()
        # Debug: Verify self.model exists
        if not hasattr(self.window, 'model'):
            raise AttributeError("MainWindow.model is not initialized")

    def setUp(self):
        self.window = MainWindow()
        self.window.show()

    def tearDown(self):
        self.window.close()

    def test_get_request_with_connection_error(self):
        url = "https://invalid-url.com"
        self.window.ui.lineEdit.setText(url)

        with mock.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error")):
            QTest.mouseClick(self.window.ui.push_GET_request, Qt.LeftButton)

            model = self.window.model
            self.assertTrue(any("Error: Failed to make GET request" in item for item in model.stringList()))

    def test_get_request_to_json_placeholder(self):
        url = "https://jsonplaceholder.typicode.com/posts"
        self.window.ui.lineEdit.setText(url)

        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'[{"id": 1, "title": "Test Post"}]'

        with mock.patch("requests.get", return_value=mock_response):
            QTest.mouseClick(self.window.ui.push_GET_request, Qt.LeftButton)

            model = self.window.model
            expected_json = json.dumps([{"id": 1, "title": "Test Post"}], indent=4, ensure_ascii=False)
            self.assertTrue(any(expected_json in item for item in model.stringList()))




if __name__ == "__main__":
    unittest.main()