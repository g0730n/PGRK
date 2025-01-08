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

from time import sleep

programs = ["""
1K $Hello $
2K $. How are you today?$
O$Enter your name: $
I3K
O 1K,3K,2K
            """,]
program = ""
k = []
g = []

debug_on = 0
console = 1

def debug(function, pos=0):
    if debug_on:
        match function:
            case 0:
                print(f'            pos: {pos}')
                sleep(0.1)
            case 1:
                print('  <read_numbers_from_prog>')
            case 2:
                print('  </read_numbers_from_prog>')
            case 3:
                print(' <get_number>')
            case 4:
                print(' </get_number>')
            case 5:
                print('  <get_string>')
            case 6:
                print('  </get_string>')
            case 7:
                print('  <is_keyword>')
            case 8:
                print('  </is_keyword>')
            case 9:
                print('  <get_keyword_value>')
            case 10:
                print('  </get_keyword_value>')
            case 11:
                print(' <save_keyword_value>')
            case 12:
                print(' </save_keyword_value>')
            case 13:
                print('   <skip_whitespace>')
            case 14:
                print('   </skip_whitespace>')
            case 15:
                print(' <send_out>')
            case 16:
                print(' </send_out>')
            case 17:
                print('  <is_operator>')
            case 18:
                print('  </is_operator>')
            case 19:
                print('<parse_keyword>')
            case 20:
                print('</parse_keyword>')
            case 21:
                print('<is_seperator>')
            case 22:
                print('</is_seperator>')
            case 23:
                print('<LOOP>')
            case 24:
                print('<save_group>')
            case 25:
                print('</save_group>')
            case 26:
                print('<run_group>')
            case 27:
                print('</run_group>')
            case _:
                print('\n')
        
        

def incr(pos):
    if pos + 1 < len(program): pos += 1

    debug(0,pos)

    return pos
    

def read_numbers_from_prog(pos):
    temp=""
    debug(1)
    while pos < len(program)-1 and program[pos].isdigit():
        
        temp += program[pos]
        pos = incr(pos)
    if pos == len(program)-1 and program[pos].isdigit(): temp += program[pos]
    debug(2)
    return pos, temp

def get_number(pos):
    temp1 = ""
    temp2 = ""
    debug(3)
    pos, temp1 = read_numbers_from_prog(pos)
    if(program[pos]=='.'):
        temp1 += program[pos]
        pos = incr(pos)
        pos, temp2 = read_numbers_from_prog(pos)
        temp1 += temp2
        debug(4)
        return pos, float(temp1)
    else:
        debug(4)
        return pos, int(temp1)
    
def get_string(pos):
    result = ""
    debug(5)
    if program[pos] == '$':
        pos = incr(pos)
    while program[pos] != '$':
        if program[pos] == '\n' or (program[pos] in (' ', '\t') and program[pos - 1] in (' ', '\t')):
            pass
        else:
            result += program[pos]
        pos = incr(pos)
    pos = incr(pos)
    debug(6)
    return pos, result

def is_keyword(pos):
    debug(7)
    if program[pos].isdigit():
        pos, num = get_number(pos)
        if num.is_integer() and program[pos] == 'K':
            debug(8)
            return 1
    debug(8)
    return 0

def get_keyword_value(pos):
    debug(9)
    pos, keyword = get_number(pos)
    pos = incr(pos)
    # if is_operator(pos):
        # print(program[temp_pos])
        # pos = inc(temp_pos)
    if keyword > len(k)-1:
        if debug_on:
            debug(10)
            print(f'     [EMPTY KEY: {keyword}K = 0]')
        
        return pos, 0
    else:
        if debug_on:
            debug(10)
            print(f'     [RETRIEVED KEY: {keyword}K = {k[keyword]}]')
        return pos, k[keyword]

def save_keyword_value(pos, value):
    debug(11)
    pos, keyword = get_number(pos)
    error = 0
    if keyword > 99: error = 2
    else:
        if len(k) < keyword + 1:
            indices_to_add = keyword-len(k)
            x = 0;
            while x < indices_to_add:
                k.append('')
                x += 1
            k.append(value)
        else: k[keyword] = value
        if debug_on: print(f'     [SAVED: {keyword}K = {value}]')
        pos = incr(pos)
    debug(12)
    return error, pos

def save_group(pos, group_id):
    debug(24)
    error = 0
    if group_id > 99: error = 2
    else:
        if len(g) < group_id + 1:
            indices_to_add = group_id - len(g)
            x = 0;
            while x < indices_to_add:
                g.append('')
                x += 1
            g.append(pos)
        else: g[group_id] = pos
        if debug_on: print(f'     [SAVED: G{group_id} = {pos}]')
        while program[pos] != '@':
            pos = incr(pos)
        pos = incr(pos)
        pos = skip_whitespace(pos)
    debug(25)
    return error, pos

def run_group(pos, group_id):
    debug(26)
    error = 0
    pos = g[group_id]
    debug(27)
    
    return error, pos

