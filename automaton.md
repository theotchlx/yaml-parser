# Automaton representation

I did not draw the stack with the automaton. I tried my best to draw the automaton from the non-terminals in the grammar, with transitions to move between them (and loops for elements that go back to earlier non-terminals, or use `{ element }` in the grammar), so that it could validate words generated from the grammar.

I used the [DOT](https://graphviz.org/doc/info/lang.html) graph visualization language.  
The automaton is also exported as an SVG and a PNG.

## In DOT language

```dot
digraph YAML_automaton {
    rankdir=LR;  // "Left to Right" automaton graph layout.
    node [shape=circle];

    // Start arrow.
    _start [style=invis];
    _start -> _node
    
    // Start node.
    _node [label="node"];
    final [shape=doublecircle, label="Valid"]; // Final state

    // Scalar states.
    scalar_start [label="scalar"];
    plain_scalar [label="plain scalar"];
    quoted_scalar [label="quoted scalar"];
    block_scalar [label="block scalar"];
    folded_scalar [label="block\nfolded scalar"];
    literal_scalar [label="block\nliteral scalar"];
    line_block [label="line block"];
    block_line [label="block line"];

    // States for collections
    block_mapping [label="block\nmapping"];
    block_sequence [label="block\nsequence"];

    // Comment state
    comment_start [label="comment"];

    // Node transitions
    _node -> scalar_start [label="scalar value"];
    _node -> block_sequence [label="- "];
    _node -> comment_start [label="#"];

    // Scalar transitions
    scalar_start -> plain_scalar [label="string"];
    scalar_start -> quoted_scalar [label="'string' or \"string\""];  # Together for a simpler automaton
    scalar_start -> block_scalar [label="> or |"];  # Same

    block_scalar -> folded_scalar [label=">"];
    block_scalar -> literal_scalar [label="|"];
    line_block -> block_line [label="ε"];
    block_line -> line_block [label="\\n"];
    folded_scalar -> line_block [label="\\n"];
    literal_scalar -> line_block [label="\\n"];
    
    // Repeart entries or scalars
    plain_scalar -> block_mapping [label=":"];
    quoted_scalar -> block_mapping [label=":"];

    // Collection transitions (to block mappins or sequences)
    # A mapping entry or sequence entry can be a scalar ... Or a sub-node! So the automaton loops back on itself.
    block_mapping -> scalar_start [label="key: value"];
    block_mapping -> _node [label="key: node"];
    block_sequence -> scalar_start [label="- scalar"];
    block_sequence -> _node [label="- node"];

    // Comment transitions: start with #.
    comment_start -> comment_start [label="string"];  // This is the "comment body". A string is equivalent to a repetition of strings.

    // Valid end states for End Of File signal (EOF).
    plain_scalar -> final [label="EOF"];
    quoted_scalar -> final [label="EOF"];
    block_line -> final [label="EOF"];
    comment_start -> final [label="EOF"];
}
```

## In PNG format

![Automaton](automaton.png)

## In SVG format

![Automaton](automaton.svg)
