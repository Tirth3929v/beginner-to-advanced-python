"""
Day 65: Web Design Principles & UX/UI Studio Server
Interactive studio providing design token calculators, contrast ratio evaluators,
and typography scale visualizers.
"""

from flask import Flask, render_template, request, jsonify
from design_system import (
    CURATED_PALETTES,
    calculate_contrast_ratio,
    evaluate_wcag,
    generate_modular_scale,
)

app = Flask(__name__)


@app.route("/")
def home():
    # Compute contrast ratios for each curated palette
    enhanced_palettes = {}
    for name, p in CURATED_PALETTES.items():
        ratio = round(calculate_contrast_ratio(p["primary"], p["bg"]), 2)
        enhanced_palettes[name] = {**p, "contrast": ratio}

    type_scale = generate_modular_scale(base=16.0, ratio=1.25, steps=6)
    return render_template("index.html", palettes=enhanced_palettes, type_scale=type_scale)


@app.route("/api/contrast")
def api_contrast():
    fg = request.args.get("fg", "#ffffff")
    bg = request.args.get("bg", "#000000")
    try:
        ratio = round(calculate_contrast_ratio(fg, bg), 2)
        evaluations = evaluate_wcag(ratio)
        return jsonify({"foreground": fg, "background": bg, "contrast_ratio": ratio, "wcag": evaluations})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    print("🌐 Starting Day 65 Design Lab Studio on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
