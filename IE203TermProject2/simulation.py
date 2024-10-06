import numpy as np
import pandas as pd


file_names = ["HW2_2022402150_10.txt",
              "HW2_2022402150_100.txt",
              "HW2_2022402150_1000.txt"]


def mse(base_arr, compare_arr):
    return np.sum(np.square(base_arr-compare_arr))/len(base_arr)


def pull_file(file_name):
    return np.genfromtxt(file_name, delimiter=" ")


def method_analytic_solution(arr):
    eigenvalues, eigenvectors = np.linalg.eig(arr.T)
    left_eigenvector = eigenvectors[:, np.where(np.isclose(eigenvalues, 1))[0][0]].T 
    left_eigenvector /= np.sum(left_eigenvector) 
    return np.real(left_eigenvector)

def method_simulation(arr, T=1000000):
    count = 0
    arr_len = len(arr[0])
    realizations = {i:0 for i in range(arr_len)}
    current_row = arr[np.random.randint(0, arr_len)]
    while count < T:
        r = np.random.random()
        for c, entry in enumerate(current_row):
            r -= entry
            if r <= 0:
                break
        realizations[c] += 1
        current_row = arr[c]
        count += 1
    return np.array(list(realizations.values()))/T
            

def method_matrix_multiplication(arr, tolerance=0.000001):
    size = len(arr[0])
    not_done = True
    steps = 0
    while not_done:    
        for c in range(size):      
            fault = False
            column = arr[:, c]
            col_avg = np.sum(column)/size    
            for entry in column:
                if np.abs(entry- col_avg) >= tolerance:
                    fault = True
                    break
            if fault:
                break    
        else:
            not_done = False    
        if not_done:         
            arr = np.matmul(arr, arr)
            steps += 1        
    return arr[0]


def create_dataframe(file_names):
    datasets = {}

    for  n, dataset in enumerate(file_names):
        arr = pull_file(dataset)

        analytic = method_analytic_solution(arr)
        simulation = method_simulation(arr)
        multiplication = method_matrix_multiplication(arr)


        df_dict = {(f"Dataset {n+1}", "MSE"): ["-", mse(analytic, simulation), mse(analytic, multiplication)],
                   (f"Dataset {n+1}", "Runtime (s)"): [None, None, None]}

        datasets.update(df_dict)
        if n == 1:
            break

    method_indexes = ["Method 1", "Method 2", "Method 3"]
    df = pd.DataFrame(data=datasets)
    df.index = method_indexes
    return df


def test_5(arr):
    arr_len = len(arr[0])
    arr[0] = np.array([1] + [0 for i in range(arr_len-1)])
    return method_analytic_solution(arr), method_simulation(arr), method_matrix_multiplication(arr)

