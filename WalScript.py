import math, sys, Tkinter, tkFileDialog, re
commands = {
    'IMPORT':'import',
    'PRINT':'print',
    'VAR':'var',
    'BOOL':'bool',
    'INPUT':'input',
    'RINPUT':'rinput',
    'HOLD':'hold',
    'IF':'if',
    'ENDIF':'endif',
    'WHILE':'while',
    'ENDWHILE':'endwhile',
    'FUNCTION':'func',
    'FOR':'for',
    'ENDFOR':'endfor',
    'ENDFUNCTION':'endfunc',
    'EXPFUNCTION':'expfunction',
    'ENDEXPFUNCTION':'endexpfunction',
    'STOP':'stop',
    'DEBUGSTOP':'debugstop'
    }
spchars = {
    'SEP':'}',
    'OP':'{',
    'ALTOP':'['
    }
root = Tkinter.Tk()
root.withdraw()
loopStarts = [[],[]]
out = []
operations = {
    'PLUS':'+',
    'MINUS':'-',
    'MULTIPLY':'*',
    'DIVIDE':'/',
    'EXPONENT':'^',
    'MODULUS':'%'}
boolops = ['=','>','<','>=','<=','!','&','|','$']
expcommands = {'char':'char'}
scriptIndex = 0
CustomErrors = []
ArgOffset = 0
order = '^*/%+-'
defaultruntime = {'var':{},
                  'bool':{},
                  'func':{},
                  'pyfunc':{},
                  'class':{},
                  'instance':{}
    }

def contains(l, e): #find if list l contains element e
    r = 0
    for x in l:
        if x == e:
            r = 1
    return r

def find_nth(haystack, needle, n): #Find the nth occurence of needle in haystack
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def scriptError(errorType, line=0): #Handle errors in the script
    errors = {'conflictingNamespace':'A conflicting namespace was used',
              'namespaceNotFound':'An undefined namespace was used',
              'divideByZero':'You cannot divide by zero',
              'assertionError':'An assertion failed',
              'invalidErrorCode':'An invalid error was encountered',
              'invalidBool':'A boolean with an invalid value was encountered'
              }+CustomErrors #Script errors
    validError = False
    if errorType in errors:
        validError=True
    if not validError:
        scriptError('InvalidErrorCode', line)
    print('WalScript Error: '+errorType+' in line '+str(line))
    sys.exit()
    
def evalExp(expression, runtime): #Evaluate expressions
    i = 0
    exp = expression
    if any(o in exp for o in boolops):
        exp = evalBool(expression, runtime)
    while i < len(exp):
        if exp[i] == '#':
            i2=exp.find('#',i+1)
            exp = exp[:i]+runtime['var'][exp[i+1:i2]]+exp[i2+1:]
            i = -1
        i = i+1

    while any(s in exp for s in expcommands):
        if 'char' in exp:
            spos = exp.find('char')+5
            epos = spos
            fend = 0
            splitpos = []
            while fend < 1:
                epos = epos+1
                if exp[epos] == ')':
                    fend = fend+1
                elif exp[epos] == '(':
                    fend = fend-1
                elif exp[epos] == ',' and fend == 0:
                    splitpos = epos
            exp = exp[:spos-5]+exp[splitpos+1:epos][int(exp[spos:splitpos])]+exp[epos+1:]
        else:
            pass #This will be the custom functions with return variables

    ns = vars(math).copy()
    ns['__builtins__'] = None
    exp = exp.replace('^','**')
    try:
        return eval(exp,ns)
    except NameError:
        return exp
    except SyntaxError:
        return exp

def evalBool(expression, runtime):
    i = 0
    exp = expression
    while i < len(exp):
        if exp[i] == '$':
            i2 = i+1
            while exp[i2] != '$' and i2 < len(exp):
                i2 = i2+1
            #i2 = i2+1
            exp = exp[:i]+runtime['bool'][exp[i+1:i2]]+exp[i2+1:]
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
            exp = '1'
        else:
            exp = '0'
    elif '!=' in exp:
        if evalExp(exp[0:exp.find('!=')]) != evalExp(exp[exp.find('=')+2:len(exp)]):
            exp = '1'
        else:
            exp = '0'
    elif '>' in exp:
        if evalExp(exp[0:exp.find('>')]) > evalExp(exp[exp.find('>')+1:len(exp)]):
            exp = '1'
        else:
            exp = '0'
    elif '<' in exp:
        if evalExp(exp[0:exp.find('<')]) < evalExp(exp[exp.find('<')+1:len(exp)]):
            exp = '1'
        else:
            exp = '0'
            
    if '|' in exp or '&' in exp:
        expAO = exp.split('&')
        for x in len(expAO):
            expAO[x] = expAO[x].split('|')
        for x in len(expAO):
            if any(y in expAO[x] for y in ['1']):
                expAO[x] = '1'
        if all(x == '1' for x in expAO):
            exp = '1'
    return exp

