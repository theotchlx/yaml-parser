# g

```md
yaml                = { document };                                      # A YAML file can be zero documents.
document            = [ document_header ] node [ document_terminator ];  # In YAML there is only one root node, but it can be anything valid seen below.
document_header     = "---" newline;
document_terminator = "..." newline;                                     # Document start/end markers (entirely optionnal).

node                = scalar | collection | comment;                     # Scalar: single value, collection: simple or multi-line mapping, sequence/list, or a comment.
scalar              = plain_scalar | quoted_scalar | block_scalar;       # A scalars is a single value: plain/simple (unquoted), quoted (single ' or double "), or block-style (with > or |).
plain_scalar        = string;                                            # Unquoted string.
quoted_scalar       = '"' escaped_string '"' | "'" unescaped_string "'"; # Double-quoted is to allow sequences, single-quoted do not.
block_scalar        = block_folded_scalar | block_literal_scalar;        # Folded is >, literal is |. They are followed by indented content.
block_folded_scalar = ">" [ newline ] indented_block;                    # "Folded": newlines are folded into spaces.
block_literal_scalar = "|" [ newline ] indented_block;                   # "Literal": newlines are preserved.

collection          = block_mapping | block_sequence; 
# Collections group multiple nodes together.
# They can be mappings (key-value pairs) or sequences (lists).
block_mapping       = { mapping_entry };
# A block mapping is a collection of key-value pairs.
block_sequence      = { sequence_entry };
# A block sequence is a collection of list items.

mapping_entry       = key ":" [ " " node ] newline;
# A mapping entry is a key followed by a colon (`:`), optionally a value (a "sub-root node"), and a newline.
key                 = plain_scalar | quoted_scalar;
# Keys in mappings can be plain or quoted scalars.
sequence_entry      = "-" [ " " node ] newline;
# A sequence entry starts with a dash (`-`), optionally followed by a value and a newline.

comment             = "#" string newline;                                # Comments are ignored... Even when they startin the middle of a line.
string              = { character };
escaped_string      = { character | escape_sequence };                   # An escaped string doesn't 
# An escaped string allows special sequences (e.g., `\n` for newlines).
unescaped_string    = { character };
# An unescaped string is a simpler form of string with no escape sequences.
escape_sequence     = "\" ( "n" | "t" | "\\" | "\"" );
# Escape sequences in double-quoted strings include:
# - `\n` (newline), `\t` (tab), `\\` (backslash), and `\"` (double quote).
character           = any UTF-8 character - newline;
# A character is any valid UTF-8 character except a newline.
newline             = "\n" | "\r\n";
# A newline can be Unix-style (`\n`) or Windows-style (`\r\n`).
indented_block      = { indentation_line };
# An indented block contains multiple lines, each starting with indentation.
indentation_line    = indentation string newline;
# An indentation line begins with spaces (indentation), followed by a string, and ends with a newline.
indentation         = { " " };
# Indentation is represented as one or more spaces.
```
