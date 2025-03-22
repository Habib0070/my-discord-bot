import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Ensure the bot token is loaded
if not TOKEN:
    print("Error: DISCORD_TOKEN is not set in the .env file.")
    exit()

# Set intents for bot to detect member join events
intents = discord.Intents.default()
intents.members = True  # Required to handle member join event
intents.message_content = True  # Enable message content intent to respond to commands

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Remove default help command
bot.remove_command('help')

# Event: When a new channel is created (for ticket creation)
@bot.event
async def on_guild_channel_create(channel: discord.TextChannel):
    """
    1?? This event listens for when a new channel is created.
    2?? If the channel name indicates it's a ticket (e.g., `ticket-0101`), the bot greets the user.
    """
    # Check if the new channel is a ticket (You can customize this to match your ticket tool naming convention)
    if 'ticket-' in channel.name:
        user = None

        for member in channel.members:
            user = member
            break  # Assume the first member is the one who opened the ticket

        if user:
            # Send a greeting in the ticket channel
            embed = discord.Embed(
                title=f"Hello {user.mention} :wave:",
                description=(
                    f"Thank you for reaching out! How can we assist you today? One of our team members will get to your request shortly.\n\n"
                    f"Here are some commands you can use:\n"
                    f"- :clipboard: `/myhelp`: Displays the list of available commands.\n"
                    f"- :credit_card: `/payment_method`: View available payment methods.\n"
                    f"- :moneybag: `/payha`: Get payment details for Admin HA.\n"
                    f"- :moneybag: `/paysh`: Get payment details for Admin SH.\n\n"
                    "Feel free to use any of the commands to get more information or navigate our support!"
                ),
                color=discord.Color.blue()  # Color of the embed
            )

            # Send the embed to the ticket channel
            await channel.send(embed=embed)

# Slash Command: /myhelp (Help Command)
@bot.tree.command(name='myhelp', description=':clipboard: Displays a list of available commands')
async def myhelp(interaction: discord.Interaction):
    embed = discord.Embed(title=":clipboard: Bot Commands", description="List of available commands:", color=discord.Color.blue())
    embed.add_field(name=":lock: `/auth`", value="Verify your identity in the server.", inline=False)
    embed.add_field(name=":bust_in_silhouette: `/view_account`", value="Check your verification status.", inline=False)
    embed.add_field(name=":credit_card: `/payment_method`", value="View available payment methods.", inline=False)
    embed.add_field(name=":moneybag: `/payha`", value="Get payment details for Admin HA.", inline=False)
    embed.add_field(name=":moneybag: `/paysh`", value="Get payment details for Admin SH.", inline=False)
    embed.set_footer(text="Use these commands to interact with the bot.")
    await interaction.response.send_message(embed=embed)

# Slash Command: /payment_method (Show Payment Methods)
@bot.tree.command(name='payment_method', description=':credit_card: View available payment methods')
async def payment_method(interaction: discord.Interaction):
    embed = discord.Embed(title=":credit_card: Available Payment Methods", description="Choose your preferred payment method:", color=discord.Color.green())
    embed.add_field(name=":large_orange_diamond: Binance", value="Secure cryptocurrency exchange.", inline=False)
    embed.add_field(name=":mobile_phone: Nagad", value="Mobile financial service for easy transactions.", inline=False)
    embed.add_field(name=":mobile_phone: Bkash", value="Convenient payment option via mobile.", inline=False)
    embed.add_field(name=":link: LTC", value="Litecoin address for payments: `LVo4KawK8EUJS8o42MFCfcL2VwjK671UYt`", inline=False)
    await interaction.response.send_message(embed=embed)

# Slash Command: /payha (Payment Details for Admin HA)
@bot.tree.command(name='payha', description=':moneybag: View payment details for Admin HA')
async def payHA(interaction: discord.Interaction):
    embed = discord.Embed(title=":moneybag: Payment Details - Admin HA", color=discord.Color.gold())
    embed.add_field(name=":large_orange_diamond: Binance ID", value="947740594", inline=False)
    embed.add_field(name=":mobile_phone: Nagad Number", value="01795-395747", inline=False)
    embed.add_field(name=":mobile_phone: Bkash Number", value="01795-395747", inline=False)
    await interaction.response.send_message(embed=embed)

# Slash Command: /paysh (Payment Details for Admin SH)
@bot.tree.command(name='paysh', description=':moneybag: View payment details for Admin SH')
async def paySH(interaction: discord.Interaction):
    embed = discord.Embed(title=":moneybag: Payment Details - Admin SH", color=discord.Color.gold())
    embed.add_field(name=":large_orange_diamond: Binance ID", value="962123136", inline=False)
    embed.add_field(name=":mobile_phone: Nagad Number", value="01742208442", inline=False)
    embed.add_field(name=":mobile_phone: Bkash Number", value="01742208442", inline=False)
    embed.add_field(name=":link: LTC Address", value="LVo4KawK8EUJS8o42MFCfcL2VwjK671UYt", inline=False)
    await interaction.response.send_message(embed=embed)

# Slash Command: /view_account (Check User's Verification Status)
@bot.tree.command(name='view_account', description=':bust_in_silhouette: Check your verification status')
async def view_account(interaction: discord.Interaction):
    # Simple verification status response
    await interaction.response.send_message(f":white_check_mark: **{interaction.user.name}** is verified!")

# Slash Command: /refresh_commands (Force Sync Slash Commands)
@bot.tree.command(name='refresh_commands', description=':arrows_counterclockwise: Refresh bot commands')
async def refresh_commands(interaction: discord.Interaction):
    await bot.tree.sync(guild=discord.Object(id=1285512825980321864))  # Your Guild ID
    await interaction.response.send_message(":white_check_mark: Slash commands have been refreshed!", ephemeral=True)

# Run the bot
bot.run(TOKEN)