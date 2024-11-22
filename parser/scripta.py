import sys

class YAMLValidator:
    def __init__(self):
        self.stack = []
          # Stack to keeps track of each indentation levels of the lines. Example:
          # foo:                            # stack = [0]
          #   - bar:                        # stack = [0, 1]
          #       one: "This. Is. YAML!!"   # stack = [0, 1, 3]
          #       twoo: woaw based          # stack = [0, 1, 3]
          #       threee: 1993              # stack = [0, 1, 3]
        self.current_indent = 0
          # These attributes allow us to make sure indentation is consistent, and that each list or nested list has a parent key.
          # It's like implementing a stack automaton with the grammar and the stack.

    def validate_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            for index, line in enumerate(lines):
              print(self.stack, self.current_indent)
              if not self.validate_line(line):
                print(f"Validation failed at line {index + 1}")
                return False
            return True
        except Exception as e:
            print(f"Error reading file: {e}")
            return False

    def validate_line(self, line):
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith("#"):
            return True

        # Determine indentation level
        indent_level = len(line) - len(stripped)
        if indent_level > self.current_indent:
            # Indent increased: entering a nested structure
            self.stack.append(self.current_indent)
            self.current_indent = indent_level
        elif indent_level < self.current_indent:
            # Indent decreased: exiting nested structures
            while self.stack and self.stack[-1] >= indent_level:
                self.current_indent = self.stack.pop()
            if self.current_indent != indent_level:
                return False

        # Parse node
        if ":" in stripped:
            return self.validate_mapping_entry(stripped)
        elif stripped.startswith("-"):
            return self.validate_sequence_entry(stripped)
        else:
            return self.validate_scalar(stripped)

    def validate_mapping_entry(self, line):
        key, _, value = line.partition(":")
        if not self.validate_key(key.strip()):
            return False
        if value and not self.validate_node(value.strip()):
            return False
        return True

    def validate_sequence_entry(self, line):
        if not line.startswith("- "):
            return False
        return self.validate_node(line[2:].strip())

    def validate_key(self, key):
        return self.validate_plain_scalar(key) or self.validate_quoted_scalar(key)

    def validate_node(self, node):
        return (
            self.validate_scalar(node) or
            self.validate_collection(node) or
            self.validate_comment(node)
        )

    def validate_scalar(self, scalar):
        return (
            self.validate_plain_scalar(scalar) or
            self.validate_quoted_scalar(scalar) or
            self.validate_block_scalar(scalar)
        )

    def validate_plain_scalar(self, scalar):
        # Simplified plain scalar validation
        return scalar.isprintable()

    def validate_quoted_scalar(self, scalar):
        if scalar.startswith('"') and scalar.endswith('"'):
            return self.validate_escaped_string(scalar[1:-1])
        if scalar.startswith("'") and scalar.endswith("'"):
            return self.validate_unescaped_string(scalar[1:-1])
        return False

    def validate_escaped_string(self, string):
        i = 0
        while i < len(string):
            if string[i] == "\\":
                i += 1
                if i >= len(string) or string[i] not in ['n', 't', '\\', '"']:
                    return False
            i += 1
        return True

    def validate_unescaped_string(self, string):
        return string.isprintable()

    def validate_block_scalar(self, scalar):
        return scalar.startswith("|")

    def validate_collection(self, collection):
        # Collections are more complex; here we keep it minimal
        return collection.startswith("-") or ":" in collection

    def validate_comment(self, line):
        return line.startswith("#")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python yaml_validator.py <file_path>")
        sys.exit(1)

    validator = YAMLValidator()
    if validator.validate_file(sys.argv[1]):
        print("Valid YAML")
    else:
        print("Invalid YAML")
