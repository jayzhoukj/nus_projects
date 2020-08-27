# Import required packages
import math

# Prompt for the number of people attending the party
people = input("Enter the number of people that are going for the party: ")

def pizza(no_of_people):
    people = no_of_people

    # Check that the input is a digit and is in the range of 1 to 50
    while not(people.isdigit() and (int(people) in list(range(1,51)))):
        print("Incorrect input, please try again.")
        people = input("Enter the number of people that are going for the party: ")

    people = int(people)

    # Determine the number of pizza to order based on 4 person per pizza
    pizza_order = math.ceil(people/4)

    # Calculate the total price of the pizza order
    if 1 <= pizza_order <= 5:
        expected_expense = (pizza_order*20) + 5
    elif 6 <= pizza_order <= 10:
        expected_expense = (pizza_order*15) + 5
    elif pizza_order > 10:
        expected_expense = (pizza_order*10) + 5

    # Display the printed results of the total order price
    print("Estimated pizza cost for the party from Little Sicily is $" + str(expected_expense))

    return expected_expense

pizza(people)
