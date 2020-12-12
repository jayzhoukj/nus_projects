# Import required packages
import math
people = input("Enter the number of people that are going for the party: ")
# Reuse pizza() from Q11 to determine price from Little Sicily
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
    # print("Estimated pizza cost for the party from Little Sicily is $" + str(expected_expense))

    return expected_expense

# Define function to determine price from Big Tuscany
def pizza_competitor(no_of_people):
    people = no_of_people

    # Check that the input is a digit and is in the range of 1 to 50
    while not (people.isdigit() and (int(people) in list(range(1, 51)))):
        print("Incorrect input, please try again.")
        people = input("Enter the number of people that are going for the party: ")

    people = int(people)

    # Determine the number of pizza to order based on 4 person per pizza
    pizza_order = math.ceil(people / 4)

    # Calculate total cost of the pizza order
    expected_expense = pizza_order*15

    # Add $15 delivery fee for orders that are below $75
    if expected_expense < 75:
        expected_expense += 15

    # print("Estimated pizza cost for the party from Big Tuscany is $" + str(expected_expense))

    return expected_expense

def cheapest(no_of_people):

    little_sicily = pizza(no_of_people)
    big_tuscany = pizza_competitor(no_of_people)

    # Compare prices between Little Sicily and Big Tuscany and return which is the cheaper option as well as the price of the order
    if little_sicily < big_tuscany:
        print("If",
              no_of_people,
              "people came to the party, then the cheapest option would be Little Sicily and the cost would be $" +
              str(little_sicily))
    elif big_tuscany < little_sicily:
        print("If",
              no_of_people,
              "people came to the party, then the cheapest option would be Big Tuscany and the cost would be $" +
              str(big_tuscany))
    else:
        print("If",
              no_of_people,
              "people came to the party, then both Little Sicily and Big Tuscany costs the same, and the cost would be $" +
              str(little_sicily))

# Test the cheapest() function for 5, 20 and 50 people
# cheapest("5")
# cheapest("20")
# cheapest("50")

cheapest(people)