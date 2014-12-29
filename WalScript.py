import math, sys, Tkinter, tkFileDialog
root = Tkinter.Tk()
root.withdraw()
runtime = []
out = []
operations = ['+','-','*','/','^','%']
boolops = ['=','>','<','>=','<=','!','&','|','$']
scriptIndex = 0
CustomErrors = []
ArgOffset = 0

def contains(l, e): #
    r = 0
    for x in l:
        if x == e:
            r = 1
    return r

def scriptError(errorType, line=0):
    errors = [['DivideByZero','You cannot divide by zero'],['AssertionError','An assertion failed'],['InvalidErrorCode','An invalid error was encountered'],['InvalidBool','A boolean with an invalid value was encountered']]+CustomErrors
    #if not contains(errors, errorType):
    #    scriptError('InvalidErrorCode')
    print('WalScript Error: '+errorType+' in line '+str(line))
    sys.exit()
    
def evalExp(expression):
    i = 0
    exp = expression
    if any(o in exp for o in boolops):
        exp = evalBool(expression)
    while i < len(exp):
        if exp[i] == '#':
            i2 = i+1
            while exp[i2] != '#' and i2 < len(exp):
                i2 = i2+1
            #i2 = i2+1
            exp = exp[:i]+runtime[runtime.index('var'+exp[i+1:i2])+1]+exp[i2+1:]
            i = -1
        i = i+1
    ns = vars(math).copy()
    ns['__builtins__'] = None
    exp = exp.replace('^','**')
    try:
        return eval(exp,ns)
    except NameError:
        return exp
        

def evalBool(expression):
    i = 0
    exp = expression
    while i < len(exp):
        if exp[i] == '$':
            i2 = i+1
            while exp[i2] != '$' and i2 < len(exp):
                i2 = i2+1
            #i2 = i2+1
            exp = exp[:i]+runtime[runtime.index('bool'+exp[i+1:i2])+1]+exp[i2+1:]
            i = -1
        i = i+1
    while '!' in exp:
        if exp[exp.find('!')+2] == '1':
            exp[exp.find('!')+2] == '0'
            exp[exp.find('!')] == ''
        elif exp[exp.find('!')+2] == '0':
            exp[exp.find('!')+2] == '0'
            exp[exp.find('!')] == ''         
        else:
            scriptError('InvalidBool',0)
    if '=' in exp:
        if evalExp(exp[0:exp.find('=')]) == evalExp(exp[exp.find('=')+1:len(exp)]):
            exp = 'b1'
        else:
            exp = 'b0'
    elif evalExp(exp[0:exp.find('!=')]) != evalExp(exp[exp.find('=')+2:len(exp)]):
            exp = 'b1'
        else:
            exp = 'b0'
    elif '>' in exp:
        if evalExp(exp[0:exp.find('>')]) > evalExp(exp[exp.find('>')+1:len(exp)]):
            exp = 'b1'
        else:
            exp = 'b0'
    elif '<' in exp:
        if evalExp(exp[0:exp.find('<')]) < evalExp(exp[exp.find('<')+1:len(exp)]):
            exp = 'b1'
        else:
            exp = 'b0'
            
    if '|' in exp or '&' in exp:
        expAO = exp.split('&')
        for x in len(expAO):
            expAO[x] = expAO[x].split('|')
        for x in len(expAO):
            if any(y in expAO[x] for y in ['b1']):
                expAO[x] = 'b1'
        if all(x == 'b1' for x in expAO):
            exp = 'b1'
    return exp
    
def getCommand(n,script):
    C = ''
    AC = 0
    i = 0
    while script[n][i] != '}':
        i = i+1
    C = script[n][:i]
    while i < len(script[n]):
        while i < len(script[n]) and script[n][i] != '}':
            i = i+1
        AC = AC+1
        i = i+1
    return [C, AC]