def getCommand(n,script):
    C = ''
    AC = 0
    i = 0
    while script[n][i] != spchars['SEP']:
        i = i+1
    C = script[n][:i]
    while i < len(script[n]):
        while i < len(script[n]) and script[n][i] != spchars['SEP']:
            i = i+1
        AC = AC+1
        i = i+1
    return [C, AC]

def getArg(n,C,runtime, raw=False):
    A = ''
    i = 0
    for x in range(n):
        while C[i] != spchars['SEP'] and x != len(C):
            i = i+1
        i = i+1
    i2 = i
    while C[i] != spchars['SEP'] and i < len(C):
        i = i+1
    A = C[i2:i]
    if raw == True:
        return A
    if A[0] == spchars['OP']:
        A = evalExp(A[1:], runtime)
    elif A[0] == spchars['ALTOP']:
        A = evalBool(A[1:], runtime)
    return A

def listify(o):
    return [x for x in o]

def run(script,rt=defaultruntime,r=None):
    ret = ''
    runtime = rt
    i = 0
    while getCommand(i,script)[0] != commands['STOP'] and getCommand(i,script)[0] != commands['DEBUGSTOP'] and getCommand(i,script)[0] != 'passStop' and i != len(script):
        C = script[i]
        com = getCommand(i,script)[0]
        Args = []
        for x in range(1, getCommand(i,script)[1]):
            Args = Args+[getArg(x,C,runtime)]
        ArgCount = getCommand(i,script)[1]-1

        if com == commands['IMPORT']:
            runFile(Args[0])
        
        elif com == commands['PRINT']: #Print Statement
            o = ''
            for x in range(1, getCommand(i,script)[1]):
               o = o+str(getArg(x,C,runtime))
            print(o)
            
        elif com == commands['VAR']: #Declare/set Variable
            if Args[1] == 't':
                runtime['bool'][Args[0]] = not runtime['bool'][Args[0]]
            else:
                runtime['bool'][Args[0]] = Args[1]
                
        elif com == commands['BOOL']: #Declare/set Boolean
            o = ''
            for x in range(2, getCommand(i,script)[1]):
                o = o+str(getArg(x,C,runtime))
            runtime['bool'][Args[0]]=o

        elif com == commands['IF']: #Conditional
            foundEnd = 0
            while foundEnd < 1:
                i2 = i2+1
                if getCommand(i2,script)[0] == commands['ENDIF']:
                    foundEnd = foundEnd+1
                elif getCommand(i2,script)[0] == commands['IF']:
                    foundEnd = foundEnd-1
            if not Args[0] == '1':
                i = i2

        elif com == commands['WHILE']: #Conditional Loop
            foundEnd = 0
            while foundEnd < 1:
                i2 = i2+1
                if getCommand(i2,script)[0] == commands['ENDWHILE']:
                    foundEnd = foundEnd+1
                elif getCommand(i2,script)[0] == commands['WHILE']:
                    foundEnd = foundEnd-1
            if str(Args[0]) == '1':
                loopStarts[0].append(i)
            else:
                i = i2

        elif com == commands['ENDWHILE']:
            i = loopStarts[0][-1]-1
            loopStarts[0].pop(-1)

        elif com == commands['FOR']: #For Loop
            pass
            
        elif com == commands['ENDFOR']:
            pass

        elif com == commands['FUNCTION']:
            i2 = i
            fArgs = []
            while getCommand(i2,script)[0] != commands['ENDFUNCTION']:
                i2 = i2+1
            for x in range(1,ArgCount+1):
                if getArg(x,C,runtime,True)[0] == spchars['OP']:
                    fArgs.append('var'+getArg(x,C,runtime,True)[1:len(getArg(x,C,runtime,True))])
                elif getArg(x,C,runtime,True)[0] == spchars['ALTOP']:
                    fArgs.append('boo'+getArg(x,C,True)[2:len(getArg(x,C,True))])
            runtime['func'][Args[0]]={'command':C[5:],'Args':fArgs,'script':script[i+1:i2]}
            i = i2
            
        elif com == commands['EXPFUNCTION']:
            i2 = i
            runtime.append('expfunc'+getArg(1,C,runtime))
            runtime.append(C[5:])
            fArgs = []
            while getCommand(i2,script)[0] != commands['ENDEXPFUNCTION']:
                i2 = i2+1
            for x in range(1,ArgCount+1):
                if getArg(x,C,runtime,True)[0] == spchars['OP']:
                    fArgs.append('var'+getArg(x,C,runtime,True)[1:len(getArg(x,C,runtime,True))])
                elif getArg(x,C,runtime,True)[0] == spchars['ALTOP']:
                    fArgs.append('boo'+getArg(x,C,True)[2:len(getArg(x,C,True))])
            runtime.append(fArgs)
            runtime.append(script[i+1:i2])
            i = i2

        elif com == commands['ENDEXPFUNCTION']:
            ret = getArg(1,C,True)

        elif com == commands['INPUT']: #Set a variable or boolean based on input
            o = ''
            if Args[0] in runtime['var']:
                for x in range(1, ArgCount):
                    o = o+str(Args[x])
                runtime['var'][Args[0]] = getArg(1,'c'+spchars['SEP']+raw_input(o)+spchars['SEP'],runtime)
            elif Args[0] in runtime['bool']:
                for x in range(1, ArgCount):
                    o = o+str(Args[x])
                runtime['bool'][Args[0]] = getArg(1,'c'+spchars['SEP']+raw_input(o)+spchars['SEP'],runtime)
            else:
                scriptError('namespaceNotFound',i)

        elif com == commands['RINPUT']: #Set a variable based exactly on an input
            o = ''
            if Args[0] in runtime['var']:
                for x in range(1, ArgCount):
                    o = o+str(getArg(x,C,runtime,True))
                runtime['var'][Args[0]] = raw_input(o)
            else:
                scriptError('namespaceNotFound',i)
    
        elif com == commands['LIST']: #Make a List
            print('WIP')
            
        elif com == commands['STOP']: #Stops the Script
            runtime = []
            break
        
        elif com == commands['DEBUGSTOP']: #Stops the script, prints a message, and prints the runtime
            o = ''
            for x in range(1, getCommand(i,script)[1]):
               o = o+str(getArg(x,C,runtime))
            print(o)
            print('runtime:')
            for x in runtime: print(x)
            print('Arguments:')
            for x in Args: print(x)
            runtime = []
            break
        
        elif contains(runtime, 'func'+getCommand(i,script)[0]):
            rti = runtime.index('func'+getCommand(i,script)[0])
            fArgs = []
            for x in range(ArgCount):
                fArgs.append(runtime[rti+2][x])
                fArgs.append(getArg(x+1,C,runtime))
            runtime = run(runtime[rti+3], runtime+fArgs, 'runtime')
        i = i+1
        i2 = i
            
    if r != None:
        if r == 'runtime':
            return runtime
        elif r == 'ret':
            return ret
        else:
            return runtime[runtime.index('var'+r)+1]
    else:
        return None

def runFile(name,r=None):
    with open(name) as f:
        program = f.read().replace('\n',';').replace(';;',';')
        program = program.split(';')
        program = [x for x in program if x]
        program = [x.strip() for x in program]
        for x in program:
            print(x)
    if r == None:
        run(program)
    else:
        return run(program,[],r)

def openFile(r=None):
    if r == None:
        runFile(tkFileDialog.askopenfilename())
        return None
    else:
        return runFile(tkFileDialog.askopenfilename(),r)

###########################################################################################
#mode = raw_input('Mode: ')
#if mode == 'o':
    #print 'mode==\'o\''
openFile()
#elif mode == 't':
#    runFile("C:\Users\Nathan\Desktop\Programming\WalrusOS\WalTests\VarTest.walrus")
#elif mode == 'b':
#    run(['print}{5+2/3*9}','debugstop}'])
