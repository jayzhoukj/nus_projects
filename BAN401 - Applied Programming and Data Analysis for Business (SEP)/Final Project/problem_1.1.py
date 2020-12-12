# Numbers and their corresponding words are stored in a dictionary
Numbers = {0:'zero', 10: 'ten', 20: 'twenty', 30: 'thirty', 40: 'forty',
         50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety', 100: 'hundred'}

number_input = input('Key in a number from 0 to 100 which is a multiple of 10: ') # Prompting user to input a number

# Prompt the user for a number in the dictionary until a correct input is entered. Then, print the corresponding word of the number input.
while number_input not in [str(x) for x in Numbers.keys()]:
    print('Sorry, the input was not valid')
    number_input = input('Key in a number from 0 to 100 which is a multiple of 10: ')

print('The English word for ' + str(number_input) + ' is ' + Numbers[int(number_input)])