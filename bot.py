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

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user joined the specific voice channel
    if after.channel is not None and after.channel.id == VOICE_CHANNEL_ID:
        # Get the guild, text channel, and role using their IDs
        guild = bot.get_guild(GUILD_ID)
        text_channel = guild.get_channel(TEXT_CHANNEL_ID)
        role = guild.get_role(ROLE_ID)

        if text_channel and role:
            # Create a mention link for the voice channel
            channel_link = f"<#{VOICE_CHANNEL_ID}>"
            # Mention the role in the text channel
            await text_channel.send(f"{role.mention} User {member.mention} ist im {channel_link}!")

# Run the bot
bot.run(TOKEN)
