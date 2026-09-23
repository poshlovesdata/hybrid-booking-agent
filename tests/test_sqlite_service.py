import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.services.sqlite_service import (
    check_live_availabilty,
    get_db_connection,
    setup_database,
)


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


class TestCheckLiveAvailabiltyWithDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_file_patcher = patch(
            "app.services.sqlite_service.DB_FILE",
            str(Path(self.temp_dir.name) / "inventory.db"),
        )
        self.db_file_patcher.start()
        setup_database()

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO workspaces (id, name, location, base_capacity, price_per_hour)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("space_1", "Test Workspace", "Test Location", 4, 25),
        )
        conn.commit()
        conn.close()

    def tearDown(self):
        self.db_file_patcher.stop()
        self.temp_dir.cleanup()

    def add_booking(self, start_time, end_time):
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO bookings (workspace_id, booking_date, start_time, end_time)
            VALUES (?, ?, ?, ?)
            """,
            ("space_1", "2026-01-01", start_time, end_time),
        )
        conn.commit()
        conn.close()

    def test_non_zero_minutes_are_preserved_when_calculating_end_time(self):
        self.add_booking("15:30", "16:00")

        result = check_live_availabilty(
            ["space_1"], "14:45", 1, "2026-01-01", 1
        )

        self.assertEqual(result, [])

    def test_booking_overlapping_only_previously_truncated_minutes_is_excluded(self):
        self.add_booking("12:00", "12:30")

        result = check_live_availabilty(
            ["space_1"], "10:30", 2, "2026-01-01", 1
        )

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
