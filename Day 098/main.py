"""
Day 98: Custom Automation Scripting Capstone
Phase 5: Portfolio

Key Concepts:
OS/Shutil File System Automation, File Organizer, System Monitoring Engine
"""

import os
import sys
import tempfile
import zipfile

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO, GEAR_SCENE
from automation_engine import (
    SystemMonitor,
    FileOrganizer,
    DuplicateDetector,
    BackupSnapshotEngine,
    compute_file_sha256
)


def banner():
    """Prints the project banner and ASCII art."""
    print("=" * 72)
    print(LOGO)
    print(GEAR_SCENE)
    print("=" * 72)
    print(" 🚀 DAY 98: CUSTOM AUTOMATION SCRIPTING CAPSTONE")
    print(" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print(" Key Concepts: OS/Shutil, SHA-256 Deduplication, Compression, Diagnostics")
    print("=" * 72 + "\n")


def run_automated_tests():
    """Validates system diagnostics, file organization, SHA-256 deduplication, and snapshots."""
    print("\n🔍 Running Day 98 Automated DevOps Automation Test Suite...")
    print("-" * 70)

    # 1. System diagnostics test
    metrics = SystemMonitor.get_system_metrics()
    assert metrics["cpu_cores"] >= 1
    assert metrics["disk_total_gb"] > 0
    assert metrics["disk_free_gb"] > 0
    print(f" [PASS] 1. System diagnostics verified ({metrics['os']}, {metrics['cpu_cores']} cores, {metrics['disk_total_gb']}GB disk).")

    # 2. SHA-256 hashing test
    temp_dir = tempfile.mkdtemp()
    test_file1 = os.path.join(temp_dir, "sample.txt")
    with open(test_file1, "w", encoding="utf-8") as f:
        f.write("Hello 100 Days of Code Automation!")
    h1 = compute_file_sha256(test_file1)
    assert len(h1) == 64
    assert isinstance(h1, str)
    print(f" [PASS] 2. Cryptographic SHA-256 file stream digest verified ({h1[:16]}...).")

    # 3. File organization by extension
    sandbox_organize = os.path.join(temp_dir, "organize_test")
    os.makedirs(sandbox_organize, exist_ok=True)
    with open(os.path.join(sandbox_organize, "photo.png"), "w") as f: f.write("dummy png")
    with open(os.path.join(sandbox_organize, "script.py"), "w") as f: f.write("print(1)")
    with open(os.path.join(sandbox_organize, "report.pdf"), "w") as f: f.write("dummy pdf")
    with open(os.path.join(sandbox_organize, "track.mp3"), "w") as f: f.write("dummy mp3")

    stats = FileOrganizer.organize_directory(sandbox_organize)
    assert stats.get("Images") == 1
    assert stats.get("Code") == 1
    assert stats.get("Documents") == 1
    assert stats.get("Audio") == 1
    assert os.path.exists(os.path.join(sandbox_organize, "Images", "photo.png"))
    assert os.path.exists(os.path.join(sandbox_organize, "Code", "script.py"))
    print(" [PASS] 3. Directory auto-classification & file reorganization verified.")

    # 4. Duplicate detection via SHA-256
    sandbox_dupes = os.path.join(temp_dir, "dupe_test")
    os.makedirs(sandbox_dupes, exist_ok=True)
    content = "Identical binary payload data for testing deduplication."
    file_orig = os.path.join(sandbox_dupes, "original.txt")
    file_copy1 = os.path.join(sandbox_dupes, "copy1.txt")
    file_copy2 = os.path.join(sandbox_dupes, "copy2.txt")
    file_diff = os.path.join(sandbox_dupes, "different.txt")
    with open(file_orig, "w") as f: f.write(content)
    with open(file_copy1, "w") as f: f.write(content)
    with open(file_copy2, "w") as f: f.write(content)
    with open(file_diff, "w") as f: f.write("Unique content string.")

    dupes = DuplicateDetector.scan_for_duplicates(sandbox_dupes)
    assert len(dupes) == 1
    matching_files = list(dupes.values())[0]
    assert len(matching_files) == 3
    print(" [PASS] 4. Two-stage size & SHA-256 duplicate detection verified (3 duplicates found).")

    # 5. Duplicate cleanup
    removed = DuplicateDetector.clean_duplicates(dupes, keep_first=True)
    assert removed == 2
    # Verify exactly 1 instance was preserved and different.txt untouched
    surviving = [p for p in (file_orig, file_copy1, file_copy2) if os.path.exists(p)]
    assert len(surviving) == 1
    assert os.path.exists(file_diff)
    print(" [PASS] 5. Safe deduplication execution verified (redundant copies purged, original preserved).")

    # 6. Backup snapshot and manifest
    backup_dest = os.path.join(temp_dir, "backups")
    zip_path, manifest_path = BackupSnapshotEngine.create_snapshot(sandbox_dupes, backup_dest)
    assert os.path.exists(zip_path)
    assert os.path.exists(manifest_path)
    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        assert os.path.basename(surviving[0]) in namelist
        assert "different.txt" in namelist
    with open(manifest_path, "r", encoding="utf-8") as f:
        m_content = f.read()
        assert "BACKUP MANIFEST" in m_content
    print(" [PASS] 6. Compressed ZIP snapshot and cryptographic checksum manifest verified.")

    print("-" * 70)
    print("✨ ALL 6 TESTS PASSED! Custom Automation Scripting Capstone fully operational.\n")


def interactive_cli():
    """Interactive command-line interface."""
    banner()

    while True:
        print("\n" + "=" * 55)
        print("  AUTOMATION & SYSADMIN COMMAND CENTER")
        print("=" * 55)
        print("  [1] System & Storage Hardware Diagnostics")
        print("  [2] Organize Unstructured Directory by File Extensions")
        print("  [3] Scan Directory for Duplicate Files (SHA-256)")
        print("  [4] Create Compressed Backup Archive & SHA-256 Manifest")
        print("  [5] Run Automated Test Suite")
        print("  [6] Exit")
        print("=" * 55)

        choice = input("Enter option (1-6): ").strip()

        if choice == "1":
            metrics = SystemMonitor.get_system_metrics()
            print("\n  💻 SYSTEM & HARDWARE DIAGNOSTICS:")
            print("  " + "-" * 50)
            print(f"  Operating System : {metrics['os']}")
            print(f"  Python Runtime   : v{metrics['python_version']}")
            print(f"  CPU Cores        : {metrics['cpu_cores']}")
            print(f"  Disk Total Space : {metrics['disk_total_gb']} GB")
            print(f"  Disk Used Space  : {metrics['disk_used_gb']} GB ({metrics['disk_usage_pct']}%)")
            print(f"  Disk Free Space  : {metrics['disk_free_gb']} GB")

        elif choice == "2":
            target = input("  Enter directory path to organize (default: current directory): ").strip() or "."
            try:
                stats = FileOrganizer.organize_directory(target)
                print(f"\n  [✓] Directory '{target}' organized successfully:")
                for cat, cnt in stats.items():
                    print(f"      • {cat:<12}: {cnt} files moved")
            except Exception as e:
                print(f"  [!] Error organizing directory: {e}")

        elif choice == "3":
            target = input("  Enter directory to scan for duplicates (default: current directory): ").strip() or "."
            print("  🔍 Scanning directory for identical files...")
            dupes = DuplicateDetector.scan_for_duplicates(target)
            if not dupes:
                print("  [✓] Zero duplicates found! Directory is clean.")
            else:
                total_dupes = sum(len(v) - 1 for v in dupes.values())
                print(f"\n  [!] Found {len(dupes)} duplicate sets ({total_dupes} redundant files):")
                for h, paths in dupes.items():
                    print(f"\n  SHA-256: {h[:16]}...")
                    for p in paths:
                        print(f"    - {p}")
                confirm = input("\n  Clean duplicates and keep 1 original of each? (y/N): ").strip().lower()
                if confirm == "y":
                    removed = DuplicateDetector.clean_duplicates(dupes)
                    print(f"  [✓] Cleaned {removed} redundant duplicate files!")

        elif choice == "4":
            src = input("  Enter folder to backup (default: '.'): ").strip() or "."
            dest = input("  Enter backup destination directory (default: 'backups'): ").strip() or "backups"
            zip_p, man_p = BackupSnapshotEngine.create_snapshot(src, dest)
            print(f"\n  [✓] Snapshot created:")
            print(f"      ZIP Archive : {zip_p}")
            print(f"      Manifest    : {man_p}")

        elif choice == "5":
            run_automated_tests()

        elif choice == "6":
            print("\n👋 Exiting Automation Capstone. Happy Automating!\n")
            break
        else:
            print("  [!] Invalid option. Please choose 1-6.")


def main():
    try:
        interactive_cli()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 98 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
