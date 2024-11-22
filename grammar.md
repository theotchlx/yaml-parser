# YAML grammar

## Design

The official YAML website provides a extremely complete and explicit description of each YAML element. It was very time consuming to read, and made me realize that YAML is much, much more complex and complete than the extent of its use in my daily life.

Using other online resources in multiple Wikis and blogs, I started by writing the possible words and word combinations of YAML.  
It quickly became apparent that indentation (and keeping track of indentation consistency) was gonna be a big issue, but not for now.  
Looking at the different ways to write my grammar, I tried making a BNF (Backus-Naur Form), before realizing it was easier to write the YAML grammar in Extended BNF (EBNF), I found it clearer and more readable.

At first, I included more complex YAML objects in my grammar, ones that I never use and never encounter in practice, such as:  
YAML "variables" (anchors, aliases and references),  
block scalars (| or >) with multiline strings (string with newline followed by n strings with newline),  
and some more obscure stuff.

These are very easy to define and combine in EBNF, but I got rid of these when I realized it was just making my prototype algorithms more complex, and they didn't interest me a lot since I never see them. The real challenge was validating syntax and indentation with a direct implementation of the grammar (and not just a bunch of loops or regexps).

The result is a simplified YAML grammar written in EBNF.

## Simplified EBNF YAML grammar

```md
yaml                = { document };   
document            = [ document_header ] node [ document_terminator ];
document_header     = "---" newline;
document_terminator = "..." newline;  

node                = scalar | collection | comment;
scalar              = plain_scalar | quoted_scalar | block_scalar;
plain_scalar        = string;
quoted_scalar       = '"' escaped_string '"' | "'" unescaped_string "'";

collection          = block_mapping | block_sequence;
block_mapping       = { mapping_entry };
block_sequence      = { sequence_entry };

mapping_entry       = key ":" [ node ];
key                 = plain_scalar | quoted_scalar;
sequence_entry      = "-" node;

comment             = "#" string;
string              = { character };
escaped_string      = { character | escape_sequence };
unescaped_string    = { character };
escape_sequence     = "\" ( "n" | "t" | "\\" | "\"" );
character           = any UTF-8 character
newline             = "\n" | "\r\n";
```
