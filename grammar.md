# YAML grammar

## Design

The official YAML website provides a extremely complete and explicit description of each YAML element. It was very time consuming to read, and made me realize that YAML is much, much more complex and complete than the extent of its use in my daily life.

Using other online resources in multiple Wikis and blogs, I started by writing the possible words and word combinations of YAML.  
It quickly became apparent that indentation (and keeping track of indentation consistency) was gonna be a big issue for writing the script.  
Looking at the different ways to write my grammar, I tried writing it in BNF (Backus-Naur Form), before realizing it was easier to write the YAML grammar in Extended BNF (EBNF), I found it clearer and more readable.

At first, I included more complex YAML objects in my grammar, ones that I rarely encounter, such as:  
YAML "variables" (anchors, aliases and references),  
I believe the only elements (among the ones I could find at least) my grammar doesn't include are YAML "variables": anchors, aliases and references.
This is because I find my grammar already complex to understand, but also because I have never seen or used these elements in practice, and validating the relationships they have in different parts of the documents is too much of a challenge for me to write a script for, at least for now.

I believe I can find the techniques to validate such elements at [Crafting Interpreters](https://craftinginterpreters.com/), which looks very interesting to learn about, and I hope I find the time for it.

Now that the grammar is done, the next challenge is validating syntax and indentation with a direct implementation of the grammar (and not just a bunch of loops or regexps).

Below is my best try at a YAML grammar, written in EBNF.

## EBNF YAML grammar

```md
yaml                 = { document };                                       # A YAML file can be zero documents.
document             = [ document_header ] node [ document_terminator ];   # In YAML there is only one root node, but it can be anything valid seen below.
document_header      = "---" newline;
document_terminator  = "..." newline;                                      # Document start/end markers (entirely optionnal).

node                 = scalar | collection | comment;                      # Scalar: single value, collection: simple or multi-line mapping, sequence/list, or a comment.
scalar               = plain_scalar | quoted_scalar | block_scalar;        # A scalars is a single value: plain/simple (unquoted), quoted (single ' or double "), or block-style (with > or |).
plain_scalar         = string;                                             # Unquoted string.
quoted_scalar        = '"' string '"' | "'" string "'";                    # Double-quoted is to allow escape characters (\t, \\...), single-quoted do not.
block_scalar         = block_folded_scalar | block_literal_scalar;         # Folded is >, literal is |. They are followed by indented content.
block_folded_scalar  = ">" [ newline ] line_block;                         # "Folded": newlines are folded into spaces.
block_literal_scalar = "|" [ newline ] line_block;                         # "Literal": newlines are preserved.

collection           = block_mapping | block_sequence;                     # Collections are maps or sequences. They represent arrays/lists of more or less complex values.
block_mapping        = { mapping_entry };                                  # Collection of key-value pairs.
block_sequence       = { sequence_entry };                                 # Collection of list/sequence items.

mapping_entry        = key ":" ( " " scalar | newline indentation node );  # A mapping entry is a key followed by a colon, followed by a value, which can be simple or complex.
key                  = plain_scalar | quoted_scalar;                       # Keys in mappings can be plain or quoted scalars. Not empty.
sequence_entry       = "-" ( " " scalar | newline indentation node );      # A sequence entry starts with a dash (`-`), followed by a simple or complex value.

comment              = "#" string newline;                                 # Comments are ignored... Even when they start in the middle of a line.
string               = { character };
character            = any UTF-8 character excluding newline;
line_block           = { block_line };
block_line           = indentation string newline;
indentation          = { " " };                                            # An indent is zero or more spaces.
newline              = "\n" | "\r\n";                                      # Historically, old Macintosh OSes used a single \r (carriage return) as newline, but the more Unix-compliant OS X has switched to \n for over 20 years now.
```
