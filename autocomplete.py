import readline

# List of words for autocomplete
autocomplete_words = ["apple", "banana", "cherry", "date", "grape", "kiwi", "lemon", "orange"]

# Custom autocomplete function
def autocomplete(text, state):
    options = [word for word in autocomplete_words if word.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

# Register the autocomplete function
readline.set_completer(autocomplete)

# Enable tab-completion
readline.parse_and_bind("tab: complete")

# Main loop
try:
    while True:
        user_input = input("Enter a fruit (or 'exit' to quit): ")
        if user_input == "exit":
            break
        print(f"You entered: {user_input}")
except KeyboardInterrupt:
    print("\nTerminated by the user.")
