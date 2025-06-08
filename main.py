import sys
import json
import requests
from datetime import datetime
from typing import Optional, List, Dict, Any

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QStringListModel

from main_window import Ui_MainMenu


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainMenu()
        self.ui.setupUi(self)
        self.ui.listView.setMinimumHeight(300)

        self.click_count: int = 0
        self.ui.push_POST_request.clicked.connect(self.post_request)
        self.ui.push_GET_request.clicked.connect(self.get_request)

        # Инициализируем модель для listView
        self.model: QStringListModel = QStringListModel()
        self.ui.listView.setModel(self.model)

    def post_request(self) -> None:
        url: str = self.ui.lineEdit.text().strip()
        if not url:
            self.add_to_list("Error: URL is empty")
            return

        try:
            response = requests.get('http://127.0.0.1:8000/retrieve')
            response.raise_for_status()
            result: Dict[str, List[Dict[str, Any]]] = response.json()
            data_list: List[Dict[str, Any]] = result.get("data", [])

            last_click: int = max(
                (item["click_count"] for item in data_list if item["url"] == url),
                default=0
            )
            new_click_count: int = last_click + 1

        except Exception as e:
            self.add_to_list(f"Error fetching click count: {e}")
            return

        current_time: datetime = datetime.now()
        date: str = current_time.strftime("%Y-%m-%d")
        time: str = current_time.strftime("%H:%M:%S")

        data: Dict[str, Any] = {
            "url": url,
            "date": date,
            "time": time,
            "click_count": new_click_count
        }

        display_text: str = f"Date: {date}\nTime: {time}\nClick Count: {new_click_count}"

        try:
            response = requests.post("http://127.0.0.1:8000/submit", json=data)
            response.raise_for_status()
            self.add_to_list(display_text)
        except requests.RequestException as e:
            self.add_to_list(f"POST request failed: {str(e)}")

    def get_request(self) -> None:
        url: str = self.ui.lineEdit.text().strip()
        if not url:
            self.add_to_list("Error: URL is empty")
            return

        try:
            response = requests.get(url)
            response.raise_for_status()

            try:
                data: Dict[str, Any] = response.json()
                display_text: str = json.dumps(data, indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                display_text: str = response.text

        except requests.RequestException as e:
            display_text: str = f"Error: Failed to make GET request ({str(e)})"

        self.add_to_list(display_text)

    def add_to_list(self, text: str) -> None:
        lines: List[str] = text.split('\n')
        current_list: List[str] = self.model.stringList()
        current_list.extend(lines)
        self.model.setStringList(current_list)


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())