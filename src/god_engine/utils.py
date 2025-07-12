import numpy as np
"""
Helpers: safe patch, JSON diff, sandbox runner.
"""
# TODO: add anti-tamper code integrity checker with auto-restore snapshot
import hashlib
import os
import json  # For persistent storage of checksums and content

def calculate_checksum(file_path, buffer_size=4096):
    """Calculates the SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(buffer_size), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

class CodeIntegrityChecker:
    def __init__(self, snapshot_dir):
        self.snapshot_dir = snapshot_dir
        self.snapshot_index_file = os.path.join(snapshot_dir, "snapshots_index.json")
        self.snapshots = {}  # Store {file_path: {"checksum": str, "snapshot_file": str}}
        self._load_snapshots_index()

    def _get_snapshot_path(self, file_path):
        """Generates a unique snapshot file path within the snapshot directory."""
        file_name = os.path.basename(file_path)
        path_hash = hashlib.md5(file_path.encode()).hexdigest()
        return os.path.join(self.snapshot_dir, f"{file_name}.{path_hash}.snapshot")

    def _load_snapshots_index(self):
        """Loads the snapshot index from disk."""
        if os.path.exists(self.snapshot_index_file):
            with open(self.snapshot_index_file, "r", encoding="utf-8") as f:
                self.snapshots = json.load(f)
        print(f"Loaded snapshot index: {len(self.snapshots)} entries.")

    def _save_snapshots_index(self):
        """Saves the snapshot index to disk."""
        if not os.path.exists(self.snapshot_dir):
            os.makedirs(self.snapshot_dir)
        with open(self.snapshot_index_file, "w", encoding="utf-8") as f:
            json.dump(self.snapshots, f, indent=4)
        print(f"Saved snapshot index: {len(self.snapshots)} entries.")



    def take_snapshot(self, file_path):
        """Takes a snapshot of a file's checksum and content, persisting it to disk."""
        if not os.path.exists(self.snapshot_dir):
            os.makedirs(self.snapshot_dir)

        checksum = calculate_checksum(file_path)

        # Read content and save it to a dedicated snapshot file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        snapshot_file_path = self._get_snapshot_path(file_path)
        with open(snapshot_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Update the in-memory index and save it to disk
        self.snapshots[file_path] = {
            "checksum": checksum,
            "snapshot_file": snapshot_file_path
        }
        self._save_snapshots_index()

        print(f"Snapshot for {file_path} created with checksum {checksum}")

    def verify_integrity(self, file_path):
        """Verifies the integrity of a file against its stored snapshot checksum."""
        if file_path not in self.snapshots:
            print(f"Warning: No snapshot found for {file_path}. Cannot verify integrity.")
            return True  # No baseline to compare against

        stored_checksum = self.snapshots[file_path]["checksum"]
        current_checksum = calculate_checksum(file_path)

        if current_checksum != stored_checksum:
            print(f"TAMPERING DETECTED: Checksum mismatch for {file_path}.")
            return False
        return True


    def auto_restore(self, file_path):
        """Restores a file from its trusted snapshot file if tampering is detected."""
        if file_path not in self.snapshots:
            print(f"Error: Cannot restore {file_path}. No snapshot available.")
            return False

        snapshot_file_path = self.snapshots[file_path]["snapshot_file"]
        if not os.path.exists(snapshot_file_path):
            print(f"Error: Snapshot file not found at {snapshot_file_path}. Cannot restore.")
            return False

        try:
            with open(snapshot_file_path, "r", encoding="utf-8") as sf:
                trusted_content = sf.read()

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(trusted_content)

            print(f"Restored {file_path} from trusted snapshot.")
            # After restoring, re-take the snapshot to update the checksum in the index
            # This ensures the restored file's new checksum is the new trusted state.
            self.take_snapshot(file_path)
            return True
        except IOError as e:
            print(f"Error restoring {file_path}: {e}")
            return False

def run_in_sandbox(code_string, globals_dict=None, locals_dict=None):
    """
    Executes a string of code in a restricted sandbox environment.
    WARNING: This is a highly simplified and INSECURE sandbox.
    For production, consider using dedicated sandboxing libraries (e.g., RestrictedPython),
    process isolation (e.g., subprocess with strict permissions), or containerization (e.g., Docker).
    """
    if globals_dict is None:
        # Restrict built-ins to a minimal set for basic safety
        # This is not exhaustive and can be bypassed by sophisticated attacks.
        safe_builtins = {
            'print': print,
            'len': len,
            'range': range,
            'Exception': Exception,
            'TypeError': TypeError,
            'ValueError': ValueError,
            '__import__': __import__,  # Required for modules to import other modules
            '__build_class__': __build_class__,  # Required for class definition
            # Add other necessary built-ins as needed, with caution
        }
        globals_dict = {"__builtins__": safe_builtins}


    # Add necessary modules to globals for the executed code
    # This exposes the actual logging module, which is a security consideration in a real sandbox.
    globals_dict['logging'] = __import__('logging')
    globals_dict['logging.handlers'] = __import__('logging.handlers')
    globals_dict['__name__'] = '__main__'  # Provide a __name__ for the executed module


    if locals_dict is None:
        locals_dict = {}

    try:
        # Execute the code string within the restricted environment
        exec(code_string, globals_dict, locals_dict)
        print("Code executed successfully in sandbox.")
        return True, "Execution successful."
    except Exception as e:
        print(f"Sandbox execution failed: {e}")
        return False, str(e)


def greet(name):
    """
    A simple greeting function added by the Self-Improvement Module.
    """
    return f"Hello, {name}! This function was added by the God Engine's self-improvement system."

def process_data(data_list):
    """
    A hypothetical complex function to be refactored.
    # TODO: Refactor this function
    """
    result = 0
    for item in data_list:
        if isinstance(item, (int, float)):
            result += item * 2
        else:
            result += 1
    return result

def list_sum_optimization(data_list):
    """
    Optimized: A hypothetical function for list sum optimization using NumPy.
    """
    return np.sum(data_list)
