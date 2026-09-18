"""
Day 70: Git Internal Architecture & DAG Engine Simulator
Models Git's content-addressable storage and Directed Acyclic Graph (DAG) for:
- Commits (hash, author, parent references, tree snapshots)
- Branch pointers and HEAD tracking
- Fast-forward vs Three-Way Merge logic
- Rebase history reconstruction
- ASCII commit graph rendering
"""

import hashlib
import time
from typing import Dict, List, Optional, Tuple


class Commit:
    def __init__(self, message: str, parents: List[str], snapshot: Dict[str, str], author: str = "Developer <dev@code.org>"):
        self.message = message
        self.parents = parents
        self.snapshot = dict(snapshot)  # file_path -> content
        self.timestamp = time.time()
        self.author = author

        content_for_hash = f"{message}|{','.join(parents)}|{self.timestamp}|{str(sorted(snapshot.items()))}"
        self.hash = hashlib.sha1(content_for_hash.encode("utf-8")).hexdigest()[:8]

    def __repr__(self) -> str:
        return f"<Commit {self.hash}: '{self.message}'>"


class GitSimulator:
    def __init__(self):
        self.commits: Dict[str, Commit] = {}
        self.branches: Dict[str, str] = {}  # branch_name -> commit_hash
        self.head: str = "main"  # current branch name or detached commit hash
        self.staging_area: Dict[str, str] = {}
        self.working_dir: Dict[str, str] = {}

        # Initialize root commit
        self.working_dir["README.md"] = "# My Project\nInitial release"
        self.stage_file("README.md", self.working_dir["README.md"])
        root = Commit("Initial commit", [], self.staging_area)
        self.commits[root.hash] = root
        self.branches["main"] = root.hash
        self.head = "main"

    def stage_file(self, filename: str, content: str):
        self.staging_area[filename] = content

    def get_head_commit_hash(self) -> Optional[str]:
        if self.head in self.branches:
            return self.branches[self.head]
        return self.commits.get(self.head, None).hash if self.head in self.commits else None

    def commit(self, message: str) -> Commit:
        parent_hash = self.get_head_commit_hash()
        parents = [parent_hash] if parent_hash else []
        new_commit = Commit(message, parents, self.staging_area)
        self.commits[new_commit.hash] = new_commit

        if self.head in self.branches:
            self.branches[self.head] = new_commit.hash
        else:
            self.head = new_commit.hash
        return new_commit

    def create_branch(self, branch_name: str) -> bool:
        if branch_name in self.branches:
            return False
        current_hash = self.get_head_commit_hash()
        if not current_hash:
            return False
        self.branches[branch_name] = current_hash
        return True

    def checkout(self, target: str) -> bool:
        if target in self.branches:
            self.head = target
            current_commit = self.commits[self.branches[target]]
            self.staging_area = dict(current_commit.snapshot)
            self.working_dir = dict(current_commit.snapshot)
            return True
        elif target in self.commits:
            self.head = target  # Detached HEAD
            current_commit = self.commits[target]
            self.staging_area = dict(current_commit.snapshot)
            self.working_dir = dict(current_commit.snapshot)
            return True
        return False

    def is_ancestor(self, ancestor_hash: str, descendant_hash: str) -> bool:
        if ancestor_hash == descendant_hash:
            return True
        visited = set()
        queue = [descendant_hash]
        while queue:
            curr = queue.pop(0)
            if curr == ancestor_hash:
                return True
            if curr in visited or curr not in self.commits:
                continue
            visited.add(curr)
            queue.extend(self.commits[curr].parents)
        return False

    def merge(self, source_branch: str) -> Tuple[str, Optional[Commit]]:
        """
        Merges source_branch into current HEAD branch.
        Returns: (status_message, merge_commit_or_None)
        """
        if source_branch not in self.branches:
            return f"Error: Branch '{source_branch}' does not exist.", None

        current_branch = self.head
        if current_branch not in self.branches:
            return "Error: Cannot merge in detached HEAD state.", None

        target_hash = self.branches[current_branch]
        source_hash = self.branches[source_branch]

        if target_hash == source_hash:
            return "Already up to date.", None

        # Check for Fast-Forward
        if self.is_ancestor(target_hash, source_hash):
            self.branches[current_branch] = source_hash
            self.staging_area = dict(self.commits[source_hash].snapshot)
            return f"Fast-forward merge: {current_branch} -> {source_hash}", self.commits[source_hash]

        # Three-Way Merge
        # Check for conflicts
        target_snap = self.commits[target_hash].snapshot
        source_snap = self.commits[source_hash].snapshot
        merged_snap = dict(target_snap)
        has_conflict = False

        for fname, s_content in source_snap.items():
            if fname in target_snap and target_snap[fname] != s_content:
                has_conflict = True
                merged_snap[fname] = (
                    f"<<<<<<< HEAD ({current_branch})\n"
                    f"{target_snap[fname]}\n"
                    f"=======\n"
                    f"{s_content}\n"
                    f">>>>>>> {source_branch}"
                )
            else:
                merged_snap[fname] = s_content

        if has_conflict:
            self.staging_area = merged_snap
            return f"CONFLICT: Merge conflict detected between '{current_branch}' and '{source_branch}'. Resolution required.", None

        # Clean Three-Way Merge Commit
        parents = [target_hash, source_hash]
        merge_commit = Commit(f"Merge branch '{source_branch}' into {current_branch}", parents, merged_snap)
        self.commits[merge_commit.hash] = merge_commit
        self.branches[current_branch] = merge_commit.hash
        self.staging_area = dict(merged_snap)
        return f"Three-way merge succeeded: created commit {merge_commit.hash}", merge_commit

    def rebase(self, upstream_branch: str) -> Tuple[bool, str]:
        """
        Rebases current branch commits onto upstream_branch.
        """
        if upstream_branch not in self.branches:
            return False, f"Upstream branch '{upstream_branch}' does not exist."

        current_branch = self.head
        if current_branch not in self.branches:
            return False, "Cannot rebase in detached HEAD state."

        curr_hash = self.branches[current_branch]
        upstream_hash = self.branches[upstream_branch]

        if curr_hash == upstream_hash or self.is_ancestor(curr_hash, upstream_hash):
            self.branches[current_branch] = upstream_hash
            return True, f"Rebase fast-forwarded '{current_branch}' onto '{upstream_branch}'."

        # Collect commits unique to current branch
        branch_commits: List[Commit] = []
        pointer = curr_hash
        while pointer and pointer != upstream_hash and not self.is_ancestor(pointer, upstream_hash):
            if pointer in self.commits:
                branch_commits.append(self.commits[pointer])
                pointer = self.commits[pointer].parents[0] if self.commits[pointer].parents else None
            else:
                break

        branch_commits.reverse()
        new_base = upstream_hash

        for c in branch_commits:
            replayed_snap = dict(self.commits[new_base].snapshot)
            replayed_snap.update(c.snapshot)
            replayed = Commit(f"{c.message} (rebased)", [new_base], replayed_snap)
            self.commits[replayed.hash] = replayed
            new_base = replayed.hash

        self.branches[current_branch] = new_base
        return True, f"Successfully rebased {len(branch_commits)} commit(s) onto '{upstream_branch}'."

    def render_graph(self) -> str:
        """Renders an ASCII visualization of the commit DAG and branch pointers."""
        lines = []
        lines.append("🌿 Git Commit Graph (DAG):")
        lines.append("-" * 65)

        # Inverted commit list by dependency order
        ordered = list(self.commits.values())
        for c in reversed(ordered):
            # Identify pointing branch pointers
            pointers = []
            for b_name, b_hash in self.branches.items():
                if b_hash == c.hash:
                    if b_name == self.head:
                        pointers.append(f"HEAD -> {b_name}")
                    else:
                        pointers.append(b_name)

            pointer_str = f" ({', '.join(pointers)})" if pointers else ""
            parents_str = f"parents: {', '.join(c.parents)}" if c.parents else "root"
            is_merge = len(c.parents) > 1

            icon = "🔷" if is_merge else "🟢"
            lines.append(f"  {icon} [{c.hash}] {c.message}{pointer_str}")
            lines.append(f"      └─ {parents_str}")
        lines.append("-" * 65)
        return "\n".join(lines)
