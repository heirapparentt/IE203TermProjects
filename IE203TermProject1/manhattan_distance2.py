from pulp import *

def manhattan_distance_2(file_name):
    with open(file_name) as file:
        lines = file.readlines()
        
    # Initialization
    prob = LpProblem("Manhattan_Distance_2", LpMinimize)
    
    # Decision Variables
    x = LpVariable("x", 0)
    y = LpVariable("y", 0)
    tp = LpVariable.dicts("tpos", range(1, len(lines) + 1), lowBound=0) # + t's
    tn = LpVariable.dicts("tneg", range(1, len(lines) + 1), lowBound=0) # - t's
    hp = LpVariable.dicts("hpos", range(1, len(lines) + 1), lowBound=0) # + h's
    hn = LpVariable.dicts("hneg", range(1, len(lines) + 1), lowBound=0) # - h's
    
    # Objective Function
    prob += lpSum([tp[i] + tn[i] + hp[i] + hn[i] for i in range(1, len(lines) + 1)])
    
    # Constraints
    for i, line in enumerate(lines):
        a, b = map(float, line.rstrip().split(","))
        prob += x - a == tp[i+1] - tn[i+1]
        prob += y - b == hp[i+1] - hn[i+1]
        
    status = prob.solve()
    print("Status:", LpStatus[status])
    print(x.varValue, y.varValue)
    
    
    

file_name = "HW1_2022402150_case_1.txt"
manhattan_distance_2(file_name)