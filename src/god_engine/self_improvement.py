# self_improvement.py
import os
import subprocess
from pathlib import Path

try:
    from google.cloud import aiplatform as vertex_ai
except ImportError:
    vertex_ai = None

from vertexai.preview.generative_models import GenerativeModel

from god_engine.goal_manager import GoalManager
from god_engine.problem_identification import generate_goals_from_todos


class SelfImprovementModule:
    """
    Orchestrates dynamic goal management, problem identification,
    and Gemini-driven patch generation focused on capability & autonomy.
    """

    def __init__(self, cfg: dict):
        # Load config
        self.code_dir = Path(cfg["code_dir"])
        self.mem_file = Path(cfg["memory_path"])
        self.max_cycles = cfg["max_cycles"]
        # Init goal manager
        self.goals = GoalManager(cfg.get("goals_path", "goals.json"))
        # Bootstrap any new TODOs as goals by analyzing the codebase
        new_goals = generate_goals_from_todos(str(self.code_dir))
        for goal_data in new_goals:
            if not any(g.id == goal_data["id"] for g in self.goals.goals):
                self.goals.add_goal_from_dict(goal_data)
        
        # Gemini client setup
        if vertex_ai:
            vertex_ai.init(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = GenerativeModel("gemini-1.5-pro")
        else:
            self.model = None
        # Memory of applied goals
        self.memory = (
            set(self.mem_file.read_text().splitlines())
            if self.mem_file.exists()
            else set()
        )

    def _save_memory(self):
        self.mem_file.write_text("\n".join(self.memory))

    def _call_gemini(self, prompt: str) -> str:
        """
        Send a feature-driven request to Gemini and return the unified-diff patch.
        """
        if not self.model:
            return ""
        # Ensure your GEMINI_API_KEY is set in the env
        response = self.model.generate_content(prompt)
        # Gemini returns a list of predictions; we expect one unified diff
        content = response.text
        # Some trimming/hygiene: ensure it starts with diff header
        if not content.startswith("diff") and "+++" in content:
            # try to locate first '+++'
            idx = content.find("+++")
            content = content[idx:]
        return content

    def improve(self):
        for _ in range(self.max_cycles):
            goal = self.goals.next_goal()
            if not goal:
                break  # no more pending goals

            # Skip if already attempted
            if goal.id in self.memory:
                continue

            # Build prompt: describe codebase + ask for patch
            prompt = (
                f"# Goal ID: {goal.id}\n"
                f"# Description: {goal.description}\n"
                "Generate a unified-diff patch to implement this capability, "
                "prioritizing autonomy and resilience.\n"
                f"# Base path: {self.code_dir}\n"
            )
            patch = self._call_gemini(prompt)

            # Attempt to apply & test
            applied = self._apply_patch(patch)
            if applied and self._run_tests():
                self.goals.mark_done(goal.id)
            else:
                # revert if tests fail
                self._git_reset_all()
            self.memory.add(goal.id)

        self._save_memory()
        self.goals.save()

    def _apply_patch(self, patch_text: str) -> bool:
        """Applies a patch to the codebase."""
        if not patch_text:
            return False
        try:
            # Create a temporary patch file in the current working directory (project root)
            patch_file_path = Path("./temp.patch")
            patch_file_path.write_text(patch_text)

            # Apply the patch using git from the project root
            subprocess.run(
                ["git", "apply", str(patch_file_path)],
                check=True,
                cwd=".",  # Execute from the current working directory (project root)
                capture_output=True,
            )
            patch_file_path.unlink()  # Delete the temporary patch file
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error applying patch: {e}")
            if isinstance(e, subprocess.CalledProcessError):
                print(e.stderr.decode())
            return False

    def _run_tests(self) -> bool:
        """Runs the test suite."""
        try:
            subprocess.run(
                ["pytest"], check=True, cwd=".", capture_output=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Tests failed: {e}")
            print(e.stderr.decode())
            return False

    def _git_reset_all(self):
        """Resets all changes in the git repository."""
        try:
            subprocess.run(
                ["git", "reset", "--hard"],
                check=True,
                cwd=".",
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error resetting git: {e}")
            print(e.stderr.decode())
