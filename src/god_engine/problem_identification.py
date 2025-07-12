"""
Problem Identification Module for the God Engine.

This module is responsible for analyzing the system to identify potential
areas for improvement and generating new goals.
"""
import os
import json
from pylint.lint import Run
import io
import sys
import subprocess  # For calling external tools


class ProblemIdentificationModule:
    def __init__(self, code_root, goals_config_path, system_monitor):
        self.code_root = code_root
        self.goals_config_path = goals_config_path
        self.system_monitor = system_monitor

    def analyze_codebase(self):
        """
        Analyzes the codebase for potential issues using static analysis (pylint).
        """
        print("ProblemIdentificationModule: Analyzing codebase with pylint...")

        # Redirect stdout to capture pylint's JSON output
        old_stdout = sys.stdout
        sys.stdout = new_stdout = io.StringIO()

        try:
            # Run pylint programmatically on the code_root
            # We explicitly set exit=False to prevent pylint from exiting the process.
            # The output is captured via stdout redirection.
            Run([self.code_root, '--output-format=json', '--reports=n'], exit=False)
            
            # Get the captured output
            pylint_output = new_stdout.getvalue()
            
            # Restore stdout
            sys.stdout = old_stdout

            # Parse the JSON output
            pylint_messages = json.loads(pylint_output)
            
            if not pylint_messages:
                print("ProblemIdentificationModule: Pylint found no issues.")
                return

            for msg in pylint_messages:
                # Construct a more precise goal name
                goal_name = f"{msg['message-id'].lower()}_{os.path.basename(msg['path']).replace('.', '_')}_{msg['line']}"
                
                # Determine target file relative to code_root
                target_file_relative = os.path.relpath(msg['path'], self.code_root)

                # Create a description and completion criteria based on the message
                description = f"Pylint: {msg['message']} in {msg['path']} at line {msg['line']} (ID: {msg['message-id']})"
                
                # Placeholder patch logic and completion criteria for now
                # Read the target file content to get the specific line for completion criteria
                try:
                    with open(os.path.join(self.code_root, target_file_relative), "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        # Pylint line numbers are 1-based
                        if 0 < msg['line'] <= len(lines):
                            target_line_content = lines[msg['line'] - 1]
                        else:
                            print(f"ProblemIdentificationModule: Warning - Line number {msg['line']} out of bounds for {target_file_relative}.")
                            target_line_content = "" # Fallback if line number is invalid
                except Exception as e:
                    print(f"ProblemIdentificationModule: Error reading line {msg['line']} from {target_file_relative}: {e}")
                    target_line_content = "" # Fallback if file cannot be read

                # Placeholder patch logic and completion criteria for now
                # These would be refined based on the type of pylint message
                patch_logic = f"# TODO: Implement fix for {msg['message-id']}"
                completion_criteria = f"# Fixed: {msg['message-id']}" # Default, will be overridden for specific types

                # Specific handling for C0303 (trailing-whitespace)
                if msg['message-id'] == 'C0303':
                    # The completion criteria is the line without any leading/trailing whitespace or newline characters.
                    completion_criteria = target_line_content.strip()

                    # Patch logic indicates a fix-in-place operation for this type of issue
                    patch_logic = "FIX_TRAILING_WHITESPACE"
                    print(f"ProblemIdentificationModule: C0303 - Original line: "
                          f"{repr(target_line_content)}, Completion criteria: "
                          f"{repr(completion_criteria)}")
                elif msg['message-id'] == 'C0114':  # Missing module docstring
                    completion_criteria = (
                        f"\"\"\"{os.path.basename(msg['path']).replace('.py', '')} "
                        "module.\"\"\""
                    )
                    patch_logic = "ADD_MODULE_DOCSTRING"
                elif msg['message-id'] == 'C0115':  # Missing class docstring
                    completion_criteria = (
                        f"\"\"\"Docstring for {msg['obj']} class.\"\"\""
                    )
                    patch_logic = "ADD_CLASS_DOCSTRING"
                elif msg['message-id'] == 'C0116':  # Missing function/method docstring
                    completion_criteria = (
                        f"\"\"\"Docstring for {msg['obj']} function/method.\"\"\""
                    )
                    patch_logic = "ADD_FUNCTION_DOCSTRING"
                elif msg['message-id'] == 'C0411':  # Wrong import order
                    patch_logic = "FIX_IMPORT_ORDER"
                    completion_criteria = (
                        f"Fixed import order in {target_file_relative}"
                    )
                elif msg['message-id'] == 'W0611':  # Unused import
                    patch_logic = "REMOVE_UNUSED_IMPORT"
                    completion_criteria = (
                        f"Removed unused import in {target_file_relative} at "
                        f"line {msg['line']}"
                    )
                elif msg['message-id'] == 'C0301':  # Line too long
                    patch_logic = "FIX_LINE_LENGTH"
                    completion_criteria = (
                        f"Fixed line length in {target_file_relative} at "
                        f"line {msg['line']}"
                    )
                elif msg['message-id'] == 'W0107':  # Unnecessary pass
                    patch_logic = "REMOVE_UNNECESSARY_PASS"
                    completion_criteria = (
                        f"Removed unnecessary pass statement in {target_file_relative} "
                        f"at line {msg['line']}"
                    )
                elif msg['message-id'] == 'R1705':  # Unnecessary else/return
                    patch_logic = "SIMPLIFY_IF_ELSE_RETURN"
                    completion_criteria = (
                        f"Simplified unnecessary else/return in {target_file_relative} "
                        f"at line {msg['line']}"
                    )
                elif msg['message-id'] == 'W0718':  # Too general exception
                    patch_logic = "SPECIFY_EXCEPTION_TYPE"
                    completion_criteria = (
                        f"Specified exception type in {target_file_relative} "
                        f"at line {msg['line']}"
                    )
                elif msg['message-id'] == 'W0122':  # Use of exec
                    patch_logic = "REMOVE_EXEC_USE"
                    completion_criteria = (
                        f"Removed use of exec in {target_file_relative} at "
                        f"line {msg['line']}"
                    )
                elif msg['message-id'] == 'W0511':  # TODO comment
                    patch_logic = "HANDLE_TODO_COMMENT"
                    completion_criteria = (
                        f"Handled TODO comment in {target_file_relative} at "
                        f"line {msg['line']}"
                    )
                elif msg['message-id'] == 'R0903': # Too few public methods
                    patch_logic = "ADD_PUBLIC_METHOD_PLACEHOLDER"
                    completion_criteria = (
                        f"Added public method placeholder in {target_file_relative} "
                        f"at line {msg['line']}"
                    )
                elif msg['message-id'] == 'R0902': # Too many attributes
                    patch_logic = "REFACTOR_ATTRIBUTES_TO_CLASS"
                    completion_criteria = (
                        f"Refactored attributes in {target_file_relative} "
                        f"at line {msg['line']}"
                    )
                elif msg['message-id'] == 'R0913': # Too many arguments
                    patch_logic = "REFACTOR_ARGS_TO_DICT"
                    completion_criteria = (
                        f"Refactored arguments in {target_file_relative} "
                        f"at line {msg['line']}"
                    )
                elif msg['message-id'] == 'R0917': # Too many positional arguments
                    patch_logic = "REFACTOR_POSITIONAL_ARGS"
                    completion_criteria = (
                        f"Refactored positional arguments in {target_file_relative} "
                        f"at line {msg['line']}"
                    )
                elif msg['message-id'] == 'R0911': # Too many return statements
                    patch_logic = "SIMPLIFY_RETURN_STATEMENTS"
                    completion_criteria = (
                        f"Simplified return statements in {target_file_relative} "
                        f"at line {msg['line']}"
                    )
                elif msg['message-id'] == 'R0912': # Too many branches
                    patch_logic = "REFACTOR_TOO_MANY_BRANCHES"
                    completion_criteria = (
                        f"Refactored too many branches in {target_file_relative} "
                        f"at line {msg['line']}"
                    )
                elif msg['message-id'] == 'R0915': # Too many statements
                    patch_logic = "REFACTOR_TOO_MANY_STATEMENTS"
                    completion_criteria = (
                        f"Refactored too many statements in {target_file_relative} "
                        f"at line {msg['line']}"
                    )
                # Add more specific handling for other Pylint message types as needed

                new_goal_data = {
                    "name": goal_name,
                    "description": description,
                    "target_file": target_file_relative,
                    "patch_logic": patch_logic,  # This is now more dynamic
                    "completion_criteria": completion_criteria,
                    "priority": 1,  # Default priority, can be adjusted based on message type
                    "effort": 1,   # Default effort, can be adjusted
                    "validation_command": (
                        f"pytest tests/test_{os.path.basename(msg['path']).replace('.py', '')}.py"  # Basic validation
                    )
                }

                # Assign priorities based on message type
                if msg['type'] == 'error':
                    new_goal_data['priority'] = 10
                elif msg['type'] == 'warning':
                    new_goal_data['priority'] = 7
                elif msg['type'] == 'refactor':
                    new_goal_data['priority'] = 5
                elif msg['type'] == 'convention':
                    new_goal_data['priority'] = 3
                elif msg['type'] == 'design': # For R0902, R0903, R0913, R0917
                    new_goal_data['priority'] = 6
                elif msg['type'] == 'complexity': # For R0911, R0912, R0915
                    new_goal_data['priority'] = 8

                self.generate_new_goal(new_goal_data)

        except json.JSONDecodeError as e:
            sys.stdout = old_stdout # Ensure stdout is restored even on error
            print(f"ProblemIdentificationModule: Failed to parse pylint JSON output: {e}")
            print(f"Raw pylint output: {pylint_output}")
        except Exception as e:
            sys.stdout = old_stdout # Ensure stdout is restored even on error
            print(f"ProblemIdentificationModule: Pylint analysis or goal generation failed: {e}")

    def generate_new_goal(self, new_goal_data):
        """
        Adds a new goal to the goals.json configuration file.
        """
        print(f"ProblemIdentificationModule: Generating new goal: {new_goal_data['name']}")
        
        with open(self.goals_config_path, "r+", encoding="utf-8") as f:
            goals = json.load(f)
            if new_goal_data["name"] not in goals:
                goals[new_goal_data["name"]] = new_goal_data
                f.seek(0)
                json.dump(goals, f, indent=4)
                f.truncate()
                print(f"ProblemIdentificationModule: Successfully added new goal '{new_goal_data['name']}'.")
            else:
                print(f"ProblemIdentificationModule: Goal '{new_goal_data['name']}' already exists.")
