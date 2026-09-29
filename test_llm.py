"""
test_llm.py — Unit tests for Groq LLM phrasing layer
"""
import os
import unittest
from engine import Decision, RuleEngine
from llm import GroqPhraser


class TestGroqPhraser(unittest.TestCase):

    def setUp(self):
        self.phraser = GroqPhraser()
        self.engine = RuleEngine()

    def test_availability(self):
        """Phraser should detect available API key from .env."""
        self.assertTrue(self.phraser.is_available())

    def test_fallback_when_disabled(self):
        """When API key is empty, must instantly return exact decision.answer."""
        empty_phraser = GroqPhraser(api_key="")
        d = self.engine.decide("battery drain")
        phrased, provider = empty_phraser.phrase("battery drain", d)
        self.assertEqual(phrased, d.answer)
        self.assertEqual(provider, "deterministic_rule_engine")

    def test_groq_phrasing_escalate(self):
        """Test live Groq rephrasing on critical battery safety stop."""
        d = self.engine.decide("battery phooli hui hai")
        self.assertEqual(d.verdict, "ESCALATE")
        self.assertEqual(d.rule_id, "BAT-003")

        phrased, provider = self.phraser.phrase("battery phooli hui hai", d)
        self.assertTrue(provider.startswith("groq:"))
        self.assertGreater(len(phrased), 20)
        # Check that safety guidance is present
        lower = phrased.lower()
        has_stop = any(w in lower for w in ["band", "mat", "risk", "hazard", "dukaan", "check", "kharab", "aag", "stop", "off"])
        self.assertTrue(has_stop, f"Phrased text lacks safety instructions: {phrased}")

    def test_groq_phrasing_safe(self):
        """Test live Groq rephrasing on safe cracked screen."""
        d = self.engine.decide("screen is cracked but touch works")
        self.assertEqual(d.verdict, "SAFE")
        self.assertEqual(d.rule_id, "SCR-001")

        phrased, provider = self.phraser.phrase("screen is cracked but touch works", d)
        self.assertTrue(provider.startswith("groq:"))
        self.assertGreater(len(phrased), 20)


if __name__ == "__main__":
    unittest.main()
