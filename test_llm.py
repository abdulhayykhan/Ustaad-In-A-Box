"""
test_llm.py — Unit tests for Groq LLM phrasing layer
"""
import os
import unittest
from engine import Decision, RuleEngine
from llm import GroqPhraser


HAS_KEY = GroqPhraser().is_available()


class TestGroqPhraser(unittest.TestCase):

    def setUp(self):
        self.phraser = GroqPhraser()
        self.engine = RuleEngine()

    @unittest.skipUnless(HAS_KEY, "needs GROQ_API_KEY and network")
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

    @unittest.skipUnless(HAS_KEY, "needs GROQ_API_KEY and network")
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

    @unittest.skipUnless(HAS_KEY, "needs GROQ_API_KEY and network")
    def test_groq_phrasing_safe(self):
        """Test live Groq rephrasing on safe cracked screen."""
        d = self.engine.decide("screen is cracked but touch works")
        self.assertEqual(d.verdict, "SAFE")
        self.assertEqual(d.rule_id, "SCR-001")

        phrased, provider = self.phraser.phrase("screen is cracked but touch works", d)
        self.assertTrue(provider.startswith("groq:"))
        self.assertGreater(len(phrased), 20)

    def test_guard_rejects_reassuring_escalate(self):
        """A reassuring phrasing of an ESCALATE verdict must be rejected (offline test)."""
        d = self.engine.decide("battery pholi hui hai")
        self.assertFalse(self.phraser._passes_guard("Koi masla nahi, phone safe hai.", d))
        self.assertTrue(self.phraser._passes_guard("Charging band karo aur shop le aao.", d))


if __name__ == "__main__":
    unittest.main()
