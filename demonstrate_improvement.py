import os
import sys

# Add the parent directory of 'src' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from god_engine.self_improvement import SelfImprovementModule
from god_engine.problem_identification import ProblemIdentificationModule
from god_engine.experimentation_engine import ExperimentationEngine

def demonstrate():
    print("--- Starting Self-Improvement Demonstration ---")
    
    code_root_path = os.path.abspath(os.path.join(os.getcwd(), "src", "god_engine"))
    goals_config_path = os.path.abspath(os.path.join(code_root_path, "goals.json"))
    
    # --- Initialization ---
    si_module = SelfImprovementModule(
        code_root=code_root_path, 
        snapshot_dir="./snapshots", 
        goals_config_path=goals_config_path
    )
    
    problem_identifier = ProblemIdentificationModule(
        code_root=code_root_path,
        goals_config_path=goals_config_path,
        system_monitor=si_module.system_monitor
    )

    exp_engine = ExperimentationEngine(
        code_root=code_root_path,
        goals_config_path=goals_config_path,
        system_monitor=si_module.system_monitor
    )

    # --- Step 1: Autonomous Problem Identification ---
    print("\n--- Phase 1: Autonomous Problem Identification ---")
    problem_identifier.analyze_codebase()
    print("--- End of Phase 1 ---")

    # --- Step 2: Proactive Experimentation ---
    print("\n--- Phase 2: Proactive Experimentation ---")
    # This is a sample hypothesis. In a real system, these would be generated dynamically.
    sample_hypothesis = {
        "name": "optimize_utils_with_numpy",
        "description": "Optimize list operations in utils.py using numpy.",
        "target_file": "utils.py", # Corrected to be relative to code_root
        "patch_logic": "# TODO: Implement numpy optimization",
        "completion_criteria": "import numpy as np",
        "priority": 9,
        "effort": 6,
        "validation_command": "pytest tests/test_utils.py",
        "capability": "capability_algorithmic_efficiency"
    }
    exp_engine.run_experiment(sample_hypothesis)
    print("--- End of Phase 2 ---")

    # --- Reload GoalManager to recognize new goals ---
    from god_engine.goal_manager import GoalManager
    si_module.goal_manager = GoalManager(goals_config_path, si_module.system_monitor, si_module.protected_modules)


    # --- Step 3: Self-Improvement Cycle ---
    print("\n--- Phase 3: Executing Self-Improvement Cycle ---")
    success = si_module.perform_self_improvement()
    print("--- End of Phase 3 ---")

    # --- Step 4: Verification and Demonstration ---
    if success:
        print("\n--- Phase 4: Verifying Final State ---")
        all_goals_met_overall = True
        
        from god_engine.goal_manager import GoalManager
        final_goal_manager = GoalManager(goals_config_path, si_module.system_monitor, si_module.protected_modules)

        for goal_name, goal_obj in final_goal_manager.available_goals.items():
            is_met = goal_name in si_module.improvements_made or si_module.self_evaluate(goal_name)
            status = "COMPLETED" if is_met else "PENDING"
            
            print(f"  - Goal '{goal_name}': '{goal_obj.description}' - {status}.")
            
            if not is_met:
                all_goals_met_overall = False
        
        if all_goals_met_overall:
            print("\nConclusion: All defined self-improvement goals have been met.")
        else:
            print("\nConclusion: Some goals are still pending.")
            
    else:
        print("\nSelf-improvement process failed.")

    print("\n--- End of Demonstration ---")

if __name__ == "__main__":
    demonstrate()
