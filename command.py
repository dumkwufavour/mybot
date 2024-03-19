import random
import asyncio
from discord.ext import commands

#for playing the game
def setup_commands(bot):
    @bot.command(name="test", help="This is a test command.")
    async def test_command(ctx):
        await ctx.send("Test command executed!")  
    
    @bot.command(name="hello", help="Say hello to Alita.")
    async def hello_command(ctx):
        await ctx.send(f"Hi!, {ctx.author.mention}!")
    
    @bot.command(name="Alita")
    async def alita(ctx):
        await ctx.send(f"Hello {ctx.author.mention}, yes, how can I help you? Type a command to get started")

    @bot.command(name='startgame', help='Start a new guess game')
    async def start_game(ctx, difficulty='medium'):
        user_games = {}

        if ctx.author.id in user_games:
            await ctx.send("You already have an active game. Finish it before starting a new one.")
            return

        if difficulty == 'easy':
            range_max = 50
        elif difficulty == 'hard':
            range_max = 200
        else:
            range_max = 100

        current_number = random.randint(1, range_max)
        user_games[ctx.author.id] = {'current_number': current_number, 'attempts': 0}

        await ctx.send(f'Guess the number between 1 and {range_max}! Type `$guess <number>` to make a guess.')

        # Start a timer for game timeout (e.g., 5 minutes)
        await asyncio.sleep(300)
        if ctx.author.id in user_games:
            del user_games[ctx.author.id]
            await ctx.send("Game timeout. The correct number was not guessed in time.")

    @bot.command(name='guess', help='Make a guess in the current game')
    async def make_guess(ctx, guess: int):
        user_games = {}

        if ctx.author.id not in user_games:
            await ctx.send('No active game. Start a new game with `$startgame`.')
            return

        current_number = user_games[ctx.author.id]['current_number']
        user_games[ctx.author.id]['attempts'] += 1

        if guess == current_number:
            attempts = user_games[ctx.author.id]['attempts']
            del user_games[ctx.author.id]
            await ctx.send(f'Congratulations! {ctx.author.mention} guessed the correct number in {attempts} attempts!')
        elif guess < current_number:
            await ctx.send('Too low! Try a higher number.')
        else:
            await ctx.send('Too high! Try a lower number.')

    @bot.command(name='endgame', help='End the current game')
    async def end_game(ctx):
        user_games = {}

        if ctx.author.id in user_games:
            del user_games[ctx.author.id]
            await ctx.send('Game ended. You can start a new game with `$startgame`.')
        else:
            await ctx.send('No active game. Start a new game with `$startgame`.')

    @bot.command(name='leaderboard', help='Show the leaderboard')
    async def leaderboard(ctx):
        user_games = {}

        leaderboard = sorted(user_games.items(), key=lambda x: x[1]['attempts'])
    
        if leaderboard:
            leaderboard_str = ''
            for user_id, data in leaderboard:
                member = ctx.guild.get_member(user_id)
                display_name = member.display_name if member else f"User ID: {user_id}"
                leaderboard_str += f'{display_name}: {data["attempts"]} attempts\n'

            await ctx.send(f'Leaderboard:\n{leaderboard_str}')
        else:
            await ctx.send('No games played yet. Start a game with `$startgame`.')
