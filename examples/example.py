# Convert *.pc.txt to *.py

from compiler import compile
import os

for file in os.listdir(os.path.relpath("./examples")):
    if file.endswith(".pc.txt"):
        with open(os.path.relpath(f"./examples/{file}"), "r") as f:
            compiled_code = compile(f.read())
        with open(os.path.relpath(f"./examples/{file[:-7]}.py"), "w") as f:
            f.write(compiled_code)