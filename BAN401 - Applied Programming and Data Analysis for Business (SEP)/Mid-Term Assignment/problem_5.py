# Define the solution within a function
def shipping_cost():
    # Store all the distances between destinations in a dictionary
    distances = {'B-O': 463.9, 'B-T': 628.7, 'O-T': 493.7}
    print("To find the shipping cost please enter")

    # Prompt the user for the origin and destination cities, and volume
    # to be transported, and store them in different variables
    origin_city = input("What is the origin city? ")
    dest_city = input("What is the destination? ")
    volume = float(input("What is the volume to be transported? "))

    # Remove whitespaces at the start and end of the origin and destination
    # string. Use the first letter of the locations as keys to the dictionary
    # containing the strings. Since the distance between 2 locations are the same
    # regardless of the order, try different orders (origin-destination,
    # destination-origin) to get the distance from the distances dictionary.
    try:
        shipping_path = origin_city.strip()[0].upper() + "-" + dest_city.strip()[0].upper()
        ship_distance = distances[shipping_path]
    except:
        shipping_path = dest_city.strip()[0].upper() + "-" + origin_city.strip()[0].upper()
        ship_distance = distances[shipping_path]

    # Calculate total shipping costs based on the distances and volume
    # and round to the nearest whole number.
    shipping_cost = round((volume*ship_distance/4) + 100)
    print("The total shipping cost is:", shipping_cost, "kr")

# Call the function
shipping_cost()