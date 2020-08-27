### Function to get the new chain
def get_the_chain(numbers):

    ## Creating a new list sorted in ascending order with no duplicates
    # Remove duplicates
    global i
    new_numbers = []  # Empty list where non-repeated numbers are added
    for i in range(0, len(numbers)):
        if numbers[i] not in new_numbers:  # If number from original list not in 'new_numbers', add it in
            new_numbers.append(numbers[i])

    # Sort 'new_numbers' in ascending order
    for j in range(1, len(new_numbers)):        # Iterate 'new_numbers' starting from the 2nd index
        for k in range(0, len(new_numbers)):    # For each iteration, iterate 'new_numbers' starting from the 1st index
            if new_numbers[j] > new_numbers[k]: # If  number in the higher position is greater, keep the position
                continue
            else:
                new_numbers[j], new_numbers[k] = new_numbers[k], new_numbers[j] #If  number in higher position is lower, the numbers exchange position

    ## Finding consecutive chains
    # With 'new_numbers', go through each item in the list and create lists of "chains" that contain consecutive numbers in sequence
    all_chains = [] #List containing all consecutive chains
    num_chain = []
    index1 = 1

    for n in new_numbers:
        # Check if current chain is empty or if current number is a consecutive number in the current chain
        if (len(num_chain) == 0) or (num_chain[-1] + 1 == n):
            num_chain += [n] # Add the number to current chain

            # Updates current chain in 'all_chains'
            if index1 == len(new_numbers):
                all_chains += [num_chain]
            index1 += 1

        # If current number is not consecutive, a new 'num_chain' is created beginning with current number
        else:
            all_chains += [num_chain] # current chain added to 'all_chains'
            num_chain = [n] # restart 'num_chain'

            # Updates current chain in 'all_chains'
            if index1 == len(new_numbers):
                all_chains += [num_chain]
            index1 += 1

    ## Finding the longest consecutive chain that starts with the highest number
    # Find the lengths of all consecutive chains
    all_length = []
    for i in all_chains:
        all_length += [len(i)]

    # Find the index of the longest chain
    max = all_length[0]
    max_index = 0

    for l in range(0, len(all_length)):
        if all_length[l] >= max: # If length in this index > current highest length, update max and max_index
            max = all_length[l]
            max_index = l # Index of the max length


    ## Print required lists
    print('Initial number list: ', numbers)
    print('Resulting number list: ', all_chains[max_index])

### List where function will be applied to
num_list = [0, 7, 4, 8, 1, 3, 8, 10, 11, 2, 5, 12, 9]

get_the_chain(num_list)