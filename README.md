# DSE-Pseudocode-Compiler
A function that converts DSE-style Pseudocode into Python.

## Supported styles
All styles and capitalization found throughout various years of past papers.

## Feature list
- Variable assignment
- Comparison operators
- Logical operators
- `if`/ `else`/ `else if` statements
- `for` loops
- `while` loops
- `repeat... until` loops
- `Input`
- `Output`
- Pseudo-accurate arrays

## Arrays
To not break `for` loops that aim to iterate over lists, the trait of **array indices starting from 1** is retained.
The compiler searches for the highest index for each array referenced, and initializes the list:
```
X = [None] * (highest_index + 1)
```
