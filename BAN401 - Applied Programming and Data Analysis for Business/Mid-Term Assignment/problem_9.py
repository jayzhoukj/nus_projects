def check_prime():
    # Prompt the user for an integer
    number = int(input("Enter an integer: "))
    divisor_count = 0
    divisors = []

    # Check for all the divisors for that number
    for i in range(1,number+1):
        if number % i == 0:
            divisor_count += 1
            divisors.append(i)


    # If there are only 2 divisors (1 and the number itself), the number is a prime number.
    # Print the result of the prime number check.
    if divisor_count == 2:
        print(number, "is a prime number!")
    else:
        print(number, "is not a prime number, and it's smallest divisor is " + str(divisors[1]))

check_prime()

