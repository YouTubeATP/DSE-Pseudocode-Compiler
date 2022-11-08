# This file makes compiler.exe

# Convert *.pc.txt to *.py

from compiler import compile
import os

for file in os.listdir(os.path.abspath("./")):
    if file.endswith(".pc.txt"):
        with open(os.path.abspath(f"./{file}"), "r") as f:
            compiled_code = compile(f.read())
            print(f"Processed {file}")
        with open(os.path.abspath(f"./{file[:-7]}.py"), "w") as f:
            f.write(compiled_code)
            print(f"Written to {file[:-7]}.py")
    
input()
exit()