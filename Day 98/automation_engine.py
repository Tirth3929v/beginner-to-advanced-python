"""
Day 98: Custom Automation Scripting Capstone
File System Automation, Deduplication, and System Diagnostics Engine
"""

import hashlib
import os
import platform
import shutil
import time
import zipfile
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any

CATEGORY_EXTENSIONS = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".csv", ".xlsx", ".md"},
    "Code": {".py", ".js", ".html", ".css", ".json", ".sh", ".sql", ".rs"},
    "Audio": {".mp3", ".wav", ".aac", ".ogg", ".flac"},
    "Archives": {".zip", ".tar", ".gz", ".7z", ".rar"}
}


def compute_file_sha256(filepath: str, chunk_size: int = 65536) -> str:
    """Computes SHA-256 hexadecimal digest of a file stream."""
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            sha.update(chunk)
    return sha.hexdigest()


class SystemMonitor:
    """Collects operating system, processor, and disk storage metrics."""

    @staticmethod
    def get_system_metrics(path: str = ".") -> Dict[str, Any]:
        total, used, free = shutil.disk_usage(os.path.abspath(path))
        gb = 1024 ** 3

        return {
            "os": f"{platform.system()} {platform.release()} ({platform.architecture()[0]})",
            "python_version": platform.python_version(),
            "cpu_cores": os.cpu_count() or 1,
            "disk_total_gb": round(total / gb, 2),
            "disk_used_gb": round(used / gb, 2),
            "disk_free_gb": round(free / gb, 2),
            "disk_usage_pct": round((used / total) * 100, 1)
        }


class FileOrganizer:
    """Scans and organizes unorganized folders into classified subdirectories."""

    @staticmethod
    def organize_directory(target_dir: str) -> Dict[str, int]:
        target = os.path.abspath(target_dir)
        stats: Dict[str, int] = {}

        if not os.path.isdir(target):
            raise ValueError(f"Target path '{target_dir}' is not a valid directory.")

        for item in os.listdir(target):
            item_path = os.path.join(target, item)
            if os.path.isdir(item_path):
                continue

            _, ext = os.path.splitext(item)
            ext_lower = ext.lower()

            destination_cat = "Misc"
            for cat, exts in CATEGORY_EXTENSIONS.items():
                if ext_lower in exts:
                    destination_cat = cat
                    break

            cat_dir = os.path.join(target, destination_cat)
            os.makedirs(cat_dir, exist_ok=True)

            dest_path = os.path.join(cat_dir, item)
            # Avoid overwriting existing files
            if os.path.exists(dest_path):
                base, ext_part = os.path.splitext(item)
                dest_path = os.path.join(cat_dir, f"{base}_{int(time.time())}{ext_part}")

            shutil.move(item_path, dest_path)
            stats[destination_cat] = stats.get(destination_cat, 0) + 1

        return stats


class DuplicateDetector:
    """Identifies bitwise identical duplicate files via 2-stage size & SHA-256 filtering."""

    @staticmethod
    def scan_for_duplicates(target_dir: str) -> Dict[str, List[str]]:
        target = os.path.abspath(target_dir)
        size_buckets: Dict[int, List[str]] = {}

        # Stage 1: Group files by byte size
        for root, _, files in os.walk(target):
            for f in files:
                full_path = os.path.join(root, f)
                try:
                    size = os.path.getsize(full_path)
                    size_buckets.setdefault(size, []).append(full_path)
                except (OSError, PermissionError):
                    continue

        # Stage 2: Hash files with identical sizes
        hash_buckets: Dict[str, List[str]] = {}
        for size, file_list in size_buckets.items():
            if len(file_list) > 1 and size > 0:
                for file_path in file_list:
                    try:
                        f_hash = compute_file_sha256(file_path)
                        hash_buckets.setdefault(f_hash, []).append(file_path)
                    except (OSError, PermissionError):
                        continue

        # Return only hashes with 2 or more files
        return {h: paths for h, paths in hash_buckets.items() if len(paths) > 1}

    @staticmethod
    def clean_duplicates(duplicates: Dict[str, List[str]], keep_first: bool = True) -> int:
        removed_count = 0
        for h, paths in duplicates.items():
            to_remove = paths[1:] if keep_first else paths[:-1]
            for p in to_remove:
                try:
                    os.remove(p)
                    removed_count += 1
                except (OSError, PermissionError):
                    pass
        return removed_count


class BackupSnapshotEngine:
    """Creates compressed timestamped ZIP snapshots with cryptographic manifest checksums."""

    @staticmethod
    def create_snapshot(source_dir: str, backup_dest_dir: str) -> Tuple[str, str]:
        src = os.path.abspath(source_dir)
        dest = os.path.abspath(backup_dest_dir)
        os.makedirs(dest, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(src) or "backup"
        zip_filename = f"{base_name}_snapshot_{timestamp}.zip"
        zip_filepath = os.path.join(dest, zip_filename)

        manifest_filename = f"{base_name}_manifest_{timestamp}.txt"
        manifest_filepath = os.path.join(dest, manifest_filename)

        manifest_lines = [
            f"# BACKUP MANIFEST: {zip_filename}",
            f"# Timestamp: {timestamp}",
            f"# Source: {src}",
            f"# ----------------------------------------------------"
        ]

        with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(src):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, src)
                    zf.write(full_path, arcname=rel_path)
                    f_hash = compute_file_sha256(full_path)
                    manifest_lines.append(f"{f_hash}  {rel_path}")

        with open(manifest_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(manifest_lines) + "\n")

        return zip_filepath, manifest_filepath
