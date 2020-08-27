def word_in_sentence():
    # Request the user to input a sentence for checking
    sentence_input = input("Please enter a sentence (without any numbers, punctuation, or special characters): ")

    # Prompt for the word to check in the sentence
    word_input = input("Enter the word to check if it is in the sentence: ")

    # Generate a list of all the words in the sentence by splitting based on whitespaces in the sentence
    sentence_list = sentence_input.split(sep = " ")

    if word_input in sentence_list:
        # Return the position of the word in the sentence
        print("The word \"" + word_input + "\" is at position", sentence_list.index(word_input)+1, "in the sentence.")
    else:
        print("The word is not in the sentence")

word_in_sentence()