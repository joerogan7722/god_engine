"""
Manages the definition, tracking, and selection of self-improvement goals for the God Engine.
"""
import json
import os
from god_engine.system_monitor import SystemMonitor

class Goal:
    """
    Represents a self-improvement goal with its definition and criteria.
    """
    def __init__(self, name, description, target_file, patch_logic, completion_criteria, priority=1, effort=1):
        self.name = name
        self.description = description
        self.target_file = target_file
        self.patch_logic = patch_logic
        self.completion_criteria = completion_criteria # A string or callable to evaluate success
        self.priority = priority
        self.effort = effort
        self.score = self.priority / self.effort if self.effort > 0 else self.priority

class GoalManager:
    """
    Loads, tracks, and provides access to defined self-improvement goals.
    """
    def __init__(self, goals_config_path, system_monitor, protected_modules=None):
        self.goals_config_path = goals_config_path
        self.protected_modules = protected_modules if protected_modules is not None else set()
        self.system_monitor = system_monitor
        self.available_goals = {} # {goal_name: Goal object}
        self._load_goals_config()

    def _load_goals_config(self):
        """Loads goals from a JSON configuration file."""
        if not os.path.exists(self.goals_config_path):
            print(f"Warning: Goals configuration file not found at {self.goals_config_path}. No goals loaded.")
            return

        with open(self.goals_config_path, "r", encoding="utf-8") as f:
            goals_data = json.load(f)
        
        for goal_name, data in goals_data.items():
            self.available_goals[goal_name] = Goal(
                name=goal_name,
                description=data.get("description", ""),
                target_file=data.get("target_file"),
                patch_logic=data.get("patch_logic"),
                completion_criteria=data.get("completion_criteria"),
                priority=data.get("priority", 1),
                effort=data.get("effort", 1)
            )
        print(f"Loaded {len(self.available_goals)} goals from {self.goals_config_path}.")

    def get_goal(self, goal_name):
        """Returns a specific Goal object by name."""
        return self.available_goals.get(goal_name)

    def get_next_pending_goal(self, completed_goals, code_root):
        """
        Determines the next goal to pursue based on a dynamic scoring algorithm.
        The score is adjusted based on real-time data from the SystemMonitor.
        """
        pending_goals = [goal for name, goal in self.available_goals.items() if name not in completed_goals]

        if not pending_goals:
            return None

        # Get current system metrics
        error_rates = self.system_monitor.get_error_rates()
        bottlenecks = dict(self.system_monitor.get_performance_bottlenecks())

        # Dynamically adjust scores
        for goal in pending_goals:
            dynamic_priority = goal.priority
            
            # Increase priority for goals targeting error-prone modules
            target_module = os.path.basename(goal.target_file)
            if target_module in error_rates:
                error_bonus = error_rates[target_module] * 2 # Bonus for each error
                dynamic_priority += error_bonus
                print(f"Goal '{goal.name}' priority boosted by {error_bonus} due to errors in {target_module}.")

            # Increase priority for goals that optimize bottlenecks
            # (This is a simple heuristic; could be more sophisticated)
            if "optimize" in goal.name.lower() and goal.target_file in str(bottlenecks):
                 dynamic_priority += 5 # Flat bonus for targeting an optimization
                 print(f"Goal '{goal.name}' priority boosted for targeting a performance bottleneck.")

            goal.score = dynamic_priority / goal.effort if goal.effort > 0 else dynamic_priority

        pending_goals.sort(key=lambda g: g.score, reverse=True)

        for goal in pending_goals:
            target_file_path = os.path.abspath(os.path.join(code_root, goal.target_file))
            if os.path.exists(target_file_path):
                print(f"Selected highest-scoring goal: '{goal.name}' (Score: {goal.score:.2f})")
                return goal
            else:
                print(f"Warning: Target file for goal '{goal.name}' not found at {target_file_path}. Skipping.")

        return None