def getArg(n,C):
    A = ''
    i = 0
    for x in range(n):
        while C[i] != '}' and x != len(C):
            i = i+1
        i = i+1
    i2 = i
    while C[i] != '}' and i < len(C):
        i = i+1
    A = C[i2:i]
    if A[0] == '{':
        A = evalExp(A[1:])
    elif A[0] == '[':
        A = evalBool(A[1:])
    return A

def run(script,r=None):
    i = 0
    while getCommand(i,script)[0] != 'stop' and getCommand(i,script)[0] != 'debugsstop':
        C = script[i]
        com = getCommand(i,script)[0]
        Args = []
        for x in range(1, getCommand(i,script)[1]):
            Args = Args+[getArg(x,C)]
        ArgCount = getCommand(i,script)[1]-1
        
        if com == 'print': #Print Statement
            o = ''
            for x in range(1, getCommand(i,script)[1]):
               o = o+str(getArg(x,C))
            print(o)
            
        elif com == 'var': #Declare/set Variable
            if contains(runtime,'var'+Args[0]):
                o = ''
                for x in range(2, getCommand(i,script)[1]):
                    o = o+str(getArg(x,C))
                runtime[runtime.index('var'+Args[0])+1]=o
            else:
                o = ''
                for x in range(2, getCommand(i,script)[1]):
                    o = o+str(getArg(x,C))
                runtime.append('var'+Args[0])
                runtime.append(o)
                
        elif com == 'bool': #Declare/set Boolean
            if contains(runtime,'bool'+Args[0]):
                b = Args[1]
                if b == 't':
                    if b == 'b1':
                        b = 'b0'
                    else:
                        b = 'b1'
                runtime[runtime.index('bool'+Args[0])+1]=str(b)
            elif Args[1] == '1' or Args[1] == '0':
                runtime.append('bool'+Args[0])
                runtime.append('b'+str(Args[1]))
            else:
                scriptError('InvalidBool',i)

        elif com == 'if': #Conditional
            foundEnd = 0
            while foundEnd < 1:
                i2 = i2+1
                if getCommand(i2,script)[0] == 'endif':
                    foundEnd = foundEnd+1
                elif getCommand(i2,script)[0] == 'if':
                    foundEnd = foundEnd-1
            if not Args[0] == 'b1':
                i = i2

        elif com == 'input': #Set a variable based on input
            o = ''
            if contains(runtime,'var'+Args[0]):
                for x in range(1, ArgCount):
                    o = o+str(Args[x])
                runtime[runtime.index('var'+Args[0])+1] = raw_input(o)
            else:
                print('Error: var '+Args[0]+' not found')

        elif com == 'binput': #Set a boolean based on input
            o = ''
            if contains(runtime,'bool'+Args[0]):
                for x in range(1, ArgCount):
                    o = o+str(Args[x])
                runtime[runtime.index('bool'+Args[0])+1] = 'b'+str(raw_input(o))
            else:
                print('Error: bool '+Args[0]+' not found')
                
        elif com == 'list': #Make a List
            print('WIP')
            
        elif com == 'hold': #pause until user says something
            raw_input()
            
        elif com == 'stop': #Stops the Script
            break
        
        elif com == 'debugstop': #Stops the script, prints a message, and prints the runtime
            o = ''
            for x in range(1, getCommand(i,script)[1]):
               o = o+str(getArg(x,C))
            print(o)
            print('Runtime:')
            for x in runtime: print(x)
            print('Arguments:')
            for x in Args: print(x)
            break
        i = i+1
        i2 = i
        
    if r != None:
        return runtime[runtime.index('var'+r)+1]
    else:
        return ''

def runFile(name,r=None):
    with open(name) as f:
        program = f.read().splitlines()
        program = [x for x in program if x]
    if r == None:
        run(program)
    else:
        return run(program,r)

def openFile(r=None):
    if r == None:
        runFile(tkFileDialog.askopenfilename())
    else:
        runFile(tkFileDialog.askopenfilename(),r)

###########################################################################################
runFile("C:\Users\Nathan\Desktop\Programming\WalrusOS\WalTests\BoolTest.walrus")
