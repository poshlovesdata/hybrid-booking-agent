import unittest

from app.models.schemas import FinalResponse


class TestFinalResponse(unittest.TestCase):
    def test_model_dump_uses_agent_message_key(self):
        response = FinalResponse(agent_message="Here are some options.", recommendations=[])
        dumped = response.model_dump()

        self.assertIn("agent_message", dumped)
        self.assertNotIn("agent_messge", dumped)
        self.assertEqual(dumped["agent_message"], "Here are some options.")


if __name__ == "__main__":
    unittest.main()
