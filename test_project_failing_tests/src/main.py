''' 
PYTHON PROGRAM WITH FAULTY TESTS  
Expects at least unittest to evaluate to false
'''

def addition_function_to_fail_unit_test(n1, n2):
    return (n1 + n2 + 1) 

if __name__ == "__main__":
    print(addition_function_to_fail_unit_test(5,5))
