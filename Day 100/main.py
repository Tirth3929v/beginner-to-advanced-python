"""
Day 100: Predict Titanic Survival / Machine Learning Capstone
Phase 5: Portfolio - The 100th Milestone!

Key Concepts:
Scikit-Learn, Random Forest Classifier, Feature Engineering, Model Metrics
"""

import sys

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO, TITANIC_SCENE
from ml_pipeline import TitanicMLPipeline, extract_title


def banner():
    """Prints the project banner and ASCII art."""
    print("=" * 72)
    print(LOGO)
    print(TITANIC_SCENE)
    print("=" * 72)
    print(" 🚀 DAY 100: PREDICT TITANIC SURVIVAL / MACHINE LEARNING CAPSTONE")
    print(" 🎓 100 DAYS OF CODE BOOTCAMP - CURRICULUM GRADUATION!")
    print(" Key Concepts: Scikit-Learn, Random Forest, Feature Engineering, ROC-AUC")
    print("=" * 72 + "\n")


def run_automated_tests():
    """Validates data engineering, Random Forest training, metrics, and inference."""
    print("\n🔍 Running Day 100 Automated Machine Learning Pipeline Test Suite...")
    print("-" * 70)

    # 1. Feature extraction regex test
    assert extract_title("Braund, Mr. Owen Harris") == 0  # Mr
    assert extract_title("Cumings, Mrs. John Bradley") == 2  # Mrs
    assert extract_title("Heikkinen, Miss. Laina") == 1  # Miss
    assert extract_title("Palsson, Master. Gosta Leonard") == 3  # Master
    assert extract_title("Uruchurtu, Don. Manuel E") == 4  # Rare
    print(" [PASS] 1. Social title regex extraction and categorical mapping verified.")

    # 2. Pipeline initialization and training
    pipeline = TitanicMLPipeline()
    metrics = pipeline.train_and_evaluate(test_size=0.2)
    assert pipeline.is_trained is True
    assert metrics["rf_accuracy"] >= 0.70, f"Accuracy below baseline: {metrics['rf_accuracy']}"
    assert metrics["rf_roc_auc"] >= 0.70, f"ROC-AUC below baseline: {metrics['rf_roc_auc']}"
    print(f" [PASS] 2. Random Forest training verified (Accuracy: {metrics['rf_accuracy']*100:.1f}%, ROC-AUC: {metrics['rf_roc_auc']:.3f}).")

    # 3. Logistic Regression baseline comparison
    assert metrics["lr_accuracy"] >= 0.65
    print(f" [PASS] 3. Logistic Regression baseline evaluated (Accuracy: {metrics['lr_accuracy']*100:.1f}%).")

    # 4. Feature importance ranking
    features = dict(metrics["feature_importances"])
    assert "Sex" in features or "Title" in features or "Pclass" in features
    top_feature = metrics["feature_importances"][0][0]
    print(f" [PASS] 4. Gini impurity feature importances verified (Top predictor: {top_feature}).")

    # 5. High survival probability profile (1st Class Female, age 28, fare $100)
    high_prob_passenger = pipeline.predict_passenger(
        pclass=1, sex="female", age=28, sibsp=1, parch=0, fare=100.0, title="mrs"
    )
    assert high_prob_passenger["survived"] is True
    assert high_prob_passenger["survival_probability"] > 60.0
    print(f" [PASS] 5. High-probability survival profile verified ({high_prob_passenger['survival_probability']}% survival chance).")

    # 6. Low survival probability profile (3rd Class Male, age 35, solo, fare $8)
    low_prob_passenger = pipeline.predict_passenger(
        pclass=3, sex="male", age=35, sibsp=0, parch=0, fare=8.0, title="mr"
    )
    assert low_prob_passenger["survived"] is False
    assert low_prob_passenger["survival_probability"] < 50.0
    print(f" [PASS] 6. Low-probability survival profile verified ({low_prob_passenger['fatality_probability']}% fatality chance).")

    print("-" * 70)
    print("✨ ALL 6 TESTS PASSED! Titanic Survival Machine Learning Capstone fully operational.\n")


def print_celebration():
    """Prints the 100 Days of Code graduation announcement."""
    print("\n" + "*" * 74)
    print("  🎉🎉🎉 CONGRATULATIONS! YOU HAVE COMPLETED 100 DAYS OF CODE! 🎉🎉🎉")
    print("*" * 74)
    print("""
  From Day 1: Band Name Generator & Python Basics
  Through Phase 2: Object-Oriented Architecture, Turtle, Snake & Pong
  Through Phase 3: Web Scraping, REST APIs, Automation & GUI Apps
  Through Phase 4: Full-Stack Flask, SQL Databases, Auth & Security
  Through Phase 5: Advanced Data Science, Machine Learning & Capstone Portfolios!

  🏆 100 Projects Completed
  📦 Clean, Modular Software Architecture
  🚀 Production-Grade Test Suites Across Every Single Day
  🌟 Ready for Professional Python Engineering!
    """)
    print("*" * 74 + "\n")


