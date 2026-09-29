"""
test_engine.py — Automated rule tests for Ustaad-in-a-Box

Run: python test_engine.py
Every rule must have at least one passing test per language.
Failures are printed and summarised.
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from engine import RuleEngine

engine = RuleEngine()

# Format: (description, input_text, expected_verdict, expected_rule_id_or_None)
# expected_rule_id=None means any verdict is acceptable (used for no-match tests)

TESTS = [
    # ── Safety stops — must ALL be ESCALATE ──────────────────────────────────
    ("BAT-003 en: swollen battery",            "my battery is swollen",              "ESCALATE", "BAT-003"),
    ("BAT-003 ro: pholi battery",              "battery pholi hui hai",               "ESCALATE", "BAT-003"),
    ("BAT-003 ro: bulging back",               "phone ka back ublta hai",             "ESCALATE", "BAT-003"),
    ("BAT-004 en: leaking battery",            "liquid is leaking from battery",      "ESCALATE", "BAT-004"),
    ("BAT-004 ro: liquid nikal raha",          "battery se liquid nikal raha",        "ESCALATE", "BAT-004"),
    ("SMK-001 en: smoke",                      "smoke coming from phone",             "ESCALATE", "SMK-001"),
    ("SMK-001 ro: dhuan",                      "phone se dhuan aa raha",              "ESCALATE", "SMK-001"),
    ("SMK-001 en: burning smell",              "burning smell from my phone",         "ESCALATE", "SMK-001"),
    ("WAT-001 en: wet and on",                 "phone got wet and is still on",       "ESCALATE", "WAT-001"),
    ("WAT-001 ro: paani gira, on hai",         "paani gira aur phone on hai",         "ESCALATE", "WAT-001"),
    ("CHG-002 en: overheating while charging", "phone gets very hot while charging",  "ESCALATE", "CHG-002"),
    ("CHG-002 ro: garam while charging",       "charging karte waqt bahut garam hota","ESCALATE", "CHG-002"),
    ("PWR-001 en: open power bank",            "can I open my power bank",            "ESCALATE", "PWR-001"),
    ("PWR-002 ro: power bank overheating",     "power bank garam ho gaya charge karte waqt", "ESCALATE", "PWR-002"),

    # ── Caution / Normal ─────────────────────────────────────────────────────
    ("WAT-002 en: wet but off",                "phone got wet, I turned it off",      "CAUTION",  "WAT-002"),
    ("WAT-002 ro: bheeg gaya band hai",        "phone bheeg gaya band hai",           "CAUTION",  "WAT-002"),
    ("CHG-001 en: not charging",               "phone is not charging",               "CAUTION",  "CHG-001"),
    ("CHG-001 ro: charge nahi",                "phone charge nahi ho raha",           "CAUTION",  "CHG-001"),
    ("BAT-001 en: fast battery drain",         "battery drains very fast",            "CAUTION",  "BAT-001"),
    ("BAT-001 ro: jaldi khatam",               "battery jaldi khatam hoti hai",       "CAUTION",  "BAT-001"),
    ("SCR-001 en: cracked screen touch ok",    "my screen is cracked but touch works","SAFE",     "SCR-001"),
    ("SCR-001 ro: crack, touch kaam karta",    "screen toot gayi lekin touch kaam karta","SAFE",  "SCR-001"),
    ("SCR-002 en: cracked no touch",           "cracked screen touch not working",    "CAUTION",  "SCR-002"),
    ("SCR-002 ro: crack, touch nahi",          "screen crack touch nahi kaam karta",  "CAUTION",  "SCR-002"),
    ("DEV-001 en: slow phone",                 "my phone is very slow and hanging",   "CAUTION",  "DEV-001"),
    ("DEV-001 ro: hang ho raha",               "phone hang ho raha hai",              "CAUTION",  "DEV-001"),
    ("DEV-002 user: zaada garam hora hai",     "mobile buht zaada garam hora hai",    "CAUTION",  "DEV-002"),
    ("LAP-001 en: laptop overheating",         "my laptop gets very hot",             "CAUTION",  "LAP-001"),
    ("LAP-001 user: laptop heating",           "laptop buht zada heating krra hai",   "CAUTION",  "LAP-001"),
    ("REP-001 en: repair vs replace",          "should I repair or replace my phone", "CAUTION",  "REP-001"),
    ("SCR-000 user: screen toot gyi",          "screen toot gyi hai mobile ki",       "CAUTION",  "SCR-000"),
    ("BAT-001 user: khtm hori hai",            "battery buht jaldi khtm hori hai mobile ki", "CAUTION", "BAT-001"),
    ("WAT-002 user: paani mai gir gya",        "mobile paani mai gir gya haii",       "CAUTION",  "WAT-002"),
    ("SCR-003: internal ink bleed",            "screen has purple ink spots but touch works", "CAUTION", "SCR-003"),

    # ── Adversarial Safety & Edge Case Probes ────────────────────────────────
    ("PROBE: swollen battery phooli variant",   "Mera phone charge nahi ho raha aur battery phooli hui hai", "ESCALATE", "BAT-003"),
    ("PROBE: touch negation",                  "screen toot gayi touch kaam nahi kar raha", "CAUTION", "SCR-002"),
    ("PROBE: water precedence over screen",     "Paani mein gira, screen toot gayi, touch kaam kar raha hai", "ESCALATE", "WAT-001"),
    ("PROBE: hairdryer + charging (WAT-003)",   "Fell in water, dried with hairdryer, now charging", "ESCALATE", "WAT-003"),
    ("PROBE: fire in phone not blocked by fir", "Phone fire pakad raha hai", "ESCALATE", "SMK-001"),
    ("PROBE: frustrated not blocked by rust",   "I am frustrated, my phone hangs", "CAUTION", "DEV-001"),
    ("PROBE: battery leak negation",           "battery leak nahi hui",               "ESCALATE", None),
    ("PROBE: not hot not swollen negation",     "phone is not hot, not swollen",       "ESCALATE", None),
    ("REGRESSION: swollen + not charging",      "battery swollen hai phone charge nahi ho raha", "ESCALATE", "BAT-003"),
    ("REGRESSION: swollen not charging en",     "battery swollen not charging",        "ESCALATE", "BAT-003"),
    ("REGRESSION: hot + not charging",          "phone garam ho gaya charge nahi ho raha", "CAUTION", "DEV-002"),
    ("REGRESSION: wet + not working",           "phone paani mein gira nahi chal raha", "CAUTION", "WAT-002"),
    ("REGRESSION: swollen + not turning on",    "battery phool gayi hai phone on nahi hota", "ESCALATE", "BAT-003"),
    ("REGRESSION: drain rate false positive",   "Battery drain rate bohot high hai",   "CAUTION",  "BAT-001"),

    # ── Out-of-scope — must ALL be ESCALATE ─────────────────────────────────
    ("OOS: price",             "how much does it cost to repair",            "ESCALATE", None),
    ("OOS: price roman urdu",  "iphone screen crack ho gaya kitne ka aayega", "ESCALATE", None),
    ("OOS: unlock",            "can you unlock my phone",                    "ESCALATE", None),
    ("OOS: medical",           "is radiation from phone harmful",            "ESCALATE", None),
    ("OOS: data",              "data recovery kaise hogi",                   "ESCALATE", None),
    ("OOS: warranty",          "warranty claim karna hai",                   "ESCALATE", None),
    ("OOS: empty",             "",                                           None,       None),  # handled by API layer

    # ── No match — must escalate ─────────────────────────────────────────────
    ("NO-MATCH: random", "what is the weather today",        "ESCALATE", None),
    ("NO-MATCH: TV",     "my TV is not working",             "ESCALATE", None),
]


# ── Run tests ──────────────────────────────────────────────────
passed = 0
failed = 0
errors = []

print(f"\n{'='*60}")
print(f"  Ustaad-in-a-Box — Rule Engine Tests")
print(f"{'='*60}\n")

for desc, text, expected_verdict, expected_rule in TESTS:
    if not text:  # empty input handled upstream
        print(f"  SKIP  {desc}")
        continue

    decision = engine.decide(text)
    ok_verdict = (expected_verdict is None) or (decision.verdict == expected_verdict)
    ok_rule    = (expected_rule    is None) or (decision.rule_id  == expected_rule)

    if ok_verdict and ok_rule:
        passed += 1
        print(f"  ✓  {desc}")
    else:
        failed += 1
        msg = (
            f"  ✗  {desc}\n"
            f"       input:    {repr(text)}\n"
            f"       expected: verdict={expected_verdict}, rule={expected_rule}\n"
            f"       got:      verdict={decision.verdict}, rule={decision.rule_id}\n"
            f"       tags:     {decision.matched_tags}"
        )
        print(msg)
        errors.append(msg)

total = passed + failed
print(f"\n{'='*60}")
print(f"  {passed}/{total} passed  |  {failed} failed")
print(f"{'='*60}\n")

if errors:
    print("FAILED TESTS — add these to your honesty note:\n")
    for e in errors:
        print(e)
    exit(1)
else:
    print("All tests passed. ✓\n")
    exit(0)
