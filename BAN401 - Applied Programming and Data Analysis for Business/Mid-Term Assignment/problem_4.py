def armstrong_check(start, stop):
    # Use a for loop to check for armstrong numbers between the given range
    armstrong_count = 0
    armstrong_numbers = []

    for i in range(start, stop+1):
        number = str(i)
        x = len(number)
        total = 0

        # Use another for loop to determine the sum of all digits raised to the power of N
        for n in number:
            total += int(n)**x

        # Check if the sum total of digits raised to power N is the same as the beginning number, print if it is an armstrong number
        if total == i:
            armstrong_numbers.append(str(i))
            armstrong_count += 1

    # Print the number of Armstrong numbers in the given range, and the value of those numbers
    print("There are", armstrong_count, "armstrong numbers, and they are:",
          ', '.join(armstrong_numbers) + ".")

#Print the number of Armstrong numbers between 100 and 1000
armstrong_check(100, 1000)