word = 'Deceptivenesses'

# Create empty list to convert the string to a list
word_list = []

# Store each character of the string in a list
for i in word:
    word_list.append(i)

count_e = 0

# Use a for-loop to determine the number of times 'e' appears in the given string
for i in word_list:
    if i=='e':
        count_e += 1

print("The letter 'e' occurs", count_e, "times.")