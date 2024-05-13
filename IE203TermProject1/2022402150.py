from pulp import *
import cvxpy as cp
import pandas as pd
import time
from tabulate import tabulate
from matplotlib import pyplot as plt


def get_points(file_name):
    x_values, y_values = [], []
    points = []
    
    with open(file_name) as file:
        lines = file.readlines()
        
    for line in lines:
        a, b = map(float, line.rstrip().split(","))
        x_values.append(a)
        y_values.append(b)
        points.append([a, b])
    
    return x_values, y_values, points

def manhattan_distance_1(data):
    start_time = time.process_time()
            
    # Initialize
    prob = LpProblem("ManhattanDistance1", LpMinimize)

    # Decision Variables
    x = LpVariable.dicts("x", range(len(data) + 1), lowBound=0) # x coords
    y = LpVariable.dicts("y", range(len(data) + 1), lowBound=0) # y coords

    # Objective Function
    prob += lpSum([x[i] + y[i] for i in range(1,len(data)+1)])

    # Constraints 
    for i, line in enumerate(data):
        a, b = line
        prob += x[0] - a <= x[i + 1]
        prob += a - x[0] <= x[i + 1]
        prob += y[0] - b <= y[i + 1]
        prob += b - y[0] <= y[i + 1]
        
    end_time = time.process_time()
    ptime = end_time - start_time
    prob.solve()
    
    return value(prob.objective), x[0].varValue, y[0].varValue, ptime


def manhattan_distance_2(data):
    start_time = time.process_time()
        
    # Initialization
    prob = LpProblem("Manhattan_Distance_2", LpMinimize)
    
    # Decision Variables
    x = LpVariable("x", 0)
    y = LpVariable("y", 0)
    tp = LpVariable.dicts("tpos", range(1, len(data) + 1), lowBound=0) # + t's
    tn = LpVariable.dicts("tneg", range(1, len(data) + 1), lowBound=0) # - t's
    hp = LpVariable.dicts("hpos", range(1, len(data) + 1), lowBound=0) # + h's
    hn = LpVariable.dicts("hneg", range(1, len(data) + 1), lowBound=0) # - h's
    
    # Objective Function
    prob += lpSum([tp[i] + tn[i] + hp[i] + hn[i] for i in range(1, len(data) + 1)])
    
    # Constraints
    for i, line in enumerate(data):
        a, b = line
        prob += x - a == tp[i+1] - tn[i+1]
        prob += y - b == hp[i+1] - hn[i+1]
        
    end_time = time.process_time()
    ptime = end_time - start_time
    prob.solve()
    
    return value(prob.objective), x.varValue, y.varValue, ptime


def euclidian_distance(data):
    start_time = time.process_time()

    x = cp.Variable()
    y = cp.Variable()

    obj_function = []

    for line in data:
        a, b = line
        obj_function.extend([cp.abs(x-a), cp.abs(y-b)])
        
    constraints = []

    obj = cp.Minimize(sum(obj_function))

    prob = cp.Problem(obj, constraints)
    
    end_time = time.process_time()
    ptime = end_time - start_time
        
    return prob.solve(), x.value, y.value, ptime
    

files = ["HW1_2022402150_case_1.txt", "HW1_2022402150_case_2.txt", "HW1_2022402150_case_3.txt"]

data_frames = []
data_x = []
data_y = []

for file_name in files:
    x_values, y_values, data = get_points(file_name)
    status1, x1, y1, time1 = manhattan_distance_1(data)
    status2, x2, y2, time2 = manhattan_distance_2(data)
    status3, x3, y3, time3 = euclidian_distance(data)

    df = pd.DataFrame({
        "n = 10": ["Task 1", "Task 2", "Task 3"],
        "z*": [status1, status2, status3],
        "x*": [x1, x2, x3],
        "y*": [y1, y2, y3],
        "Runtime": [time1, time2, time3]
    })

    data_frames.append(df.set_index("n = 10"))
    data_x.append(x_values)
    data_y.append(y_values)

for i in range(3):
    print()
    table = tabulate(data_frames[i], headers="keys", tablefmt="grid")
    plt.scatter(x_values[i], y_values[i])
    print(table)
    