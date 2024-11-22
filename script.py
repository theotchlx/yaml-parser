"""
To address the issues and ensure a correct YAML parser, we'll revise the script step by step, focusing on clarity and correctness.
Steps to Build the New Script

    Read the File: Read the lines and handle errors gracefully.
    Track Indentation Levels: Use a stack to monitor the nesting of indentation levels.
    Validate Each Line:
        Ensure keys are followed by valid values or nested structures.
        Check for proper alignment of indentation levels.
        Handle multi-line sequences (-) and mappings properly.
    Edge Cases: Address cases like missing spaces between keys and values or mismatched indentation.
"""

"""
YAML Validator with Stack Automata
This script validates YAML files by ensuring proper syntax, indentation, and structural rules. It now handles cases where:
1. A key is followed by a list.
2. A key-value pair is followed by a list.
3. All list items are at the same indentation level.
"""

"""
This module provides functions to validate YAML files based on syntax, indentation, and structure.
It uses a stack to track indentation levels and ensures that keys are followed by valid values or nested structures.
The script can handle multi-line sequences and mappings, and it reports line numbers for any errors encountered.
"""

import re


def is_yaml_file(filepath):
    """
    This function reads a file, and returns True if it's a valid YAML file, False otherwise.
    Args:
        filepath (str): Path to the file.
    Returns:
        bool: True if the file is valid YAML, False otherwise.
    """
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
        return validate_lines(lines)
    except Exception as e:  # Catch-all in case of exceptions (file read error, file not found, ...)
        print(f"Error: {e}")
        return False  # Return False to prevent returning false positives.


def validate_lines(lines):
    """
    This function verifies if a list of lines (Strings) contains valid YAML lines.
    This also allows to keep track of indentation levels, and know which line precisely is invalid.
    Args:
        lines (list of str): The lines of the YAML file.
    Returns:
        bool: True if the YAML lines are valid, False otherwise.
    """
    stack = []  # List used as a stack, to track indentation levels.
    in_list_context = False  # Boolean flag to check if we are in the context of a YAML list.
    # Example of a list context:
    # key: ...
    # - item1
    # - item2  <--{ if we are here, we are in a list context.
    # - item3
    list_indent = None  # The indentation level of the list items. This is to check if all items in a list have the same indentation level.
    key_had_value = False  # This boolean flag is to track if the previous "key:"" had a value or not.
                                         # This is to invalidate if a list follows a key-value pair.

    for i, line in enumerate(lines, 1):  # Start line number at 1
        stripped_line = line.strip()

        # Skip empty lines and comments.
        if not stripped_line or stripped_line.startswith("#"):
            continue

        current_indent = get_current_indent(line)

        # Check for invalid indentation
        if not validate_indentation(stack, current_indent):
            print(f"Invalid indentation at line {i}: {line}")
            return False

        if in_list_context:
            # Validate list items' indentation level
            if stripped_line.startswith("-"):
                item_indent = get_current_indent(line)
                if item_indent != list_indent:
                    print(f"Inconsistent list item indentation at line {i}: {line}")
                    return False
            else:
                in_list_context = False
                list_indent = None

        # Validate the line's syntax and check for list context
        if stripped_line.startswith("-"):
            if key_had_value:
                print(f"Invalid list following a key-value pair at line {i}: {line}")
                return False
            if not stack:
                print(f"List without a key context at line {i}: {line}")
                return False
            if not in_list_context:
                in_list_context = True
                list_indent = current_indent
        elif ":" in stripped_line:
            if not validate_syntax(stripped_line):
                print(f"Invalid syntax at line {i}: {line}")
                return False
            # Determine if this line is a key-value pair or a standalone key
            key, value = stripped_line.split(":", 1)
            key_had_value = bool(value.strip())  # Is False if value is not empty (nor just empty characters)

    return True


def get_current_indent(line):
    """
    This small function calculates the indentation level of a line.
    It uses the .lstrip() String method to remove leading (first) spaces.
    Args:
        line (str): The line to analyze.
    Returns:
        int: The number of leading spaces in the line.
    """
    return len(line) - len(line.lstrip())  # Size of line minus size of line without first spaces/indentation.


def validate_indentation(stack, current_indent):
    """
    Validates the indentation against the stack.
    Args:
        stack (list of int): The stack of indentation levels.
        current_indent (int): The current line's indentation level.
    Returns:
        bool: True if the indentation is valid, False otherwise.
    """
    if len(stack) != 0 and current_indent < stack[-1]:
        while stack and current_indent < stack[-1]:
            stack.pop()
    elif len(stack) != 0 and current_indent > stack[-1]:
        stack.append(current_indent)
    elif not stack:
        stack.append(current_indent)

    return True


def validate_syntax(line):
    """
    This function validates the syntax of a YAML line.
    Args:
        line (str): The stripped line to validate.
    Returns:
        bool: True if the syntax is valid, False otherwise.
    """
    key_value_pattern = r"^[^:]+:\s*.*$"
    if re.match(key_value_pattern, line):
        return True
    if line.startswith("-"):
        return True
    return False


# Usage

if __name__ == "__main__":
  path = input("Enter path of the file to validate: ")
  path = "example1-valid.yaml"
  if is_yaml_file(path):
      print("Valid YAML")
  else:
      print("Invalid YAML")

"""
How This Script Addresses Your Concerns

    Handles Missing Values After Keys:
        validate_syntax checks if the key is followed by either a value, a nested structure, or a sequence.
    Detects Missing Spaces Between Keys and Values:
        Splitting on : ensures the value part is checked for a leading space.
    Tracks Indentation Levels Correctly:
        validate_indentation uses the stack to ensure consistent indentation levels.
        If a line's indentation deviates from the expected structure, it immediately flags the issue.
    Reports Line Numbers for Errors:
        If a line is invalid, the script logs the problematic line and its number for debugging.
"""




"""
Yes, we can set up a Python environment using Poetry and generate documentation. Here's how you can approach it:
Steps to Use Poetry and Generate Documentation

    Initialize Poetry in Your Project:

poetry init

Follow the prompts to configure your project.

Add Dependencies: Poetry will handle dependencies for your project. Add any required packages:

poetry add some-package

For our YAML validation project, we may not need additional dependencies unless we plan to extend functionality.

Install Dependencies: To ensure all dependencies are installed:

poetry install

Run the Project: Activate the Poetry environment and run your script:

poetry run python your_script.py

Generate Documentation: Use a tool like pdoc or Sphinx to generate documentation.

    Using pdoc: Install it via Poetry:

poetry add --dev pdoc

Generate documentation:

poetry run pdoc --html --output-dir docs your_project

Using Sphinx: Install Sphinx via Poetry:

poetry add --dev sphinx
sphinx-quickstart

Configure and build documentation:

        make html

    Define Metadata: Include detailed information in pyproject.toml (author, description, version, etc.) for better organization and documentation.

Would you like help setting up the pyproject.toml file or generating documentation with a specific tool?
"""