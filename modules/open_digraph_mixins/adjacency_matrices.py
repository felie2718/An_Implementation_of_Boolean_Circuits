'''
Constructs random adjacency matrices
'''

import random

def random_int_list(n, bound):
    '''
    n: int; Number of elements in the list
    bound: int; Maximum possible integer
    Generates a random list of length n, with integers from 0 to bound
    '''
    return [random.randrange(0, bound+1) for _ in range(n)]

def random_matrix(n, bound,null_diag=True, symmetric=False, oriented=False):
    '''
    n: int; Number of elements in the list
    bound: int; Maximum possible integer
    null_diag: bool; If True, nodes cannot connect with themselves
    symmetric: bool; If True, generates a symmetric graph
    oriented: bool; If True, generates an oriented graph
    dag: bool; If True, generates a directides acyclic graph
    Generates a random matrix of size n, with integers from 0 to bound
    '''
    M = [random_int_list(n, bound) for _ in range(n)]

    if null_diag:
        for i in range(n):
            M[i][i] = 0

    if symmetric:
        for i in range(n):
            for j in range(i):
                M[j][i] = M[i][j]
    
    if oriented:
        for i in range(n):
            for j in range(i):
                if M[j][i] != 0:
                    M[i][j] = 0

    return M

def random_dag_int_matrix(n, bound, null_diag = True):
    M = random_matrix(n, bound, null_diag, False, True)
    for i in range(n):
            for j in range(i):
                M[i][j] = 0
    return M
