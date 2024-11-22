# yaml-parser

This is repository contains a grammar, automaton and parser for the YAML language.

## Technology stack

The parser scripts are made in Python.
Poetry is used as the dependency manager.

## Usage

On Linux, execute the following commands:

```py
git clone https://github.com/theotchlx/yaml-parser.git
cd yaml-parser
python validation_script.py <your_file_path>
```

Don't forget to replace `<your_file_path>` with a valid file path such as `test-file.yaml`.  
This program can also be used as a library. It contains a `YAMLValidator` class that has methods that return `True` or `False` to check for validity of grammar elements and YAML files.

## What?

In this project, I explain the process I followed to define a grammar for the YAML language, as well as an automaton, and a Python script to validate YAML files.

## Why?

The objective of this project is to learn about automata, how to define them qx well as design a practical implementation.

## How?

## Process

I started by defining what was needed to make the YAML parser:

- The YAML language. (I removed the file since it was not interesting compared to the grammar)
- The YAML grammar, to define the set of valid words in the language. I made the grammar in Backus-Naur form (BNF), and later rewrote it in Extended Backus-Naur form.
- The YAML automaton from the grammar, to check if a word is valid in the language and with a stack to take indentation in account. I tried using [ASCIIFlow](https://asciiflow.com/) and [Mermaid](https://mermaid.js.org/) to draw the automaton, but I finally decided on using the [DOT](https://graphviz.org/doc/info/lang.html) graph visualization software. I also could've used Figma/Figjam, Excalidraw, or tools especially made to draw automata.
- I tried writing regular expressions from the grammars, to check if a set of words is valid YAML and help design the parser programs, but I ended up not using them.
- The YAML parser/validation script, to check if a file is a valid YAML file or not.

## References

- [YAML's official website](https://yaml.org/) for helping me define a simpler subset of the YAML language and words to work on.
- [Crafting Interpreters](https://craftinginterpreters.com/): not as related, but it's an interesting resource.
- [ASCII Flow](https://asciiflow.com/) as well as [Mermaid](https://mermaid.js.org/) to draw the automaton in a portable manner.
- [YAMLLint](https://www.yamllint.com/) to help me test my scripts and visualize easily what conforms to YAML standards.

define grammar
then  draw one automaton per word
then draw the automaton for the whole language, with a stack for keeping track of the indentation
then write the parser: shell script that returns true/false with a huge regexp?
Maybe make a regexp that works on one line and parse each line? (for easier indentation handling).

## Licence

This project is made open source under the MIT licence.
