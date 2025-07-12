"""
Experimentation Engine for the God Engine.

This module is responsible for generating and testing hypotheses for
potential improvements to the system's core capabilities.
"""
import os
import json
import subprocess


class ExperimentationEngine:
    def __init__(self, code_root, goals_config_path, system_monitor):
        self.code_root = code_root
        self.goals_config_path = goals_config_path
        self.system_monitor = system_monitor

    def run_experiment(self, hypothesis):
        """
        Runs an experiment to test a hypothesis.
        """
        print(f"ExperimentationEngine: Running experiment for hypothesis: "
              f"{hypothesis['name']}")

        original_file_path = hypothesis["target_file"]
        patch_content = hypothesis["patch_logic"]
        # Default to pytest
        validation_command = hypothesis.get("validation_command", "pytest")

        # Backup the original file
        backup_file_path = f"{original_file_path}.bak"
        if os.path.exists(original_file_path):
            with open(original_file_path, 'r', encoding='utf-8') as f_orig:
                original_content = f_orig.read()
            with open(backup_file_path, 'w', encoding='utf-8') as f_bak:
                f_bak.write(original_content)
            print(f"ExperimentationEngine: Backed up {original_file_path} to "
                  f"{backup_file_path}")
        else:
            print(f"ExperimentationEngine: Warning: Target file {original_file_path} "
                  f"does not exist. Creating it.")
            # No original content to backup
            original_content = ""

        success = False
        try:
            # Apply the patch (for now, simple overwrite/append)
            # This needs to be more sophisticated for real patching (e.g., diff/patch)
            # For the current Pylint fixes, patch_logic is often the corrected content
            print(f"ExperimentationEngine: Applying patch to {original_file_path}")
            with open(original_file_path, 'w', encoding='utf-8') as f_target:
                f_target.write(patch_content)

            # Run validation command (e.g., pytest)
            print(f"ExperimentationEngine: Running validation command: {validation_command}")
            result = subprocess.run(
                validation_command,
                shell=True,
                capture_output=True,
                text=True,
                # Run tests from the project root
                cwd=self.code_root
            )
            print(f"Validation Output:\n{result.stdout}")
            if result.stderr:
                print(f"Validation Errors:\n{result.stderr}")

            if result.returncode == 0:
                print(f"ExperimentationEngine: Validation successful for "
                      f"'{hypothesis['name']}'.")
                success = True
            else:
                print(f"ExperimentationEngine: Validation failed for "
                      f"'{hypothesis['name']}'.")

            # Placeholder for actual performance measurement
            performance_gain = "N/A"

            if success:
                print(f"ExperimentationEngine: Hypothesis '{hypothesis['name']}' "
                      f"was successful.")
                self.generate_goal_from_hypothesis(hypothesis, performance_gain)
            else:
                print(f"ExperimentationEngine: Hypothesis '{hypothesis['name']}' failed.")
            return success
        except Exception as e:
            print(f"ExperimentationEngine: An error occurred during experiment: {e}")
            return False
        finally:
            # Revert changes by restoring the backup
            if os.path.exists(backup_file_path):
                print(f"ExperimentationEngine: Restoring original file from "
                      f"{backup_file_path}")
                os.replace(backup_file_path, original_file_path)
            # If original file didn't exist and experiment failed, delete the created file
            elif not success and os.path.exists(original_file_path) and original_content == "":
                os.remove(original_file_path)

    def generate_goal_from_hypothesis(self, hypothesis, performance_gain):
        """
        Generates a new goal in goals.json based on a successful experiment.
        """
        new_goal = {
            "description": hypothesis["description"],
            "target_file": hypothesis["target_file"],
            "patch_logic": hypothesis["patch_logic"],
            "completion_criteria": hypothesis["completion_criteria"],
            "priority": hypothesis["priority"],
            "effort": hypothesis["effort"],
            "validation_command": hypothesis["validation_command"],
            "associated_capability": hypothesis["capability"],
            "experiment_summary": {
                "hypothesis": hypothesis["name"],
                "result": "SUCCESS",
                "performance_gain": performance_gain
            }
        }

        print(f"ExperimentationEngine: Generating new goal: {hypothesis['name']}")
        with open(self.goals_config_path, "r+", encoding="utf-8") as f:
            goals = json.load(f)
            if hypothesis["name"] not in goals:
                goals[hypothesis["name"]] = new_goal
                f.seek(0)
                json.dump(goals, f, indent=4)
                f.truncate()
                print(f"ExperimentationEngine: Successfully added new goal "
                      f"'{hypothesis['name']}'.")
            else:
                print(f"ExperimentationEngine: Goal '{hypothesis['name']}' already exists.")
