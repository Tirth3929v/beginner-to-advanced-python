"""
Day 70: Version Control Mastery with Git & GitHub
Interactive Workshop, DAG Simulator, Conflict Lab & Repository Auditor
"""

import sys
import os
import subprocess

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO
from git_simulator import GitSimulator


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 70: VERSION CONTROL MASTERY WITH GIT & GITHUB")
    print(" 📚 Phase 4: Data Science & Engineering | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Core Engineering Concepts:")
    print("  • Directed Acyclic Graphs (DAG), SHA-1 content hashing & Tree Snapshots")
    print("  • Branching Strategies: Trunk-Based Development vs Git Flow")
    print("  • Fast-Forward Merging vs Three-Way Merges & Conflict Markers")
    print("  • Interactive Rebasing & Commit History Rewriting")
    print("=" * 76 + "\n")


def run_dag_simulation():
    """Simulates branch creation, independent commits, three-way merge and rebasing."""
    print("\n🌿 Initializing Git DAG Engine Simulation...")
    sim = GitSimulator()
    print("  • Created repository with default branch 'main' and root commit.")

    print("\n📝 1. Making commits on 'main'...")
    c1 = sim.commit("feat: add user authentication scaffolding")
    print(f"  -> Committed [{c1.hash}]: {c1.message}")

    print("\n🔀 2. Creating feature branch 'feature/login'...")
    sim.create_branch("feature/login")
    sim.checkout("feature/login")
    sim.stage_file("login.py", "def login(): pass")
    c2 = sim.commit("feat(auth): implement login endpoint logic")
    print(f"  -> Committed on 'feature/login' [{c2.hash}]: {c2.message}")

    print("\n🔀 3. Switching back to 'main' and committing concurrent work...")
    sim.checkout("main")
    sim.stage_file("README.md", "# My Project\nDocumentation updated on main.")
    c3 = sim.commit("docs: update README deployment guide")
    print(f"  -> Committed on 'main' [{c3.hash}]: {c3.message}")

    print("\n📊 Current DAG State before Merge:")
    print(sim.render_graph())

    print("\n🔗 4. Performing Three-Way Merge: 'feature/login' into 'main'...")
    status, merge_c = sim.merge("feature/login")
    print(f"  -> Result: {status}")

    print("\n📊 DAG State after Three-Way Merge:")
    print(sim.render_graph())

    print("\n🔄 5. Simulating Rebase Workflow on branch 'experiment'...")
    sim.create_branch("experiment")
    sim.checkout("experiment")
    sim.stage_file("experiment.py", "print('neural net experiment')")
    exp_c = sim.commit("feat(ml): prototype sentiment classifier")
    print(f"  -> Committed on 'experiment' [{exp_c.hash}]: {exp_c.message}")

    # Advance main
    sim.checkout("main")
    sim.stage_file("config.py", "DEBUG = True")
    sim.commit("chore: update debug config")

    # Now rebase experiment onto main
    sim.checkout("experiment")
    success, msg = sim.rebase("main")
    print(f"  -> Rebase result: {msg}")

    print("\n📊 Final DAG State:")
    print(sim.render_graph())


def run_conflict_lab():
    """Simulates a realistic merge conflict and guides the user through resolution."""
    print("\n⚔️ GIT MERGE CONFLICT RESOLUTION LAB")
    print("=" * 70)
    sim = GitSimulator()

    # Step 1: Base file on main
    base_code = 'PORT = 5000\nDATABASE = "production.db"\n'
    sim.stage_file("config.py", base_code)
    sim.commit("chore: initialize base configuration")

    # Step 2: Branch 1 changes PORT to 8080
    sim.create_branch("feature/port-update")
    sim.checkout("feature/port-update")
    sim.stage_file("config.py", 'PORT = 8080\nDATABASE = "production.db"\n')
    sim.commit("feat: update server port to 8080")

    # Step 3: Branch main concurrently changes PORT to 3000
    sim.checkout("main")
    sim.stage_file("config.py", 'PORT = 3000\nDATABASE = "production.db"\n')
    sim.commit("fix: change default port to 3000")

    print("Two developers edited the exact same line in 'config.py':")
    print("  • 'main':           PORT = 3000")
    print("  • 'feature/port-update': PORT = 8080\n")

    print("Attempting merge: git merge feature/port-update...")
    status, merge_c = sim.merge("feature/port-update")
    print(f"Result: {status}\n")

    print("📄 File contents with Git Conflict Markers:")
    print("-" * 50)
    print(sim.staging_area["config.py"])
    print("-" * 50)

    print("\n💡 Resolution Strategy:")
    print("  1. Inspect the markers: <<<<<<< HEAD vs >>>>>>> branch")
    print("  2. Consult the team or specification for the intended value")
    print("  3. Resolve the conflict by keeping the target config (e.g. PORT = 8080 from environment)")
    print("  4. Remove marker lines (<<<<<<<, =======, >>>>>>>)")
    print("  5. Stage and commit the resolved state: git add config.py && git commit -m 'resolve conflict'\n")


