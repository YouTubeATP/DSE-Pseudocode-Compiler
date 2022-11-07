import re

def compile(pseudocode: str) -> str:
    
    def init_vars() -> None:
        global if_indentation_level
        global deindent_next_line
        deindent_next_line = False
        global inside_if_indentation_level
        inside_if_indentation_level = 0
        global deindent_runs
        deindent_runs = 0
        global repeat_statement_no
        repeat_statement_no = 1
        global repeat_record_no
        repeat_record_no = 1
        global repeat_ends
        repeat_ends = {}
    
    def replace_tokens(pseudocode: str):
        """Replace simple tokens, like If, Else."""
        pseudocode = pseudocode.replace("And", "and").replace("AND", "and") # Fix "and" capitalization
        pseudocode = pseudocode.replace("Or", "or").replace("OR", "or") # Fix "or" capitalization
        pseudocode = pseudocode.replace("Not", "not").replace("NOT", "not") # Fix "not" capitalization
        pseudocode = pseudocode.replace("TRUE", "True").replace("true", "True") # Fix "True" capitalization
        pseudocode = pseudocode.replace("FALSE", "False").replace("false", "False") # Fix "True" capitalization
        pseudocode = pseudocode.replace(" = ", " == ") # Replace the comparision operator: =
        pseudocode = pseudocode.replace("<>", "!=") # Replace the comparision operator: <>
        pseudocode = pseudocode.replace("<--", "=") # Replace the assignment operator: <--
        
        return pseudocode
    
    def convert_if_statements(line: str):
        """Converts if/ else statements."""
        global if_indentation_level
        global inside_if_indentation_level
        global deindent_next_line
        global deindent_runs
        
        if deindent_next_line:
            if deindent_runs == 0: # First deindent run, can't check with previous line
                inside_if_indentation_level = len(line) - len(line.lstrip())
                line = " " * if_indentation_level + line.lstrip()
                deindent_runs += 1
            elif inside_if_indentation_level == len(line) - len(line.lstrip()): # Check with previous line, are we still at the same code block
                inside_if_indentation_level = len(line) - len(line.lstrip())
                line = " " * if_indentation_level + line.lstrip()
                deindent_runs += 1
            else:
                deindent_next_line = False
                deindent_runs = 0
        
        if line.lstrip().startswith(("if", "If", "IF")):
            line = line.replace("If", "if").replace("IF", "if") # Fix "if" capitalization
            
            if_indentation_level = len(line) - len(line.lstrip())
            
            if line.endswith(("then", "Then", "THEN")):   
                # "if X < 2 then" --> "if X < 2:"
                line = line.replace(" Then", ":").replace(" then", ":").replace(" THEN", ":")
            else:
                # "if X < 2" --> "if X < 2:"
                line += ":"
                
        elif line.lstrip().startswith(("else", "Else", "ELSE")):
            line = line.replace("Else", "else").replace("ELSE", "else") # Fix "else" capitalization
            
            # If the code is like:
            # "If X < 2
            #     X <-- 2
            #     Else X <-- 1"
            if (len(line) - len(line.lstrip())) > if_indentation_level:
                tokens = line.lstrip().split()
                
                # Else If
                try:
                    if tokens[1] in ["If", "if", "IF"]:
                        code = tokens[2:] # Code following "Else If"; e.g. "x = 2" in "Else If x = 2"
                        code = " ".join(code)
                        res = " " * if_indentation_level + "elif" + " " + code + ":"
                        
                        if_indentation_level = len(line) - len(line.lstrip())
                        deindent_next_line = True
                
                    else:    
                        res = " " * if_indentation_level + "else:"
                        code = tokens[1:] # Code following "Else"; e.g. "x = 2" in "Else x = 2"
                        code = " ".join(code)
                        res += "\n" + " " * (if_indentation_level + 4) + code
                        
                    line = res
                except IndexError:
                    pass
        
        elif any(substr in line for substr in ["then", "Then", "THEN"]):
            # "then Y = 1" --> "Y = 1"
            line = line.replace("Then ", "").replace("then ", "").replace("THEN ", "")
            
        return line
    
    def convert_simple_loops(line: str):
        """Converts for loops and while loops."""
        new_line = ""
        indentation_level = len(line) - len(line.lstrip())
        
        # Old format: "For i from 1 to 5 do"
        if line.lstrip().startswith(("for", "For", "FOR")) and line.endswith(("do", "Do", "DO")):
            line = line.split()[:-1] # "For i from 1 to 5 do" --> ["For", "i", "from", "1", "to", "5"]
            line = " ".join(line)
            
        # New format: "for i from 1 to 5"    
        if line.lstrip().startswith(("for", "For", "FOR")):
            loop_var = line.split()[1]
            loop_start = line.split()[3]
            loop_end = line.split()[5]
            line = " " * indentation_level + f"for {loop_var} in range({loop_start}, {int(loop_end) + 1}):"
        
        # Old format: "While X < 1 do"
        if line.lstrip().startswith(("while", "While", "WHILE")) and line.endswith(("do", "Do", "DO")):
            line = line.split()[:-1] # "For i from 1 to 5 do" --> ["For", "i", "from", "1", "to", "5"]
            line = " ".join(line)
            
        # New format: "while X < 1"    
        if line.lstrip().startswith(("while", "While", "WHILE")):
            condition = line.split()[1:] # "while X < 1" --> ["X", "<", "1"]
            condition = " ".join(condition) # ["X", "<", "1"] --> "X < 1"
            line = " " * indentation_level + f"while {condition}:"
        
        return line
    
    def replace_input_output(line) -> str:
        indentation_level = len(line) - len(line.lstrip())
        
        if line.lstrip().startswith(("input", "Input", "INPUT")):
            tokens = line.split()[1:] # ["input", "A,", "B"] --> ["A,", "B"]
            res = ""
            for token in tokens:
                if token.endswith(","):
                    token = token[:-1] # "A," --> "A"
                res += " " * indentation_level + token + " = input()" + "\n"
            return res
        
        elif line.lstrip().startswith(("output", "Output", "OUTPUT")):
            res = ""
            code = " ".join(line.split()[1:]) # "Output X, Y" --> "X, Y"
            res = " " * indentation_level + f"print({code})"
            return res
        
        return line
    
    def replace_repeat_until(line) -> str:
        if line.lstrip().startswith(("Until", "until", "UNTIL")):
            return ""
        
        if line.lstrip().startswith(("Repeat", "repeat", "REPEAT")):
            global repeat_statement_no
            line = line.replace("Repeat", "while not {placeholder" + str(repeat_statement_no) + "}:")
            line = line.replace("REPEAT", "while not {placeholder" + str(repeat_statement_no) + "}:")
            line = line.replace("repeat", "while not {placeholder" + str(repeat_statement_no) + "}:")
            
            repeat_statement_no += 1
        
        return line
                    
    def record_repeat_until(line) -> None:
        global repeat_record_no
        global repeat_ends
        if line.lstrip().startswith(("Until", "until", "UNTIL")):
            repeat_ends[str(repeat_record_no)] = " ".join(line.split()[1:]) # "Until X < 3" --> "X < 3", put in repeat_ends
            repeat_record_no += 1
            
    def replace_repeat_until_placeholder(pseudocode) -> str:
        global repeat_ends
        for key, value in zip(repeat_ends.keys(), repeat_ends.values()):
            pseudocode = pseudocode.replace("{placeholder" + str(key) + "}", f"({value})")
        return pseudocode
            
    def process_array_indices(line) -> str:
        x = re.findall("[a-zA-Z0-9_]+\[[0-9]+\]", line)
        if x:
            for expression in x:
                # group() - Part of the string that matched the regex
                var_name = re.search("[a-zA-Z0-9_]+", expression).group()
                var_index = int(re.search("\[[0-9]+\]", expression).group()[1:-1]) # Strip the square brackets: [3] --> 3
                
                # Record highest array index
                global highest_array_indices
                try:
                    if highest_array_indices[var_name] < var_index:
                        highest_array_indices[var_name] = var_index
                except KeyError: # Create a new spot for a new variable seen
                    highest_array_indices[var_name] = var_index
        return line
                
    def initialize_arrays() -> str:
        global highest_array_indices
        init_lines = ""
        for key, value in zip(highest_array_indices.keys(), highest_array_indices.values()):
            try:
                int(value)
            except ValueError: # The index is a variable, not an integer, i.e. x[i]
                value = 99999
            init_lines += f"{key} = [None] * {value + 1}" + "\n"
        return init_lines
    
    def process_line(line: str):
        record_repeat_until(line)
        new_line = convert_if_statements(line)
        new_line = convert_simple_loops(new_line)
        new_line = replace_repeat_until(new_line)
        new_line = replace_input_output(new_line)
        new_line = process_array_indices(new_line)
        
        return new_line + "\n" if new_line != "" else new_line
    
    init_vars()
    
    pseudocode = replace_tokens(pseudocode)
    
    new_pseudocode = ""
    
    global highest_array_indices
    highest_array_indices = {}
    
    for line in pseudocode.splitlines():
        new_pseudocode += process_line(line)
    
    new_pseudocode = replace_repeat_until_placeholder(new_pseudocode)
    new_pseudocode = initialize_arrays() + new_pseudocode
    
    return new_pseudocode