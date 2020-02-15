# AdvancedStatBot
A discord bot with advanced statistics for Brawl Stars.

Simple steps to use:

1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Set your API tokens (Discord and Brawl API) in the respective `.env` files
4. Run `python bot.py`

The brawl cog currently uses BrawlAPI to mitigate dynamic IP issues, to use the official API, just change the client syntax in the `/cogs/brawl.py` file.