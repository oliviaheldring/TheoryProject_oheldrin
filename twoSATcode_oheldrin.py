#!/usr/bin/env python3


#Name: Olivia Heldring
#NetID: oheldrin
#Teamname: Heldring (I worked alone)

#Project: Implementing a polynomial time 2-SAT solver 

import time



#Read input file function

def read_cnf(input_file_oheldrin):
    problems = []  #List to hold multiple problems
    current_problem = []  #Temporary storage for the current problem clauses
    problem_number = None
    num_clauses = None
    num_variables = None
    lines = input_file_oheldrin.splitlines()

    for line in lines:
        #Store the problem number
        if line.startswith('c'):
            parts = line.split()
            if len(parts) > 1:
                problem_number = int(parts[1])
            continue

        # Start a new problem when a new 'p cnf' line is encountered
        if line.startswith('p'):
            if current_problem:
                current_problem = []  # Reset for the new problem

            parts = line.split()
            if len(parts) > 3:
                num_clauses = int(parts[-1])  #get number of clauses
                num_variables = int(parts[-2]) #get number of variables

                problems.append((problem_number, num_clauses, num_variables, current_problem))
            continue

        # Process the literals in the clause
        literals = list(map(int, line.split()))
        if literals[-1] == 0:
            literals = literals[:-1]
        current_problem.append(literals)


    return problems  #return all the information from the input file sperated in a list of "problems"



# clause with only one literal -> set that literal to satisfy the clause
def unit_propagation(clauses, assignment):   #assignment keeps track of sat or unsat
    while True:
        unit_clauses = [clause for clause in clauses if len(clause) == 1] #list of clauses that are only 1
        if not unit_clauses:
            break  # No unit clauses left
        for unit in unit_clauses: #loop through single clauses
            literal = unit[0]  #grab the variable
            assignment.add(literal)  # ass literal to the asisgnment set 
            clauses = simplify(clauses, literal)  # Simplify the formula
    return clauses, assignment



# Pure Literal Elimination: If a literal appears with only one form, assign it
def pure_literal_elimination(clauses, assignment):
    literals = [lit for clause in clauses for lit in clause]  #grouping every variable into one
    for literal in set(literals):  #by using set, we eliminate all duplicates
        if -literal not in literals: #checks if the negation is in the set
            assignment.add(literal) #add if only one kind of 'polarity'
            clauses = simplify(clauses, literal) #simplify formula
    return clauses, assignment



# Simplify by removing clauses that are satisfied and removing satisfied literals from clauses
def simplify(clauses, literal):
    simplified = [] #list for updated clauses
    for clause in clauses: 
        if literal in clause: 
            continue  # Clause is satisfiable
        new_clause = [l for l in clause if l != -literal]  # keep clauses if literal is not satisfied
        simplified.append(new_clause)
    return simplified



# Check if the problem is empty (SAT) or contains an empty clause (UNSAT)
def is_satisfiable(clauses):
    if not clauses:
        return True  # No clauses means it's satisfiable
    if any(len(clause) == 0 for clause in clauses):
        return False  # Empty clause means it's unsatisfiable
    return None  # Neither SAT nor UNSAT, keep solving


# DPLL algorithm
def dpll(clauses, assignment=set()):
    
    #calling our key functions
    clauses, assignment = unit_propagation(clauses, assignment)
    clauses, assignment = pure_literal_elimination(clauses, assignment)

    #check if we can be done
    result = is_satisfiable(clauses)
    if result is not None:
        return result, assignment

    # Now we start to guess
    #Choose a literal (pick the first literal from the first clause)
    literal = clauses[0][0]
    
    # Recur with the chosen literal set to True
    new_clauses = simplify(clauses, literal)
    sat, final_assignment = dpll(new_clauses, assignment | {literal})
    if sat:
        return True, final_assignment

    # Recur with the chosen literal set to False
    new_clauses = simplify(clauses, -literal)
    return dpll(new_clauses, assignment | {-literal})



# Main function to test reading the CNF file

if __name__ == "__main__":

    # Open and read the input file
    with open("input_file_oheldrin", "r") as file:
        cnf_content = file.read()


    with open("output_file_oheldrin.txt", "w") as output_file:

    
        # Get list of problems from the input file
        problems = read_cnf(cnf_content)


        # Iterate through each problem and solve
        for problem_number, num_clauses, num_variables, clauses in problems:
        
            start_time = time.time()  #set timer

            # Print the Info for the current problem to the Terminal
            print(f"Problem number: {problem_number}")
            print(f"Number of clauses: {num_clauses}")
            print(f"Number of variables: {num_variables}")
            print(f"Number of Literals (clauses * 2): {num_clauses * 2}")
            print(f"Clauses: {clauses}")
            
            # Write results the current problem to the output file
            output_file.write(f"Problem number: {problem_number}\n")
            output_file.write(f"Number of clauses: {num_clauses}\n")
            output_file.write(f"Number of variables: {num_variables}\n")
            output_file.write(f"Number of Literals (clauses * 2): {num_clauses * 2}\n")
            output_file.write(f"Clauses: {clauses}\n")

           
            satisfiable, assignment = dpll(clauses)  #solve

            end_time = time.time()  #end timer
            elapsed_time = end_time - start_time


        #print satisfiability and time to terminal adn output file

            if satisfiable:
                print(f"The problem {problem_number} is satisfiable with assignment: {assignment}")
                print(f"Time taken: {elapsed_time:.4f} seconds\n")

                output_file.write(f"The problem {problem_number} is satisfiable with assignment: {assignment}\n")
                output_file.write(f"Time taken: {elapsed_time:.4f} seconds\n\n")

            else:
                print(f"The problem {problem_number} is unsatisfiable.")
                print(f"Time taken: {elapsed_time:.4f} seconds\n")

                output_file.write(f"The problem {problem_number} is unsatisfiable.\n")
                output_file.write(f"Time taken: {elapsed_time:.4f} seconds\n\n")

