"""
package_submission.py — Ustaad-in-a-Box Final Submission Packager

Bundles all deliverables, verified source code, docs, review sheets,
and generates a cryptographic SHA-256 manifest ready for Rocketathon 2026.

Run: python package_submission.py
"""
import hashlib
import os
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
OUTPUT_ZIP = ROOT / "ustaad_in_a_box_submission.zip"
EXPORT_DIR = ROOT / "submission_export"

FILES_TO_PACKAGE = [
    # Core Engine & Server
    "engine.py",
    "main.py",
    "logger.py",
    "rules.yaml",
    "synonyms.yaml",
    "requirements.txt",
    "run.bat",
    "test_engine.py",
    # Frontend
    "static/index.html",
    # Evaluation & Data
    "ustaad_review.csv",
    "interactions.jsonl",
    # Master Documentation
    "README.md",
    # Formal Deliverables
    "docs/BILL_OF_PROVENANCE.md",
    "docs/HONESTY_NOTE.md",
    "docs/ARCHITECTURE.md",
    "docs/RULE_AUTHORING_GUIDE.md",
    "docs/API_REFERENCE.md",
    "docs/DEMO_SCRIPT.md",
    "docs/SUBMISSION_CHECKLIST.md",
]


def sha256_of_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("\n" + "=" * 60)
    print("  Ustaad-in-a-Box — Packaging Final Submission")
    print("=" * 60 + "\n")

    # Ensure export directory is clean
    shutil.rmtree(EXPORT_DIR, ignore_errors=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    manifest_lines = [
        "==================================================================",
        "USTAAD-IN-A-BOX: ROCKETATHON 2026 FINAL SUBMISSION MANIFEST",
        f"Generated At: {datetime.now(timezone.utc).isoformat()}",
        "Track: Track 1: Stand-In",
        "Team: Dawood University of Engineering & Technology (DUET)",
        "Venue: Expo Centre Karachi",
        "==================================================================\n",
        "FILES AND SHA-256 CHECKSUMS:\n",
    ]

    copied_files = []

    for rel_path in FILES_TO_PACKAGE:
        if "__pycache__" in rel_path or rel_path.endswith(".pyc"):
            continue
        src = ROOT / rel_path
        if not src.exists():
            print(f"  [!] Missing file: {rel_path}")
            continue

        dst = EXPORT_DIR / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

        file_hash = sha256_of_file(src)
        manifest_lines.append(f"{file_hash}  {rel_path}")
        copied_files.append((src, rel_path))
        print(f"  [+] Packaged: {rel_path}")

    # Write Manifest
    manifest_path = EXPORT_DIR / "MANIFEST.txt"
    manifest_path.write_text("\n".join(manifest_lines), encoding="utf-8")
    copied_files.append((manifest_path, "MANIFEST.txt"))
    print(f"  [+] Generated: MANIFEST.txt")

    # Create Zip Archive
    print(f"\nCreating ZIP archive: {OUTPUT_ZIP.name} ...")
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for disk_path, arc_name in copied_files:
            if "__pycache__" in arc_name or arc_name.endswith(".pyc"):
                continue
            z.write(disk_path, arcname=f"ustaad_in_a_box/{arc_name}")

    zip_size_kb = OUTPUT_ZIP.stat().st_size / 1024
    print(f"\nSuccessfully generated: {OUTPUT_ZIP.name} ({zip_size_kb:.1f} KB)")
    print(f"Submission folder ready at: {EXPORT_DIR.name}/")
    print("\n" + "=" * 60)
    print("  ALL SYSTEMS READY FOR SUBMISSION AND JUDGING!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
