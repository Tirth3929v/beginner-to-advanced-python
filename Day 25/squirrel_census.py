import csv
import os
import sys

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_CSV = os.path.join(BASE_DIR, "squirrel_data.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "squirrel_count.csv")


def run_squirrel_census_analysis():
    """Analyzes Central Park Squirrel Census CSV data and exports primary fur color counts."""
    print("\n🐿️ Central Park Squirrel Census Data Processing...")
    print("─" * 60)

    if not os.path.exists(INPUT_CSV):
        print(f"❌ Error: Dataset file not found at '{INPUT_CSV}'")
        return

    # Count frequencies of primary fur colors
    gray_count = 0
    cinnamon_count = 0
    black_count = 0

    try:
        # Try using pandas if available and compatible
        import pandas as pd
        df = pd.read_csv(INPUT_CSV)
        gray_count = len(df[df["Primary Fur Color"] == "Gray"])
        cinnamon_count = len(df[df["Primary Fur Color"] == "Cinnamon"])
        black_count = len(df[df["Primary Fur Color"] == "Black"])
    except Exception:
        # Standard library CSV fallback for reliable data extraction
        with open(INPUT_CSV, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                color = row.get("Primary Fur Color", "").strip()
                if color == "Gray":
                    gray_count += 1
                elif color == "Cinnamon":
                    cinnamon_count += 1
                elif color == "Black":
                    black_count += 1


    summary_data = {
        "Fur Color": ["Gray", "Cinnamon", "Black"],
        "Count": [gray_count, cinnamon_count, black_count]
    }

    # Write summary output CSV file
    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["Fur Color", "Count"])
        for color, count in zip(summary_data["Fur Color"], summary_data["Count"]):
            writer.writerow([color, count])

    print("📊 Analysis Results:")
    print(f"   🔘 Gray Squirrels     : {gray_count}")
    print(f"   🔴 Cinnamon Squirrels : {cinnamon_count}")
    print(f"   🖤 Black Squirrels    : {black_count}")
    print("─" * 60)
    print(f"✅ Exported summary count report to '{OUTPUT_CSV}'!\n")


if __name__ == "__main__":
    run_squirrel_census_analysis()
