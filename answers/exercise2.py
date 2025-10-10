# 2-1
def myFunction(n): # Reuse, Input
    for i in range(n): # Iteration, Reuse, Input
        square = i * i # Reuse
        print(i, "squared is",square) # Output

raw = input("Please input a number: ") # Input, Reuse
try: # Conditional
    count = int(raw) # Reuse, Input
    myFunction(count) # Reuse, Input
except: # Conditional
    print("ERROR: Not a number!") # Output

# 2-2

# Input: Name
# Input: Age
# Input: Company
# Reusue: Capitalize all of the Company
# Output: display the name