from discord.ext import commands
from model.Board import Board


class TicTacToe(commands.Cog):
    def __init__(self):
        self.board = Board()

    @commands.command(aliases=['ttt'], brief='Show TicTacToe rules.')
    async def tictactoe(self, ctx: commands.Context):
        self.board.reset_board()
        await ctx.send(embed=self.board.get_guide_embed())
        await ctx.send(embed=self.board.get_board_embed())
        await ctx.send(embed=self.board.get_turn_embed())

    @commands.command(aliases=['m'], brief='Make a move in TicTacToe board.', description='Valid inputs: 1-9')
    async def move(self, ctx: commands.Context, *args):
        message = ' '.join(*args)
        status = self.board.get_move_status(message)

        if status != self.board.SUCCESS_MESSAGE:
            await ctx.send(status)
            return

        move = int(message)
        self.board.place(move)

        await ctx.send(embed=self.board.get_board_embed())

        # Print out message and reset game if there is a winner or tie.
        if self.board.get_win_message():
            await ctx.send(embed=self.board.get_win_message_embed())
            self.board.reset_board()
            return
        # If not, other player will play.
        self.board.switch_player()
        await ctx.send(embed=self.board.get_turn_embed())
