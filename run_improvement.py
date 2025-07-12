import sys
from pathlib import Path

# Add the parent directory of src to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from god_engine.self_improvement import SelfImprovementModule

# Ensure your config.yaml is correctly set up, e.g.:
# self_improvement:
#   code_dir:       "src/god_engine"
#   memory_path:    ".sim_memory"
#   max_cycles:     3
#   goals_path:     "src/god_engine/goals.json"

config = {
    "code_dir": "src/god_engine",
    "memory_path": ".sim_memory",
    "max_cycles": 1,  # Run for one cycle to observe the immediate effect
    "goals_path": "src/god_engine/goals.json",
}

if __name__ == "__main__":
    print("Starting God Engine self-improvement cycle...")
    sim_module = SelfImprovementModule(config)
    sim_module.improve()
    print("Self-improvement cycle completed.")
