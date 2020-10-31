import random as rd
import json
from discord.ext import commands

MODEL_FILENAME = '../data/chat.json'


class Chat(commands.Cog):

    @commands.command(brief='Train bot.')
    async def train(self, ctx: commands.Context, *args):
        questions_content, answers_content = ' '.join(args).split("|")
        questions = list(map(format_question, questions_content.split('&')))
        answers = list(map(format_answer, answers_content.split('&')))
        with open(MODEL_FILENAME) as file:
            data = json.load(file)
            for question in questions:
                file_answers = data.get(question, [])
                for answer in answers:
                    if answer not in file_answers:
                        file_answers.append(answer)
                data[question] = file_answers
            with open(MODEL_FILENAME, 'w') as w_file:
                json_text = json.dumps(data, indent=4)
                w_file.write(json_text)
        await ctx.send(f':thumbsup:')

    @commands.command(aliases=['ask', 'c'], brief='Chat with bot.')
    async def chat(self, ctx: commands.Context, *args):
        question = ''.join(args)
        question_key = format_question(question)
        with open(MODEL_FILENAME) as file:
            data = json.load(file)
            answers = data.get(question_key,
                               data.get('ngoaitamhieubiet', ["Em không biết câu này. Dạy em với [name] ơi :yum:"]))
            answer = rd.choice(answers)
            answer = parse_answer(answer, ctx)
            await ctx.send(answer)


def format_answer(answer):
    return answer.strip()


def parse_answer(answer, ctx: commands.Context):
    if "[" not in answer:
        return answer
    markdown_dict = {
        "[name]": ctx.author.name,
        "[random-name]": rd.choice(ctx.guild.members).name
    }
    for markdown, str_to_replace in markdown_dict.items():
        answer = answer.replace(markdown, str_to_replace)
    return answer


def format_question(question):
    return ''.join(c for c in question if c.isalnum()).lower()