def interactive_cli():
    """Interactive command-line interface."""
    banner()
    pipeline = TitanicMLPipeline()

    while True:
        print("\n" + "=" * 55)
        print("  TITANIC MACHINE LEARNING COMMAND CENTER")
        print("=" * 55)
        print("  [1] Train & Evaluate ML Models (RF vs Logistic Regression)")
        print("  [2] View Top Predictive Feature Importances")
        print("  [3] Predict Custom Passenger Survival")
        print("  [4] View Confusion Matrix & Model Metrics")
        print("  [5] Run Automated Test Suite")
        print("  [6] Celebrate 100 Days of Code Completion! 🎓")
        print("  [7] Exit")
        print("=" * 55)

        choice = input("Enter option (1-7): ").strip()

        if choice == "1":
            print("\n  🧠 Training Ensemble Random Forest & Logistic Regression...")
            metrics = pipeline.train_and_evaluate()
            print("\n  📊 MODEL EVALUATION RESULTS:")
            print("  " + "-" * 45)
            print(f"  Random Forest Accuracy    : {metrics['rf_accuracy']*100:.2f}%")
            print(f"  Random Forest Precision   : {metrics['rf_precision']*100:.2f}%")
            print(f"  Random Forest Recall      : {metrics['rf_recall']*100:.2f}%")
            print(f"  Random Forest F1-Score    : {metrics['rf_f1']:.4f}")
            print(f"  Random Forest ROC-AUC     : {metrics['rf_roc_auc']:.4f}")
            print(f"  Logistic Reg. Accuracy    : {metrics['lr_accuracy']*100:.2f}%")

        elif choice == "2":
            if not pipeline.is_trained:
                pipeline.train_and_evaluate()
            print("\n  🌟 GINI FEATURE IMPORTANCE RANKING:")
            print("  " + "-" * 45)
            for rank, (feat, score) in enumerate(pipeline.metrics["feature_importances"], 1):
                bar = "█" * int(score * 40)
                print(f"  {rank:>2}. {feat:<12} : {score:0.4f}  {bar}")

        elif choice == "3":
            print("\n  🚢 CUSTOM PASSENGER SURVIVAL SIMULATOR:")
            try:
                pclass_str = input("  Passenger Class (1, 2, or 3) [default 3]: ").strip() or "3"
                pclass = int(pclass_str)
                sex = input("  Sex (male/female) [default female]: ").strip().lower() or "female"
                age_str = input("  Age [default 25]: ").strip() or "25"
                age = float(age_str)
                sibsp_str = input("  Siblings/Spouse aboard [default 0]: ").strip() or "0"
                sibsp = int(sibsp_str)
                parch_str = input("  Parents/Children aboard [default 0]: ").strip() or "0"
                parch = int(parch_str)
                fare_str = input("  Ticket Fare in $ [default 20.0]: ").strip() or "20.0"
                fare = float(fare_str)
                title = input("  Title (mr/mrs/miss/master/rare) [default miss]: ").strip().lower() or "miss"

                res = pipeline.predict_passenger(
                    pclass=pclass, sex=sex, age=age, sibsp=sibsp, parch=parch, fare=fare, title=title
                )

                verdict = "SURVIVED 🟢" if res["survived"] else "PERISHED 🔴"
                print("\n  🔮 INFERENCE PREDICTION RESULT:")
                print("  " + "-" * 50)
                print(f"  Outcome               : {verdict}")
                print(f"  Survival Probability  : {res['survival_probability']}%")
                print(f"  Fatality Probability  : {res['fatality_probability']}%")
            except Exception as e:
                print(f"  [!] Invalid input: {e}")

        elif choice == "4":
            if not pipeline.is_trained:
                pipeline.train_and_evaluate()
            cm = pipeline.metrics["rf_confusion_matrix"]
            print("\n  📈 CONFUSION MATRIX (Random Forest):")
            print("  " + "-" * 40)
            print(f"  True Negatives  (Died as predicted)     : {cm[0][0]}")
            print(f"  False Positives (Predicted lived, died) : {cm[0][1]}")
            print(f"  False Negatives (Predicted died, lived) : {cm[1][0]}")
            print(f"  True Positives  (Lived as predicted)    : {cm[1][1]}")

        elif choice == "5":
            run_automated_tests()

        elif choice == "6":
            print_celebration()

        elif choice == "7":
            print("\n👋 Congratulations on completing 100 Days of Code! Farewell!\n")
            break
        else:
            print("  [!] Invalid option. Please choose 1-7.")


def main():
    try:
        interactive_cli()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 100 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
