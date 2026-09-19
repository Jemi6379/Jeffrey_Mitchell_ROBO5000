# Collaborators: I asked my CP1 partner, Nolan A, what his q5 plot looked like,
# as I was surprised to see a plane rather than a curved surface

# HW1 solutions
# solutions arrived at through work in the root level sandbox.ipynb, catalogued here.

from typing import List
from math import sqrt, floor, pi
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from pathlib import Path
DATA = Path(__file__).parent / "data" / "q5.csv"


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
    # we're just gonna assume that negative numbers can't be armstrong
    # from the definition that seems to be the case? In any event, this is super
    # inefficient - constantly calling this function in the negative range
    # when we know it will never hit. Oh well! Not being graded on efficiency :^)
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
    if n <= 1: return False
    
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
def password_comparator():
    pass_a = input("Enter password A:")
    pass_b = input("Enter password B:")
    
    # I think this is super cute
    # one routine per rule with a consistent API: you give me the password, I return a score as
    # dictated by this particular rule. We then sum up contributions from all rules, and select the winner
    scorers = [char_score, pair_score, special_score, number_score, repeat_score]
    
    a = (pass_a, sum([score(pass_a) for score in scorers]))
    b = (pass_b, sum([score(pass_b) for score in scorers]))
    
    best = max(a,b, key=lambda x: x[1])
    
    print(f"Best password: '{best[0]}'")
    print(f"Score: {best[1]}")

def char_score(password: str) -> int:
    return max(len(password)-8, 0)

def pair_score(password: str) -> int:
    # sort chars into respective list by case
    # naturally, the shortest of the two will limit the number of pairs
    # that can be formed
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
    # short circuit on first special char encountered
    # if none encountered, -10
    for c in password:
        if not c.isalpha() and not c.isnumeric(): return 0
        
    return -10

def number_score(password: str) -> int:
    # short circuit on first number encountered
    # if none encountered, -10
    for c in password:
        if c.isnumeric(): return 0
        
    return -10

def repeat_score(password: str) -> int:
    # sliding window. Luckily contiguous blocks > 3 are counted multiple times
    # much simpler
    repeats = 0
    for i in range(len(password)-2):
        if password[i] == password[i+1] and password[i+1] == password[i+2]: 
            repeats += 1
            
    return -5 * repeats

# 5
def polynomial_fitting():

    data = np.loadtxt(DATA, dtype='float', delimiter=',')

    x = data[:,0]
    y = data[:,1]
    z = data[:,2]

    xy = data[:,:2]

    linear_regression = LinearRegression(fit_intercept=True)
    linear_regression.fit(xy, z)
    # 0.9901931581584443 R^2 - already sufficient

    polynomial_regression = make_pipeline(PolynomialFeatures(2), LinearRegression())
    polynomial_regression.fit(xy, z)
    # 0.99038458307019 R^2 - very marginally better? I guess?

    x_space = np.linspace(0, 10, 100)
    y_space = np.linspace(0, 10, 100)
    XX, YY = np.meshgrid(x_space, y_space)

    grid = np.column_stack([XX.ravel(), YY.ravel()])

    Z_pred = polynomial_regression.predict(grid)


    _, ax = plt.subplots(subplot_kw={'projection': '3d'})


    ax.plot_surface(XX, YY, Z_pred.reshape(XX.shape), cmap='viridis', alpha=0.6)
    # ax.set_xlim([0,10])
    # ax.set_ylim([0,10])
    # ax.set_zlim([0,300])

    ax.scatter(x, y, z)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_title('3D Polynomial Regression (Degree 2)')

    plt.show()

def main():
    print(nearest_armstrong(100))
    print(primes(0, 97))
    draw_circle()
    password_comparator()
    polynomial_fitting()

if __name__ == '__main__':
    main()