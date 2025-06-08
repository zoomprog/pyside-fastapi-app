import sys
import unittest
from unittest import mock
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
from main import MainWindow
import requests


class TestMainWindowGetRequest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def setUp(self):
        self.window = MainWindow()
        self.window.show()


    def tearDown(self):
        self.window.close()

    def test_get_request_with_empty_url(self):
        self.window.ui.lineEdit.setText("")  # Устанавливаем пустой URL
        QTest.mouseClick(self.window.ui.push_GET_request, Qt.LeftButton)  # Имитируем клик

        model = self.window.model  # Получаем модель списка
        self.assertIn("Error: URL is empty", model.stringList())  # Проверяем, есть ли ошибка

    def test_get_request_with_connection_error(self):
        url = "https://invalid-url.com"
        self.window.ui.lineEdit.setText(url)

        with mock.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error")):
            QTest.mouseClick(self.window.ui.push_GET_request, Qt.LeftButton)

            model = self.window.model
            self.assertTrue(any("Error: Failed to make GET request" in item for item in model.stringList()))

    def test_get_request_300_multiple_choices(self):
        url = "https://example.com"
        self.window.ui.lineEdit.setText(url)

        # Создаём мок для ответа с кодом 300
        mock_response = requests.Response()
        mock_response.status_code = 300
        mock_response._content = b"Multiple Choices"
        # Настраиваем мок, чтобы он выбрасывал HTTPError при вызове raise_for_status
        def raise_for_status():
            raise requests.exceptions.HTTPError("300 Multiple Choices")
        mock_response.raise_for_status = raise_for_status

        with mock.patch("requests.get", return_value=mock_response):
            QTest.mouseClick(self.window.ui.push_GET_request, Qt.LeftButton)

            model = self.window.model
            self.assertTrue(any("Error: Failed to make GET request" in item for item in model.stringList()))

    def test_get_request_400_bad_request(self):
        url = "https://example.com"
        self.window.ui.lineEdit.setText(url)

        # Создаём мок для ответа с кодом 400
        mock_response = requests.Response()
        mock_response.status_code = 400
        mock_response._content = b"Bad Request"
        def raise_for_status():
            raise requests.exceptions.HTTPError("400 Bad Request")
        mock_response.raise_for_status = raise_for_status

        with mock.patch("requests.get", return_value=mock_response):
            QTest.mouseClick(self.window.ui.push_GET_request, Qt.LeftButton)

            model = self.window.model
            self.assertTrue(any("Error: Failed to make GET request" in item for item in model.stringList()))

    def test_get_request_500_internal_server_error(self):
        url = "https://example.com"
        self.window.ui.lineEdit.setText(url)

        # Создаём мок для ответа с кодом 500
        mock_response = requests.Response()
        mock_response.status_code = 500
        mock_response._content = b"Internal Server Error"
        def raise_for_status():
            raise requests.exceptions.HTTPError("500 Internal Server Error")
        mock_response.raise_for_status = raise_for_status

        with mock.patch("requests.get", return_value=mock_response):
            QTest.mouseClick(self.window.ui.push_GET_request, Qt.LeftButton)

            model = self.window.model
            self.assertTrue(any("Error: Failed to make GET request" in item for item in model.stringList()))


if __name__ == "__main__":
    unittest.main()