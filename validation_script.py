class YAMLValidator:
    def __init__(self):
        self.stack = []  # Stack to keeps track of nested indentation levels.

    def validate_file(self, file_path):
        try:
            with open(file_path, 'r') as file:  # Open the file and get the lines.
                lines = file.readlines()  # Each line ends with a newline character.

            for index, line in enumerate(lines):  # Validate each line.
                if not self.validate_line(line):
                    print(f"Validation failed at line {index + 1}")
                    return False
            return True  # If all lines are valid, return True (file is valid YAML).
        except Exception as e:
            print(f"Error reading file: {e}")
            return False

    def validate_line(self, line):
        # Empty lines, comments and document separators are skipped (they are valid).
        stripped = self.yaml_strip(line)
        if stripped.lstrip() == "":
            return True  # Empty lines are valid.

        # Determine current line's indentation level (0 if the line is just spaces/indent).
        indent_level = len(line.rstrip()) - len(line.strip())

        # Check if indentation level is valid (must not decrease inappropriately).
        while self.stack and self.stack[-1] > indent_level:
            self.stack.pop()  # Close levels as needed.

        # Push the indentation to the stack if the indentation increases instead.
        if not self.stack or self.stack[-1] < indent_level:
            self.stack.append(indent_level)

        # Validate the line using the grammar rules functions

        # If line starts a dash (sequence entry) or is key-colon-value (mapping entry), validate:
        if stripped.startswith("-"):
            if not self.is_sequence_entry(stripped):
                return False
        elif ":" in stripped:
            if not self.is_mapping_entry(stripped):
                return False
        else:
            # Line is a standalone scalar.
            if not self.is_scalar(stripped):
                return False

        return True  # If all checks pass, the line is valid.

    # Helper function to ignore/validate/strip document separators and comments.
    def yaml_strip(self, text):
        # Validates:
        # comment             = "#" string newline;
        # document_header     = "---" newline;
        # document_terminator = "..." newline;
        stripped = text.split("#")[0].strip()  # Remove (ignore) comments.
        stripped = stripped.rstrip()  # Remove trailing whitespace characters (spaces, newlines...).
        if stripped.lstrip() == "---" or stripped.lstrip() == "...":
            return ""  # Remove (ignore) document separators.
        return stripped  # Stripped text with indentation.


#-------------------------------------------->
# Below are all the functions that validate "simple" scalar structures (plain, quoted, block...).
# They try to closely implement the grammar rules.
#-------------------------------------------->


    def is_string(self, string):
        # Validates:
        # string = { character };
        return string.isprintable()

    def is_indentation(self, string):
        # Validates:
        # indentation = { " " };
        for char in string:
            if char != " ":
                return False
        return True

    def is_key(self, string):
        # Validates:
        # key = plain_scalar | quoted_scalar;
        return self.is_plain_scalar(string) or self.is_quoted_scalar(string)

    def is_scalar(self, string):
        # Validates:
        # scalar = plain_scalar | quoted_scalar | block_scalar;
        return (
            self.is_plain_scalar(string)
            or self.is_quoted_scalar(string)
            or self.is_block_scalar(string)  # Works only partially due to line-wise validation. See function definition below.
        )

    def is_plain_scalar(self, scalar):
        # Validates:
        # plain_scalar = string;
        return self.is_string(scalar)

    def is_quoted_scalar(self, string):
        # Validates:
        # quoted_scalar = '"' string '"' | "'" string "'";
        if len(string) >= 2:  # At least 2 characters long (shortcut for quotes and string).
            if (string.startswith('"') and string.endswith('"')) or (
                string.startswith("'") and string.endswith("'")
            ):
                return self.is_string(string[1:-1])  # Remove quotes and validate the string inside.
        return False


#-------------------------------------------->
# Below are all the functions that validate "complex" block structures (mapping, sequence...).
# Most are (partially) implemented, but will only partially validate YAML due to the line-wise parsing.
# It is not possible to validate nested structures correctly with this data structure.
# However I believe it would be possible with a tree data structure, to have access to hierarchical information.
# There would need to be a function to parse the file into a tree; then these functions could validate each element of the tree.
#-------------------------------------------->


    def is_node(self, node):
        return self.is_scalar(node)# or self.is_collection(node)
        # I can't write the is_collection function because of the line-wise parsing.

    def is_mapping_entry(self, string):
        # Validates:
        # mapping_entry = key ":" ( " " scalar | newline indentation node );
        if ":" not in string:
            return False
        key, value = string.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not self.is_key(key):
            return False

        # Value can be a simple scalar or more complex.
        if self.is_scalar(value):
            return True

        # Due to the line-wise parsing, I can't validate complex values correctly: each line stops at a newline.
        # I should have implemented a tree structure to handle nested structures such as a children node.
        # I believe this is how real parsers work.

        return False

    def is_sequence_entry(self, string):
        # Validates:
        # sequence_entry = "-" ( " " scalar | newline indentation node )
        if not string.startswith("-"):
            return False

        rest = string[1:].strip()
        if self.is_scalar(rest):
            return True

        # Same thing. I can't validate complex values (subnodes) correctly with this data structure.

        return False

    def is_block_scalar(self, string):
        # Validates:
        # block_scalar = block_folded_scalar | block_literal_scalar;
        return self.is_block_folded_scalar(string) or self.is_block_literal_scalar(string)
        # Note that these two checks won't actually validate the block scalar content.
        # They don't work correctly because of the line-wise parsing. They would work if i had used a tree data structure. (See parser.md for explanations)

    def is_block_folded_scalar(self, string):
        # Validates:
        # block_folded_scalar = ">" [ newline ] line_block;
        if string.startswith(">"):
            rest = string[1:].strip()
            return rest == "" or self.is_line_block(rest)
        return False

    def is_block_literal_scalar(self, string):
        # Validates:
        # block_literal_scalar = "|" [ newline ] line_block;
        if string.startswith("|"):
            rest = string[1:].strip()
            return rest == "" or self.is_line_block(rest)
        return False
    
    # Can't be implemented.

    #def is_line_block(self, lines):
    # ...

    #def is_collection(self, lines):
    # ...


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python yaml_validator.py <file_path>")
        sys.exit(1)

    validator = YAMLValidator()
    if validator.validate_file(sys.argv[1]):
        print("Valid YAML")
    else:
        print("Invalid YAML")
