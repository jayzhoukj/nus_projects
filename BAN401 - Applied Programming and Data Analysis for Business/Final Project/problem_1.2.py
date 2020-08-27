# Prompt the user for a sequence of words
seq = input('Enter any sequence of words: ')

# Splits the sequence so that words are elements in a list and set() removes repetition
new_seq = set(seq.split())

# Sorts new sequence and joins the elements to form a string
new_seq = ' '.join(sorted(new_seq))

# Prints out the sorted sequence
print(new_seq)
