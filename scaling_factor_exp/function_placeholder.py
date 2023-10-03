import numpy as np

def S(a,b,c,n):
    return c / (1 + np.exp(-a * (n - b)))

def S_prime(a,b,c,n):
    return c * a * np.exp(-a * (n - b)) / (1 + np.exp(-a * (n - b)))**2

def L(a,b,c,n):
    return S_prime(a,b,c,b) * (n - b) + S(a,b,c,b)

def K(n):
    return min(1,S(n)/L(n))