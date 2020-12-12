# Allow the administrator to set the inventory and price in the next line
store_rental = {'Inventory': 30, 'Price': 10}

# Store the initial inventory amount in a variable to reference against for price adjustments
initial_inv = store_rental['Inventory']

def customer_order():
    # Allow the use of the initial inventory variable in the function
    global initial_inv

    # Terminate the program when there are no more board left for rental
    if store_rental["Inventory"] == 0:
        print("There are no more boards")
        return
    else:
        # Display inventory of surfboard and price of rental for customers
        print("Our inventory of surfboards is currently:",
              store_rental["Inventory"])
        print("The price is",
              round(store_rental['Price']),
              "per rental + 10 per board")

        # Request for the amount of surfboard the customer wishes to rent
        order_count = int(input("How many boards would you like to rent? "))

        # Check that the requested order does not exceed the available inventory for order.
        # If it does, request for another order amount from the customer.
        while order_count > store_rental['Inventory']:
            print("Order exceeds inventory, please try again")
            order_count = int(input("How many boards would you like to rent? "))

        # After the order amount is successfully verified and made, update the amount of surfboards in the inventory,
        store_rental['Inventory'] -= order_count

        # Check if the new inventory amount is below half of the initial inventory amount.
        # If it is, increase the rental price of each surfboard to 1.5 times.
        # "initial_inv" variable is set to 0 to prevent further price adjustments.
        if store_rental['Inventory'] <= (0.5*initial_inv):
            store_rental['Price'] *= 1.5
            initial_inv = 0

    # The function calls itself again for the next customer's order until the inventory is completely depleted.
    customer_order()

# Run the function
customer_order()