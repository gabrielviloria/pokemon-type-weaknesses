import discord
import json
import os

# Returns the types (and multipliers) effective against the user's input(s)
def effective_types(type_chart, *types):
    # Delete duplicate typings
    types = set(types)
    # Reformat user input 
    formatted_types = [t.lower().capitalize() for t in types]
    # Dictionaries to hold supper-effective and immune types
    super_effective = {}
    immune = {}
    # Creates a dictionary which stores all type(s) that exist in type_chart as well as multipliers with a default value of 1.0
    multipliers = {k: 1.0 for k in type_chart.keys()}
    # Loops over the user's inputted type(s)
    for t in formatted_types:
        # Check if user input is a valid type
        if t not in type_chart:
            raise ValueError(f"{t} is not a valid type.")
    for t in formatted_types:
        # Loops over each key-value pair in the type_chart dictionary
        for k, v in type_chart.items():
            # Checks to see if user's provided type(s) exists in the dictionary (validity check)
            if t in v:
                # Multiply the current value of the corresponding key (k) in multipliers by the value in (v) which matches the user's current type (t)
                multipliers[k] *= v[t]
        # Loops over the existing dictionary and inserts/updates values into the corresponding dictionaries based on value
        for k, v in multipliers.items():
            if v >= 2.0:
                super_effective[k] = v
            elif v == 0.0:
                immune[k] = v
    # Return a dictionary containing key-value pairs that are greater or equal to 2.0
    return super_effective, immune


# Open the JSON file in read-only mode 
with open('pokemonchartmultipliers.json', 'r') as f:
    # Loads the JSON into type_chart
    type_chart = json.load(f)

# Discord Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

# Initializes the discord client with the configured intents
client = discord.Client(intents=intents)

# Debugging purposes to check if the bot is ready in console
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Monitors chat to see if someone wanted to invoke the command
@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    # Will trigger if the discord user sends a message with !poketype in the beginning
    if message.content.startswith('!poketype'):
        print("Received message: ", message.content)
        # Get the type input from the message content
        type_input = message.content.split()[1:]
        # Store the effective types into results
        
    # Attempts to store the results of the method into the two dictionaries
    try:
        super_effective, immune = effective_types(type_chart, *type_input)
    except ValueError as e:
        await message.channel.send(str(e))
        return

    # String formatting
    final_str = ''
    if len(super_effective) > 0:
        supereffective_str = ', '.join([f'{k} {str(v).replace(".0", "x")}' for k, v in super_effective.items()])
        final_str += f'**Super-effective**: {supereffective_str}\n'
    if len(immune) > 0:
        immune_str = ', '.join([f'{k} {str(v).replace("0.0", "")}' for k, v in immune.items()])
        final_str += f'**Immune To**: {immune_str}\n'
    if not final_str:
        final_str = 'No super-effective or immune types found.'
    # Send the results as a message
    await message.channel.send(final_str)

# Token grabbed from Environment Variables
token = os.environ['DISCORD_API_TOKEN']
# Run Client
client.run(token)