def audit_repository():
    """Audits the actual git repository health."""
    print("\n🔍 REAL WORKSPACE GIT REPOSITORY AUDIT")
    print("=" * 70)
    try:
        # Branch
        branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
        print(f"  • Current Working Branch: \033[92m{branch}\033[0m")

        # Remote
        remotes = subprocess.check_output(["git", "remote", "-v"], text=True).strip().splitlines()
        print(f"  • Remotes Configured:     {remotes[0] if remotes else 'None'}")

        # Recent 5 commits
        log = subprocess.check_output(["git", "log", "-n", "5", "--oneline"], text=True).strip().splitlines()
        print("  • Recent 5 Commits:")
        for line in log:
            print(f"      {line}")

        # Status check
        status = subprocess.check_output(["git", "status", "-s"], text=True).strip()
        clean = "Clean working tree ✨" if not status else f"{len(status.splitlines())} modified/untracked files"
        print(f"  • Working Tree Status:   {clean}")
        print("=" * 70 + "\n")
    except Exception as e:
        print(f"⚠️ Git repository audit failed: {e}\n")


def run_automated_tests():
    """Runs automated verification tests for the Git engine."""
    print("\n🔍 Running Day 70 Automated Git Engine Verification Tests...")
    print("-" * 70)
    sim = GitSimulator()

    # Test 1: Root commit
    assert "main" in sim.branches
    assert len(sim.commits) == 1
    print(" [PASS] 1. Root commit & default branch verified.")

    # Test 2: Branch creation & switching
    assert sim.create_branch("develop") is True
    assert sim.checkout("develop") is True
    assert sim.head == "develop"
    print(" [PASS] 2. Branch creation & checkout verified.")

    # Test 3: Commit isolation
    sim.stage_file("dev.txt", "dev branch only")
    c_dev = sim.commit("feat: add dev module")
    assert sim.branches["develop"] == c_dev.hash
    assert sim.branches["main"] != c_dev.hash
    print(" [PASS] 3. Branch pointer isolation verified.")

    # Test 4: Fast-forward merge
    sim.checkout("main")
    status, m = sim.merge("develop")
    assert "Fast-forward" in status
    assert sim.branches["main"] == sim.branches["develop"]
    print(" [PASS] 4. Fast-forward merge verified.")

    # Test 5: Three-way merge
    sim.create_branch("featA")
    sim.checkout("featA")
    sim.stage_file("fileA.txt", "A content")
    sim.commit("feat: A")

    sim.checkout("main")
    sim.stage_file("fileB.txt", "B content")
    sim.commit("feat: B")

    status, m_commit = sim.merge("featA")
    assert "Three-way merge succeeded" in status
    assert len(m_commit.parents) == 2
    print(" [PASS] 5. Three-way merge commit with multiple parents verified.")

    # Test 6: Merge conflict detection
    sim.create_branch("conflict_branch")
    sim.checkout("conflict_branch")
    sim.stage_file("fileA.txt", "Conflicting A content from branch")
    sim.commit("feat: change fileA on branch")

    sim.checkout("main")
    sim.stage_file("fileA.txt", "Conflicting A content on main")
    sim.commit("feat: change fileA on main")

    status, _ = sim.merge("conflict_branch")
    assert "CONFLICT" in status
    assert "<<<<<<< HEAD" in sim.staging_area["fileA.txt"]
    print(" [PASS] 6. Merge conflict detection & marker generation verified.")

    print("-" * 70)
    print("✨ ALL 6 TESTS PASSED! Git Engine Simulator fully operational.\n")


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) 🌿 Run Interactive Git DAG Simulator (Branching, Merging, Rebasing)")
        print("  2) ⚔️ Merge Conflict Resolution Lab (Conflict markers & 3-way resolution)")
        print("  3) 🔍 Real Workspace Git Repository Audit")
        print("  4) ✅ Run Automated Verification Suite (6 Unit Tests)")
        print("  5) 🚪 Exit")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            run_dag_simulation()
        elif choice == "2":
            run_conflict_lab()
        elif choice == "3":
            audit_repository()
        elif choice == "4":
            run_automated_tests()
        elif choice in ("5", "exit", "quit", "q"):
            print("\n👋 Happy Version Controlling! Keep your commit trees clean 🌿\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 70 gracefully... Goodbye!\n")
