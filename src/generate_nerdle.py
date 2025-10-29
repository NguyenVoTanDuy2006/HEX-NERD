import random

def gen_problem():
    op = random.choice(['+', '-', '*', '/'])
    if op == '+':
        result = random.randint(10, 99)
        n1 = random.randint(1, result - 1)
        n2 = result - n1
    elif op == '-':
        n1 = random.randint(10, 99)
        n2 = random.randint(1, n1 - 1)
        result = n1 - n2
    elif op == '*':
        n1 = random.randint(2, 33) 
        max_n2 = 99 // n1
        if max_n2 < 1: max_n2 = 1
        n2 = random.randint(1, max_n2)
        result = n1 * n2
    elif op == '/':
        n2 = random.randint(2, 33)
        max_res = 99 // n2
        if max_res < 1: max_res = 1
        result = random.randint(1, max_res)
        n1 = n2 * result
    s_n1 = str(n1).zfill(2)
    s_n2 = str(n2).zfill(2)
    s_result = str(result).zfill(2)
    print(s_n1, s_n2, op, s_result) 
    return s_n1, s_n2, op, s_result