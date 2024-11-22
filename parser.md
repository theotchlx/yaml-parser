# Validation scripts

There are two validation scripts, made in Python.
Their implementation and the thought process behind it is explained down below.

## Design

I made a series of Python scripts, then redesigned them in one dynamic script (through smaller functions).
This first version of the algorithm was written to work like a stack automaton, going through each line of text with a stack to keep track of indentation, as well as other flags to keep track of the current YAML context (list, parent key, etc.).
nonono.
i made small functions to test each of the grammar words
then like parser automaton with stack for more complex grammar non-terminals such as block_sequence (check list items/map values/sequence entries indentation consistency, etc.)

I tried making more than a dozen scripts before I found the correct way to implement my grammar, and understood that to make a better validation script, I should just implement my grammar.

Before that, I had tried scripts that validated lines with huge regular expressions, but that means I'm using a pre-implemented automaton that validates the regexps for me.
I of course also tried making dumb algorithms that looped over the text and validated or invalidated stuff based on rules I added on top of the previous rules etc etc... That was not a good solution either.
So I concentrated my efforts on refining my grammar, and realized I could just implement a function to validate each element, for the code to be as close as possible to the mathematical definitions.

I realize this is a much better designed approach, and I did took me a while to get to it, and multiple tries to do it correctly.

Still now, the implementation is not correct. The script parses each line individually, one after the other. It cannot go back lines, it only goes forward one line.
This would work to validate languages such as JSON, that can be written on one line; but in YAML you have block structures such as:

```yaml
>
 this
 is
 text
```

or

```yaml
|
 some
 other
 text
```

As you can see, the last lines can be properly validated (by the grammar) under the condition that they belong to a block scalar: their "parent element" is "|" or ">".
The issue is, my script sees this "parent element" as a "parent line", and once it is validated, there is no way to keep track of it: either the code, or the stack, would become overcomplicated messes.
After some researches, I now realize I should have restructured the YAML file into a tree of elements, as to preserve their hierarchical relationship. I did not have enough time to design or make this, but I know this is part of some "lexing" or "parsing" or "tokenization": compilers and other tools see the analysed text as a tree, and I now have a little idea of why, and why some things can't (in a simple way) be parsed line-wise.
I am getting way ahead of myself here, but maybe even identation could have been represented hierarchically in the tree. However this may be an incorrect solution, since the stack can handle it already.

So I would have needed to design the tree data structure to use, make a function to transform the YAML file into the tree, with every hierarchical information between elements accessible, and then use my current functions that implement the grammar to validate each element of the tree.

This would have been the only correct complete solution. It would have still been possible to validate YAML using line-wise parsing using a very "stateful" approach : with lots of simpler data structures such as booleans, stacks or queues to "remember" the hierarchical state or "context" of the current line: are we in the context of a sequence? Of a mapping? ...
But manipulating this many data structure would make the code terribly complex, inefficient and unreadable.

## Ideas for further implementations

I wonder if it is possible to implement a validation script using one regular expression.
I'm not sure this is possible for YAML,
The feasability of this solution would depend on the relationships between regexps and a stack automaton, and how they can be translated to each other. How would the regular expressions validate that indentation is consistent?
