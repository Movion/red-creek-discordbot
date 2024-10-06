import discord
from discord.ext import commands

# Replace these with your actual values
TOKEN = 'YOUR_BOT_TOKEN'
GUILD_ID = YOUR_GUILD_ID  # Replace with your server ID
VOICE_CHANNEL_ID = YOUR_VOICE_CHANNEL_ID  # Replace with the ID of the voice channel
TEXT_CHANNEL_ID = YOUR_TEXT_CHANNEL_ID  # Replace with the ID of the text channel
ROLE_ID = YOUR_ROLE_ID  # Replace with the ID of the role you want to mention

intents = discord.Intents.default()
intents.voice_states = True  # Enable voice state intents
intents.guilds = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

# This will hold the message object to update
current_message = None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_voice_state_update(member, before, after):
    global current_message

    # Get the guild and role
    guild = bot.get_guild(GUILD_ID)
    role = guild.get_role(ROLE_ID)

    # Debugging output
    if role is None:
        print(f"Role with ID {ROLE_ID} not found.")
        return  # Exit early if the role is not found

    # Link to the voice channel
    channel_link = f"<#{VOICE_CHANNEL_ID}>"

    # Check if the user joined the specific voice channel
    if after.channel is not None and after.channel.id == VOICE_CHANNEL_ID:
        # Get the text channel
        text_channel = guild.get_channel(TEXT_CHANNEL_ID)

        # List users currently in the voice channel
        members_in_channel = after.channel.members

        if current_message is None:
            # Create the message if it doesn't exist
            current_message = await text_channel.send(
                f"{role.mention} User(s) aktuell im {channel_link}: {', '.join(member.mention for member in members_in_channel)}"
            )
        else:
            # Update the existing message
            await current_message.edit(
                content=f"{role.mention} User(s) aktuell im {channel_link}: {', '.join(member.mention for member in members_in_channel)}"
            )

    elif before.channel is not None and before.channel.id == VOICE_CHANNEL_ID:
        # Check if the user left the voice channel
        members_in_channel = before.channel.members

        if len(members_in_channel) == 0:
            # If no members are left, delete the message
            if current_message:
                await current_message.delete()
                current_message = None
        else:
            # Update the existing message with the remaining members
            await current_message.edit(
                content=f"{role.mention} User(s) aktuell im {channel_link}: {', '.join(member.mention for member in members_in_channel)}"
            )

# Run the bot
bot.run(TOKEN)
