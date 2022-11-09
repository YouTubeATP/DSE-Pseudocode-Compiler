# DSE-Pseudocode-Compiler
A function that converts DSE-style Pseudocode into Python.

## Supported styles
All styles and capitalization found throughout various years of past papers.

## Feature list
- Variable assignment
- Comparison operators
- Logical operators
- `if`/ `else`/ `else if` statements (with or without `then`)
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
The compromise is `X[0]` will always return `None`.

## Unsupported features
Type conversion of inputs **will not be supported**. You have to manually convert it:
```
Input A, B
Output A * B
```
to
```
Input A, B
Output int(A) * int(B)
```

Plain language used in pseudocode **will not be supported**. Convert them to Python manually:
```
X <-- 2
Y <-- 4
Output the square root of X
Output the integral part of X / Y
```
to
```
from math import sqrt
X <-- 2
Y <-- 4
Output sqrt(X)
Output X // Y
```
