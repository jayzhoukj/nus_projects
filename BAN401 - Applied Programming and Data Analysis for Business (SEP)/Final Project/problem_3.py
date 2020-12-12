### Storing all the student data in different lists
first_name = ['Mike', 'Nancy', 'Steve', 'Mike', 'Jeffrey', 'Ivan', 'Sterling']
last_name = ['Wheeler', 'Wheeler', 'Harrington', 'Wazowski', 'Lebowski', 'Belik', 'Archer']
ids = ['19710', '19670', '19660', '18119', '69420', '12345', '11007']
gpa = [3.5, 3.6, 2.4, 2.9, 4.2, 1.8, 2.7]
major = ['FIE', 'ENE', 'STR', 'BAN', 'BLZ', 'BAN', 'MBM']
groups = ['it.gruppen', ['K7 Bulletin', 'NHHS Opptur', 'NHHS Energi'], 'N/A', 'N/A', ['NHHI Bowling', 'NHHI Vinum'], ['it.gruppen', 'NHHS Consulting'], 'NHHI Lacrosse']

### Function to retrieve info
def retrieval(i):
    print('Retrieving data for student {} {} (student ID {}).'.format(first_name[i], last_name[i], str(ids[i])))
    print('- GPA: ' + str(gpa[i]))
    print('- Major: ' + major[i])
    print('- NHHS group membership: ')
    if isinstance(groups[i], list): # Checks if a student has multiple groups
        for group in groups[i]:
            print('  - ' + group)
    else:
        print('  - ' + groups[i])


### Function used when there is several matches
def several_match(prompt, indexes_one):
    if prompt == 'all':
        for index in indexes_one:
            print('-------------')
            retrieval(index)
    elif (int(prompt) <= len(indexes_one) and int(prompt) >= 1):
        print('-------------')
        retrieval(int(prompt) - 1)
    else:
        print('Incorrect input. Please try again.')
        print('-------------')
        prompt = input('Enter the number of the search result for which you want to retrieve the info or enter all to print info for all matching results: \n')
        several_match(prompt, indexes_one)


### Function to inquire for new query
def new_query(execution):
    execution = execution.lower() # Changes input to lowercase
    if execution == 'n':
        print('Exiting the program...')
    elif execution == 'y':
        query()
    else:
        print('-------------')
        print('Incorrect input. Please try again.')
        print('-------------')
        execution = input('Would you like to make a new search? (y/n)\n')
        new_query(execution)

### Function which starts the query
def query():
    search = input('Who are you looking for?\n')
    search = search.title() # Changes input so the first letter of each word is capitalised
    search = search.split() # Splits the input so that words are elements in a list

    indexes_one = [] # Empty list where index of any match will be added if user enters 1 word
    indexes_two = [] # Empty list where index of any match will be added if user enters 2 words

    ## Matching
    if len(search) == 1: # Matching when user enters 1 word
        for i in range(len(first_name)): # Check if input matches any of the elements in the 'first_name', 'last_name' or 'ids' lists
            if search[0] == first_name[i]:
                indexes_one.append(i) # If there is a match, index will be added to 'indexes_one'
            if search[0] == last_name[i]:
                indexes_one.append(i)
            if search[0] == ids[i]:
                indexes_one.append(i)

    if len(search) == 2: #Matching when user enters 2 words
        for i in range(len(first_name)): # Check if 1st word in input matches any of the elements in the 'first_name', 'last_name' or 'ids' lists
            if search[0] == first_name[i]:
                if search[1] == last_name[i]: # Check if 2nd word in input also matches
                    indexes_two.append(i)  #If there is a match, index will be added to 'indexes_two'
            elif search[0] == last_name[i]:
                if search[1] == first_name[i]:
                    indexes_two.append(i)

    ## Output
    if len(indexes_one) == 1 or len(indexes_two) == 1: # Output for one match
        print('-------------')
        print('One match found.')
        print('-------------')
        if len(indexes_one) == 1:
            retrieval(indexes_one[0])
        if len(indexes_two) == 1:
            retrieval(indexes_two[0])

    elif len(indexes_one) == 0 and len(indexes_two) == 0: # Output for no match
        print('No matches found.')

    elif (len(indexes_one) > 1 and len(indexes_two) == 0): # Output for several matches
        print('Several results matched your query:')
        for n,i in zip(range(len(indexes_one)), indexes_one):
            print('{}. {} {} (ID {})'.format(str(n+1), first_name[i], last_name[i], str(ids[i]))) # Prints out a numbered list containing first name, last name and student IDs of all matches

        prompt = input('Enter the number of the search result for which you want to retrieve the info or enter all to print info for all matching results: \n')
        several_match(prompt,indexes_one)

    ## Request for new query
    print('-------------')
    execution = input('Would you like to make a new search? (y/n)\n')
    new_query(execution)

query()