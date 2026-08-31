
#parses raw input text into formatted infix notation, removing spaces and adding symbols for implied multiplication, chunking tokens (including unary negative signs)
def lexing(exp:str) -> list:
    output = []
    negative = False

    i = 0
    while i < len(exp):
        c = exp[i]
        match c:
            case '*' | '/' | '+' | '^' | ')':
                if c != ')' and output and output[-1] in ['*', '/', '+', '-', '^', '(']:
                    raise SyntaxError('Unexpected token')
                output.append(c)
            case '(':
                if output and (output[-1][-1].isalnum() or output[-1] == ')'):
                    output.append('*')
                output.append('(')
            case '-':
                if not output or output[-1] in ['*', '/', '+', '-', '^', '(']:
                    negative = True
                else:
                    output.append('-')
            case _:
                if c.isalnum() or c == '.':
                    num = ""
                    while i < len(exp) and (exp[i].isalnum() or exp[i] == '.'):
                        num += exp[i]
                        i += 1
                    if negative:
                        num = '-' + num
                        negative = False
                    if output and output[-1] == ')':
                        output.append('*')
                    output.append(num)
                    continue
                else:
                    if c != ' ':
                        raise SyntaxError('Unexpected token')
        i += 1

    return output

def parsing(exp: list) -> list:
    output = []
    stack = []

    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    for token in exp:
        match token:
            case '(':
                stack.append(token)
            case '*' | '/' | '+' | '-':
                while stack and precedence.get(stack[-1], 0) >= precedence[token]:
                    output.append(stack.pop())
                stack.append(token)
            case '^':
                while stack and precedence.get(stack[-1], 0) > precedence[token]:
                    output.append(stack.pop())
                stack.append(token)
            case ')':
                while stack and stack[-1] != '(':   
                    output.append(stack.pop())
                if not stack:
                    raise SyntaxError("No matching open parenthesis")
                stack.pop()
            case _ if token.isalnum() or len(token) > 1:
                output.append(token)

    while stack:
        if stack[-1] == '(':
            raise SyntaxError("No matching close parenthesis")
        output.append(stack.pop())
    return output                    

def evaluate(exp: list) -> float:
    stack = []
    i = 0
    for token in exp:
        if token.isalnum() or len(token) > 1:
            stack.append(float(token))
        else:
            second = stack.pop()
            match token:
                case '+':
                    stack[-1] += second
                case '-':
                    stack[-1] -= second
                case '*':
                    stack[-1] *= second
                case '/':
                    stack[-1] /= second
                case '^':
                    stack[-1] = stack[-1] ** second
    return stack[-1]

def shunting(exp: str) -> float:
    tokens = lexing(exp)
    postfix = parsing(tokens)
    return evaluate(postfix)

with open('tests.txt') as f:
    for line in f:
        line = line.strip()
        print(line + " ➡️  " + str(shunting(line)))
