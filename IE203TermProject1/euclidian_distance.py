import cvxpy as cp

def euclidian_distance(file_name):
    with open(file_name) as file:
        lines = file.readlines()

    x = cp.Variable()
    y = cp.Variable()

    obj_function = []

    for line in lines:
        a, b = map(float, line.rstrip().split(","))
        print(a,",",b)
        obj_function.extend([cp.abs(x-a), cp.abs(y-b)])
        
    constraints = [
        
    ]

    obj = cp.Minimize(sum(obj_function))

    prob = cp.Problem(obj, constraints)
    prob.solve()
    print(prob.status)
    print(prob.value)
    print(x.value, y.value)


file_name = "HW1_2022402150_case_1.txt"