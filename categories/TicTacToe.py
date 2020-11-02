from discord.ext import commands
from models.Board import Board

board = Board()


class TicTacToe(commands.Cog):

    @commands.command(aliases=['ttt'], brief='Show TicTacToe rules.')
    async def tictactoe(self, ctx: commands.Context):
        board.reset_board()
        await ctx.send(embed=board.get_guide_embed())
        await ctx.send(embed=board.get_board_embed())
        await ctx.send(embed=board.get_turn_embed())

    @commands.command(aliases=['m'], brief='Make a move in TicTacToe board.', description='Valid inputs: 1-9')
    async def move(self, ctx: commands.Context, *args):
        message = ' '.join(*args)
        status = board.get_move_status(message)

        if status != board.SUCCESS_MESSAGE:
            await ctx.send(status)
            return

        move = int(message)
        board.place(move)

        await ctx.send(embed=board.get_board_embed())

        # Print out message and reset game if there is a winner or tie.
        if board.get_win_message():
            await ctx.send(embed=board.get_win_message_embed())
            board.reset_board()
            return
        # If not, other player will play.
        board.switch_player()
        await ctx.send(embed=board.get_turn_embed())
