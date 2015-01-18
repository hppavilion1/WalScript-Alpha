#Program to check the WalScript files
import math, sys, Tkinter, tkFileDialog
root = Tkinter.Tk()
root.withdraw()
runtime = []
loopStarts = []
out = []
operations = ['+','-','*','/','^','%']
boolops = ['=','>','<','>=','<=','!','&','|','$']
scriptIndex = 0
CustomErrors = []
ArgOffset = 0
commands = []
issues = []

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
    elif '!=' in exp:
        if evalExp(exp[0:exp.find('!=')]) != evalExp(exp[exp.find('=')+2:len(exp)]):
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

def check(script):
    for i in range(len(script)):
        C = script[i]
        com = getCommand(i,script)[0]
        Args = []
        Args = [Args+[(getArg(x,C))] for x in range(1,getCommand(i,script)[1])]
        #for x in range(1, getCommand(i,script)[1]):
        #    Args = Args+[getArg(x,C)]
        ArgCount = getCommand(i,script)[1]-1
        checklist = {
            'validComs':True,
            'validArgCounts':True
            'validSyntax':True
            }

        if not contains(commands[0],com): #Check that all commands are valid
            print('Command Error Discovered')
            checklist['validComs'] = False
            issues.append(['invalid command in line'+str(i)+': ',C])

        if commands[1][commands[0].index(com)] != -1: #Check that there's a valid argcount
            if str(ArgCount) != commands[1][commands[0].index(com)]:
                print('ArgCount Error Discovered')
                checklist['validArgCounts'] = False
                issues.append(['invalid argcount in line'+str(i)+': ', C, 'expected '+str(commands[1][commands[0].index(com)])+', got '+str(ArgCount)])

        if script[i][-1] != '}': #Check for missing }
            print('Syntax Error Discovered')
            checklist['validSyntax'] = False
            issues.append(['invalid syntax in line'+str(i)+': ', C, 'expected line to end with }'])
        
    return [checklist,issues]

def checkFile(name):
    with open(name) as f:
        program = f.read().splitlines()
        program = [x for x in program if x]
    with open("commands.txt") as f:
        commands.append(f.read().splitlines())
    with open("args.txt") as f:
        commands.append(f.read().splitlines())
    commands[1] = [int(x) for x in commands[1]]
    ch = check(program)
    print('results:')
    for x in ch[0]:
        print('\t'+x)
    print('issues:')
    for x in ch[1]:
        for y in range(len(x)):
            if y == 0:
                print x[y]
            else:
                print '\t'+x[y]


def openFile(r=None):
    checkFile(tkFileDialog.askopenfilename())

###########################################################################################
#runFile("C:\Users\Nathan\Desktop\Programming\WalrusOS\WalTests\BoolTest.walrus")
openFile()
