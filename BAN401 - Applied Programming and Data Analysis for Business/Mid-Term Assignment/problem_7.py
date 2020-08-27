def draw_square():
    # Request for the length of each side of the square
    square_length = input("Enter n dimension ")

    # Check that the function is an integer, not float, and that it is more than zero to determine a natural number.
    # If not, request for another entry from the user.
    while not(square_length.isdigit() and int(square_length) > 0):
        print("Incorrect dimensions, please enter only natural numbers for n!")
        square_length = input("Enter n dimension ")

    square_length = int(square_length)

    # Use a for-loop to print each line of a square
    for i in range(square_length):
        # Print the first and last row with n number of "#" signs with a space in between since there is a space in between each newline.
        if i == 0 or i == (square_length - 1):
            print("# "*square_length)
        # For all intermediate rows between the first and the last, print only "#" corresponding to the first and last column. Whitespaces are printed in between.
        else:
            print("#"+" "*((square_length-2)*2+1)+"#")

# Run the function
draw_square()