import unittest
from unittest.mock import patch

from app.services.sqlite_service import check_live_availabilty


class TestCheckLiveAvailabilty(unittest.TestCase):
    @patch("app.services.sqlite_service.logger")
    @patch("app.services.sqlite_service.get_db_connection")
    def test_empty_item_ids_returns_empty_list_without_db(self, mock_get_db_connection, mock_logger):
        result = check_live_availabilty([], "10:00", 2, "2026-01-01", 1)

        self.assertEqual(result, [])
        mock_get_db_connection.assert_not_called()
        mock_logger.info.assert_called_once_with(
            "No matching workspace ids for availability check; returning empty list"
        )


if __name__ == "__main__":
    unittest.main()
