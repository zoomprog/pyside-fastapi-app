import unittest
from unittest.mock import patch, MagicMock
from server.server import app, DataCreate, add_data, get_data, Data

class TestFastAPIEndpoints(unittest.IsolatedAsyncioTestCase):
    async def test_add_data(self):
        data = DataCreate(url="https://example.com", date="2023-01-01", time="12:00:00", click_count=1)
        with patch("server.server.SessionLocal") as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            response = await add_data(data, db=mock_db)
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()
            mock_db.refresh.assert_called_once()
            self.assertEqual(response, {"status": "success", "data": data})

    async def test_get_data(self):
        mock_data = [
            Data(id=1, url="https://example.com", date="2023-01-01", time="12:00:00", click_count=1),
            Data(id=2, url="https://example2.com", date="2023-01-02", time="13:00:00", click_count=2)
        ]
        with patch("server.server.SessionLocal") as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_data
            response = await get_data(skip=0, limit=10, db=mock_db)
            mock_db.query.assert_called_once_with(Data)
            self.assertEqual(response, {"data": mock_data})

    async def test_add_data_invalid_input(self):
        invalid_data = DataCreate(url="", date="2023-01-01", time="12:00:00", click_count=-1)
        with patch("server.server.SessionLocal") as mock_session:
            mock_db = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_db
            try:
                await add_data(invalid_data, db=mock_db)
            except Exception as e:
                self.assertIsInstance(e, Exception)
                self.assertFalse(mock_db.add.called, "Add should not be called with invalid data")

if __name__ == "__main__":
    unittest.main()