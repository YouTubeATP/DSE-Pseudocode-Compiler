# Convert *.pc.txt to *.py

from compiler import compile
import os

for file in os.listdir(os.path.abspath("./examples")):
    if file.endswith(".pc.txt"):
        with open(os.path.abspath(f"./examples/{file}"), "r") as f:
            compiled_code = compile(f.read())
        with open(os.path.abspath(f"./examples/{file[:-7]}.py"), "w") as f:
            f.write(compiled_code)