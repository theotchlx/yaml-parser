# yaml-parser

## Usage

## Glossary

## What?

## Why?

## How?

## Technology stack

## Process

I started by defining what I needed to define:
- The YAML language, to define the set of words.
- The set of valid YAML words.
- ((The YAML regexp, to describe a set of words (?).)) The automata defines the regexp(?) anyways.
- The YAML grammar, to generate words in the language.
- The YAML automata from the grammar, to check if a word is valid in the language. The automata is an BNF? EBNF? or is that the grammar. À pile car doit prendre en compte l'indentation...
- The YAML parser, to check if a YAML file is valid.

## References
- [YAML's official website](https://yaml.org/)
- [Crafting Interpreters](https://craftinginterpreters.com/)
- [ASCII Flow](http://asciiflow.com/)

define grammar
then  draw one automata per word
then draw the automata for the whole language, with a stack for keeping track of the indentation
then write the parser: shell script that returns true/false with a huge regexp?
Maybe make a regexp that works on one line and parse each line? (for easier indentation handling).

