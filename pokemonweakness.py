import json

# Returns the types (and multipliers) effective against the user's input(s)
def effective_types(type_chart, *types):
    # Creates a dictionary which stores all type(s) that exist in type_chart as well as multipliers with a default value of 1.0
    multipliers = {k: 1.0 for k in type_chart.keys()}
    # Loops over the user's inputted type(s)
    for t in types:
        # Loops over each key-value pair in the type_chart dictionary
        for k, v in type_chart.items():
            # Checks to see if user's provided type(s) exists in the dictionary (validity check)
            if t in v:
                # Multiply the current value of the corresponding key (k) in multipliers by the value in (v) which matches the user's current type (t)
                multipliers[k] *= v[t]
    # Return a dictionary containing key-value pairs that are greater or equal to 2.0
    return {k: v for k, v in multipliers.items() if v >= 2.0 or v == 0}

# Open the JSON file in read-only mode 
with open('pokemonchartmultipliers.json', 'r') as f:
    # Loads the JSON into type_chart
    type_chart = json.load(f)
# Prompt the user for input
type_input = input("Enter the opponent type(s) (separated by a space): ")
# Split the input into a list of types
types = type_input.split()
# Store the effective types into results in descending order based on the key's values
results = sorted(effective_types(type_chart, *types).items(), key=lambda x: x[1], reverse=True)
# Print the contents of results
print(results)