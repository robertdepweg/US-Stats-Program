# PROGRAM: Pgm U11 - US Stats 
# AUTHOR: Robert Depweg
# DESCRIPTION: Searches a txt file, splitting it up into three seperate lists and 
#              prints a report to the terminal
# INPUT: The number of customers, the debt limit, the search phrase, and the state abbreviation
# OUTPUT: For both state selected and U.S.: How many customers live in 
#         the area, how many are over the debt limit, amount of people
#         whose name starts with the search phrase, and amount of 
#         customers who are debtless
# - - - - - - - - - - - - - - - - - - - - - - - - - VARIABLE INITIALIZATION
def main():
    ''' Execute main program logic '''
    user_input: str = ''            # Sentinel to stop user input
    num_customers: int = 0          # Number of records to read from file
    debt_limit: float = 0.0         # Upper debt limit bound
    search_phrase: str = ''         # First letter or few letters of last name
    st: str = ''                    # State abbreviation

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - INPUT
    names, states, debts = read_customer_data("USStats.txt")
        
    while user_input != 'q':
        try:
            num_customers = get_num_cust(names)
            debt_limit = get_debt_limit()  
            search_phrase = get_search_phrase() 
            st = get_state() 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -OUTPUT
            display_header(num_customers)
            highest_debt(debts, names, num_customers)
            cust_search(search_phrase, names, num_customers)
            no_debt(debts, debt_limit, num_customers)
            state_report(st, states, names, debts, num_customers)
            cust_search_state(st, names, states, search_phrase, num_customers)
            state_debt_report(st, debts, states, debt_limit, num_customers)
        except ValueError as err:
            print()
            print(err)
            print('Please enter data again.')
            print()
        print()
        user_input = input("Enter any key to continue ('q' to quit.): ")
        print()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCTIONS
def read_customer_data(user_file):
    ''' Reads in data from stats file '''
    name_list = [] # List of names from file
    states_list = [] # List of states from file
    debts_list = [] # List of debts from file
    with open(user_file, 'r') as infile:
        stats_list = infile.readlines()
    for line in stats_list:
        modified_line = line.strip('\n').split(',')
        names = modified_line[0]
        name_list.append(names)
        states = modified_line[1]
        states_list.append(states)
        debts_str = modified_line[2]
        debts_float = float(debts_str) 
        debts_list.append(debts_float)
    list_collection = (name_list, states_list, debts_list) # List tuple
    return list_collection 

def get_num_cust(names):
    ''' Obtains number of customers from user '''
    num_customers = input("Enter the number of customers: ")
    if not num_customers.isnumeric(): # Checks if input isn't integer
        raise ValueError(f'Error: Number of customers must be positive' 
                         'non-zero integer.')
    if int(num_customers) <= 0:
        raise ValueError(f'Error: Number of customers must greater' 
                         'than zero.')
    if int(num_customers) > len(names):
        raise ValueError(f'Error: Number of customers must be greater' 
                         ' than zero and less than the number of '
                         'records available.')
    return int(num_customers)

def get_debt_limit():
    ''' Obtains debt limit from user '''
    debt_limit = input('Enter debt limit: ')
    if not debt_limit.isnumeric() or len(debt_limit) <= 0:
        raise ValueError(f'Error: Debt must be positive number not' 
                         ' less than 0.')
    return int(debt_limit)

def get_search_phrase():
    ''' Obtains search phrase from user '''
    search_phrase = input('Enter search phrase: ')
    if not search_phrase.isalpha():
        raise ValueError('Error: Search phrase must be alphabetic.')
    return search_phrase

def get_state():
    ''' Obtains state abbreviation from user '''
    state = input('Enter state abbreviation: ')
    if len(state) > 2 or not state.isalpha():
        raise ValueError(f'Error: Enter a 2 character abbreviation '
                         'for state.')
    return state

def display_header(num_customers):
    ''' Displays first line of report header and 
    number of customers being considered '''
    print('U.S. Report')
    print(f'Customers: {num_customers}')

def highest_debt(debts, names, num_customers):
    ''' Finds highest debt among customers '''
    previous_debt = 0 # Holds previous debt value for comparison
    greatest_debt = 0 # Highest debt amount
    for index, debt in enumerate(debts[0:num_customers]):
        if debt > previous_debt:
            greatest_debt = names[index]
            previous_debt = debt
    print(f'Highest debt: {greatest_debt}')

def cust_search(search_phrase, names, num_customers):
    ''' Finds number of customers with name 
    starting with specified phrase '''
    counter = 0 # Counts number of names that start with search phrase
    for name in names[0:num_customers]:
        if name.startswith(search_phrase):
            counter += 1
    print(f'Customer names that start with ' +
          f'"{search_phrase}": {counter}')

def no_debt(debts, debt_limit, num_customers):
    ''' Gets customers with no debt and number 
    with debt above debt limit '''
    debt_limit_counter = 0 # Number of people above debt limit
    no_debt_counter = 0 # Amount of people with no debt
    for debt_amount in debts[0:num_customers]:
        if debt_amount > debt_limit:
            debt_limit_counter += 1
        if debt_amount == 0:
            no_debt_counter += 1
    print(f'Customers with debt over ${debt_limit}: ' +
          f'{debt_limit_counter}')
    print(f'Customers debt free: {no_debt_counter}')
    print()

def state_report(st, states, names, debts, num_customers):
    ''' State Report: count and highest debt of 
    customers in the requested state '''
    print(f'{st} Report')
    cust_count = 0 # Number of customers in state
    previous_debt = 0 # Holds previous debt value for comparison
    greatest_debt = 0 # Highest debt amount in state
    for index, debt in enumerate(debts[0:num_customers]):
        if st == states[index]:
            cust_count += 1
            if debt > previous_debt:
                greatest_debt = names[index]
                previous_debt = debt
    print(f'Customers: {cust_count}')
    print(f'Highest debt: {greatest_debt}')

def cust_search_state(st, names, states, search_phrase, num_customers):
    ''' Finds customers with name starting with specified 
    phrase for requested state '''
    counter = 0 # Number of names starting with search phrase in state
    for index, name in enumerate(names[0:num_customers]):
        if st == states[index] and name.startswith(search_phrase):
            counter += 1
    print(f'Customer names that start with '
          f'"{search_phrase}": {counter}')

def state_debt_report(st, debts, states, debt_limit, num_customers):
    ''' Finds customers with no debt and number with debt above 
    specified amount for requested state '''
    debt_limit_counter = 0  # Number of people above limit in state
    no_debt_counter = 0 # Amount of people with no debt in state
    for index, debt_amount in enumerate(debts[0:num_customers]):
        if st == states[index]:
            if debt_amount > debt_limit:
                debt_limit_counter += 1
            if debt_amount == 0:
                no_debt_counter += 1
    print(f'Customers with debt over '
          f'${debt_limit}: {debt_limit_counter}')
    print(f'Customers debt free: {no_debt_counter}')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == '__main__':
    main()