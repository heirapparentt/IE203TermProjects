from pulp import *


def manhattan_distance(file_name):
    with open(file_name) as file:
        lines = file.readlines()
        
    # Initialize
    prob = LpProblem("ManhattanDistance1", LpMinimize)

    # Decision Variables
    x = LpVariable.dicts("x", range(len(lines) + 1), lowBound=0) # x coords
    y = LpVariable.dicts("y", range(len(lines) + 1), lowBound=0) # y coords

    # Objective Function
    prob += lpSum([x[i] + y[i] for i in range(1,len(lines)+1)])

    # Constraints 
    for i, line in enumerate(lines):
        a, b = map(float, line.rstrip().split(","))
        prob += x[0] - a <= x[i + 1]
        prob += a - x[0] <= x[i + 1]
        prob += y[0] - b <= y[i + 1]
        prob += b - y[0] <= y[i + 1]
        
    status = prob.solve()
    print(LpStatus[status])
    print(x[0].varValue, y[0].varValue)
    

file_name = "HW1_2022402150_case_1.txt"

manhattan_distance(file_name)