def skip_whitespace(pos):
    debug(13)
    while(pos < len(program)-1 and program[pos] in (' ','\n','\t')):
        pos = incr(pos)
    debug(14)
    return pos

def send_out(pos):
    debug(15)
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
            pos, value = get_string(pos)
            result += value
        
        pos = skip_whitespace(pos)
        
        if pos == len(program) or program[pos] != ',':
            eating = False
        else:
            pos = incr(pos)
            pos = skip_whitespace(pos)

    #OUTPUT MEDIUM OF CHOICE
    print(f'{result}')
    debug(16)
    return pos

def error_message(error, pos):
    #ERROR HANDING FUNCTION
    snippet = ""
    msg = ""
    if not error: snippet = "EOP"
    else:
        if error == 1: msg = "must be followed by keyword"
        if error == 2: msg = "max keyword index is 99"

        snippet += "\""
        for x in range(pos - 12, pos + 12):
            if x < len(program):
                if x == pos: snippet += f'<{msg}>'
                snippet += program[x]
            else:break
        snippet += "\""
    return snippet

def is_seperator(pos):
    debug(21)
    if program[pos]==':':
        debug(22)
        return 1
    debug(22)
    return 0

def is_operator(pos):
    debug(17)
    if program[pos] in ('+','-','*','/','^','%','~'):
        debug(18)
        return 1
    debug(18)
    return 0
    
def parse_keyword(pos):
    debug(19)
    current_keyword = 0
    #PARSE KEYWORD ASSIGNMENTS
    temp_pos, current_keyword = get_number(pos)
    temp_pos = incr(temp_pos)
    temp_pos = skip_whitespace(temp_pos)
    #ITS ANOTHER KEYWORD
    if is_keyword(temp_pos):
        temp_pos, value = get_keyword_value(temp_pos)
        error, pos = save_keyword_value(pos, value)
    #ITS A NUMBER
    elif program[temp_pos].isdigit():
        temp_pos, value = get_number(temp_pos)
        error, pos = save_keyword_value(pos, value)
    #ITS A STRING
    elif(program[temp_pos] == '$'):
        temp_pos, value = get_string(temp_pos)
        error, pos = save_keyword_value(pos, value)
    # elif is_operator(temp_pos):
        # print(program[temp_pos])
        # temp_pos = inc(temp_pos)
    pos = temp_pos
    debug(20)
    return pos

def parse_program():
    global k
    global g
    k = []
    g = []
    pos = 0
    g_pos = [] #array for storing group return addresses
    temp = ""
    error = 0
    while(not error and pos < len(program)-1):
        if(program[pos].isdigit()):
            if is_keyword(pos):
                pos = parse_keyword(pos)
        elif(program[pos].isalpha()):
            if program[pos] == 'O':
                #OUTPUT BUILTIN
                pos = send_out(pos)
            elif program[pos] == 'I':
                #INPUPT BUILTIN
                pos = incr(pos)
                pos = skip_whitespace(pos)
                if not is_keyword(pos):
                    error = 1
                else:
                    temp = input(">")
                    if temp == "Q":
                        pos = len(program) - 1
                    else:
                        error, pos = save_keyword_value(pos, temp)
                    
            elif program[pos] == 'L':
                #LOOP BUILTIN
                pos = incr(pos)
                debug(23)
                if program[pos] == 'G':
                    while pos > 0 and program[pos] != '@':
                        pos -= 1
                else:
                    while pos > 0 and program[pos] != ':' and program[pos] != '@':
                        pos -= 1
                pos = incr(pos)
            elif program[pos] == 'G':
                #GROUP HANDLER
                pos = incr(pos)
                pos, num = get_number(pos)
                pos = skip_whitespace(pos)
                
                if program[pos] == '@':
                    if len(g) < num  + 1 or g[num] == '':
                        pos = incr(pos)
                        error, pos = save_group(pos, num)
                    else:
                        g_pos.append(pos)
                        error, pos = run_group(pos, num)
                        
                else:
                    g_pos.append(pos)
                    error, pos = run_group(pos, num)
        elif program[pos] == '@':
            #GROUP RETURN HANDLER
            if g_pos:
                pos = g_pos.pop(-1)
            else:
                pos = incr(pos)
                pos = skip_whitespace(pos)
                    
        else:
            pos = incr(pos)

    if not error: temp = ""
    else: temp = f'ERROR at {pos}:'
    print(f'{temp}{error_message(error, pos)}')

def interpreter():
    #MAIN FUNCTION
    global program
    global console
    while console:
        program = input('>')
        if program[0] == 'P' and len(program) > 1:
            if program[1].isdigit():
                trash = ''
                trash += program[1]
                if len(program) > 2:
                    if program[2].isdigit():
                        trash += program[2]
                prog_id = int(trash)

                if len(programs) >= prog_id + 1:                
                    program = programs[prog_id]
                    parse_program()
                else:
                    print(f'ERROR: program {prog_id} doesn\'t exist!')
        else:
            parse_program()



interpreter()

