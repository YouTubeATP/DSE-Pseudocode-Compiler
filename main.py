from compiler import compile
from math import sqrt

code = """input B
A <-- 2
C <-- 2
D <-- sqrt(int(B)*int(B) - 4*A*C)
output D"""

compiled = compile(code)
print(compiled)
exec(compiled)