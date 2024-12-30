########################################################################
# A Work in progress, created by g0730n on December 30th, 2024. Feel
# free to fork, and modify at your own leasure.
#
# This interpreter is kind of a joke, as I am writing it in Python.
# It's like a dream within a nightmare. But aside from the bloated
# slowness of python, the basically typeless data format Python uses 
# on the user's end makes it
# very easy to write this interpreter. All variables and group (FUNCTION)
# data is stored in arrays.
# The entire program data will either be a plain text file, or a single string.
#
# Or if executing the code from a commandline, it will build off of there
# like any REPL like environment.
# I have no idea what I am doing here but am having a ton of fun and
# learning some new things.
# I apologize for the poorly named variables and basically non-existant
# commenting. I am not very good at doing such things, I should probably
# work at it more.
#######################################################################

program = f"""0K 2024 8K 30 O $Its December$, 8K,$th$, 0K I 1K O 1K"""
program_tokens = []
k = []
g = []

def incr(pos):
    if pos + 1 < len(program): pos += 1
    return pos
    

def read_numbers_from_prog(pos):
    temp=""
    while pos < len(program)-1 and program[pos].isdigit():
        temp += program[pos]
        pos = incr(pos)
    if pos == len(program)-1 and program[pos].isdigit(): temp += program[pos]
    return pos, temp

def get_number(pos):
    temp1 = ""
    temp2 = ""
    pos, temp1 = read_numbers_from_prog(pos)

    if(program[pos]=='.'):
        temp1 += program[pos]
        pos = incr(pos)
        pos, temp2 = read_numbers_from_prog(pos)
        temp1 += temp2
        return pos, float(temp1)
    else: return pos, int(temp1)

def is_keyword(pos):
    if program[pos].isdigit():
        pos, num = get_number(pos)
        if num.is_integer() and program[pos] == 'K': return 1
    return 0

def get_keyword_value(pos):
    pos, keyword = get_number(pos)
    pos = incr(pos)
    if keyword > len(k)-1: return pos, 0
    else: return pos, k[keyword]

def save_keyword_value(pos, value):
    pos, keyword = get_number(pos)
    error = 0
    if keyword > 99: error = 2
    else:
        if len(k) < keyword+1:
            indices_to_add = keyword-len(k)
            x = 0;
            while x < indices_to_add:
                k.append('')
                x += 1
            k.append(value)
        else: k[keyword] = value
        pos = incr(pos)
    
    return error, pos

def skip_whitespace(pos):
    while(pos < len(program)-1 and program[pos] in (' ','\n','\t')):
        pos = incr(pos)
    return pos

def send_out(pos):
    eating = True
    result = ""
    pos = incr(pos)
    pos = skip_whitespace(pos)
    while eating:
        pos = skip_whitespace(pos)
        if is_keyword(pos):
            pos, value = get_keyword_value(pos)
            result += str(value)
        elif program[pos].isdigit():
            pos, value = get_number(pos)
            result += str(value)
        elif program[pos] == '$':
            pos = incr(pos)
            while program[pos] != '$':
                result += program[pos]
                pos = incr(pos)
            pos = incr(pos)
        pos = skip_whitespace(pos)
        if pos == len(program) or program[pos] != ',':
            eating = False
        else:
            pos = incr(pos)
            if program[pos] == ' ': result += program[pos]
            pos = skip_whitespace(pos)

    #OUTPUT MEDIUM OF CHOICE
    print(f'> {result}')
    return pos

def error_message(error, pos):
    #ERROR HANDING FUNCTION
    snippet = ""
    msg = ""
    if not error: msg = "EOP"
    else:
        if error == 1: msg = "must be followed by keyword"
        if error == 2: msg = "max keyword index is 99"

        snippet += "\""
        for x in range(pos-12, pos+12):
            if x < len(program):
                if x == pos: snippet += f'<{msg}>'
                snippet += program[x]
            else:break
        snippet += "\""
    return snippet

def interpret():
    #MAIN FUNCTION
    pos = 0
    current_keyword = 0
    temp = ""
    error = 0
    while(not error and pos < len(program)-1):
        if(program[pos].isdigit()):
            if is_keyword(pos):
                #PARSE KEYWORD ASSIGNMENTS
                temp_pos, current_keyword = get_number(pos)
                temp_pos = incr(temp_pos)
                temp_pos = skip_whitespace(temp_pos)
                temp_pos, value = get_number(temp_pos)
                error, pos = save_keyword_value(pos, value)
                pos = temp_pos
        elif(program[pos].isalpha()):
            if program[pos] == 'O':
                #OUTPUT BUILTIN
                pos = send_out(pos)
            if program[pos] == 'G':
                #GROUPS BUILTIN
                pass
            if program[pos] == 'I':
                #INPUPT BUILTIN
                pos = incr(pos)
                pos = skip_whitespace(pos)
                if not is_keyword(pos):
                    error = 1
                else:
                    temp = input()
                    error, pos = save_keyword_value(pos, temp)
                    
            if program[pos] == 'L':
                #LOOP BUILTIN
                pass
        else:
            pos = incr(pos)
            pass

    if not error: temp = ""
    else: temp = f'ERROR at {pos}:'

    print(f'{temp}{error_message(error, pos)}')

interpret()
