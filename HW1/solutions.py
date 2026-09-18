# HW1 solutions
# work in progress - to the extent it exists - can be found in sandbox.ipynb

from typing import List
from math import sqrt, floor, pi
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# 2.a)
def nearest_armstrong(n: int) -> int:
    # walk out from n
    # on first encountered armstrong number, return
    dst = 0
    while True:
        if is_armstrong(n + dst): return n + dst
        if is_armstrong(n - dst): return n - dst
        dst += 1


def is_armstrong(n: int) -> bool:
    if n < 0: return False
    
    digits = [int(c) for c in str(n)]
    digits_ct = len(digits)
    raised_digits = [d ** digits_ct for d in digits]
    raise_digits_sum = sum(raised_digits)
    
    return  raise_digits_sum == n

# 2b)
def primes(a: int, b: int) -> List[int]:
    prime_list = [n for n in range(a, b + 1) if is_prime(n)]
    
    return prime_list

def is_prime(n: int) -> bool:
    for candidate in range(2, floor(sqrt(n)) + 1):
        if n % candidate == 0:
            return False
        
    return True

# 3
def draw_circle() -> None:
    _, ax = plt.subplots(figsize=(10, 6))

    ax.set_xlim(-1,3)
    ax.set_ylim(0,2)
    ax.set_aspect('equal') 
    
    ax.set_xticks(np.arange(-1, 3, 0.5)[1:])
    ax.set_yticks(np.arange(0, 2, 0.25)[1:])
    
    x = np.linspace(0, 2* pi)
    ax.plot(1+np.sqrt(0.75)*np.cos(x), 1+np.sqrt(0.75)*np.sin(x), color='red', linestyle='--', label="Circle boundary")
    ax.scatter(1,1, color='red', label="Center (1,1)")

    ax.set_title(r"Intersection of Sphere $(x-1)^2 + (y-1)^2 + (z-0.5)^2 = 1$ with $z = 0$", fontsize=16)
    plt.xlabel("x")
    plt.ylabel("y")   
    ax.legend()
    ax.grid(True)
    
    plt.show()
    
# 4
def password_comparator() -> tuple[str, int]:
    pass_a = input("Enter password A:")
    pass_b = input("Enter password B:")
    
    scorers = [char_score, pair_score, special_score, number_score, repeat_score]
    
    a = (pass_a, sum([score(pass_a) for score in scorers]))
    b = (pass_b, sum([score(pass_b) for score in scorers]))
    
    best = max(a,b, key=lambda x: x[1])
    
    print(f"Best password: '{best[0]}'")
    print(f"Score: {best[1]}")

def char_score(password: str) -> int:
    return max(len(password)-8, 0)

def pair_score(password: str) -> int:
    uppers: List[str] = []
    lowers: List[str] = []
    
    for c in password:
        if not c.isalpha(): continue
        
        if c.isupper():
            uppers.append(c)
        else:
            lowers.append(c)
    
    pair_ct = min(len(uppers), len(lowers))
        
    return 2 * pair_ct

def special_score(password: str) -> int:
    for c in password:
        if not c.isalpha() and not c.isnumeric(): return 0
        
    return -10

def number_score(password: str) -> int:
    for c in password:
        if c.isnumeric(): return 0
        
    return -10

def repeat_score(password: str) -> int:
    repeats = 0
    for i in range(len(password)-2):
        if password[i] == password[i+1] and password[i+1] == password[i+2]: 
            repeats += 1
            
    return -5 * repeats

# 5
def polynomial_fitting():

    data = np.loadtxt('/workspaces/Jeffrey_Mitchell_ROBO5000/hw1_jeffrey_mitchell/data/q5.csv', dtype='float', delimiter=',')

    x = data[:,0]
    y = data[:,1]
    z = data[:,2]

    xy = data[:,:2]

    polynomial_regression = make_pipeline(PolynomialFeatures(2), LinearRegression())
    polynomial_regression.fit(xy, z)

    x_space = np.linspace(0, 10, 100)
    y_space = np.linspace(0, 10, 100)
    XX, YY = np.meshgrid(x_space, y_space)

    grid = np.column_stack([XX.ravel(), YY.ravel()])

    Z_pred = polynomial_regression.predict(grid)


    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})


    ax.plot_surface(XX, YY, Z_pred.reshape(XX.shape), cmap='viridis', alpha=0.6)
    ax.scatter(x, y, z)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_title('3D Polynomial Regression (Degree 2)')

    plt.show()
