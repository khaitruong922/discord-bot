import random as rd
import json
import os
from discord.ext import commands
import math

CHAT_FILE = 'data/chat.json'
NO_QUESTIONS = 'Câu hỏi đâu?'
NO_ANSWERS = 'Câu trả lời đâu?'
INSERT_SUCCESSFULLY = ':thumbsup:'
SPACE_SEP = '_'


class Chat(commands.Cog):

    @commands.command(brief='Train bot.')
    async def train(self, ctx: commands.Context, *args):
        questions, answers = ' '.join(args).split("|")
        questions = list(map(format_question, questions.split('&')))
        answers = list(map(format_answer, answers.split('&')))
        message = insert(questions, answers)
        await ctx.send(message)

    @commands.command(aliases=['sync'], brief='Add all answers of a question to other questions.')
    async def copy(self, ctx: commands.Context, *args):
        old_question, new_questions = ' '.join(args).split("->")
        new_questions = list(map(format_question, new_questions.split('&')))
        answers = get_answers(old_question)
        if not answers:
            await ctx.send(f'Không tìm thấy câu hỏi: {old_question}')
            return
        message = insert(new_questions, answers)
        await ctx.send(message)

    @commands.command(aliases=['ask', 'c'], brief='Chat with bot.')
    async def chat(self, ctx: commands.Context, *args):
        question = SPACE_SEP.join(args)
        answers = get_answers(question)
        answers = answers if answers else get_answers('ngoai_tam_hieu_biet')
        answers = answers if answers else ["Em không biết câu này. Dạy em với [name] ơi :yum:"]
        answer = rd.choice(answers)
        answer = parse_answer(answer, ctx)
        await ctx.send(answer)

    @commands.command(brief='Show chat bot IQ.')
    async def iq(self, ctx: commands.Context):
        await ctx.send(f'{get_iq()} IQ')

    @commands.command(aliases=['chatbot'], brief='Show chat bot data.')
    async def chat_bot(self, ctx: commands.Context):
        await ctx.send(
            f'Chat Bot Profile:\n'
            f'- {int(get_iq())} IQ\n'
            f'- Size: {get_file_size()} B\n'
            f'- Trả lời được {get_question_count()} câu hỏi.\n'
            f'- Học được {get_unique_answer_count()} câu trả lời khác nhau.')


def insert(questions, answers):
    questions = [q for q in questions if q != '']
    answers = [a for a in answers if a != '']
    if not questions:
        return NO_QUESTIONS
    if not answers:
        return NO_ANSWERS
    old_iq = get_iq()
    data = get_chat_data()
    for question in questions:
        file_answers = data.get(question, [])
        new_answers = [answer for answer in answers if answer not in file_answers and answer != '']
        file_answers += new_answers
        data[question] = file_answers
    write_chat_data(data)
    new_iq = get_iq()
    return f'Chỉ số IQ tăng thêm {round(new_iq - old_iq, 2)}'


def get_chat_data():
    with open(CHAT_FILE) as file:
        return json.load(file)


def write_chat_data(data):
    with open(CHAT_FILE, 'w') as w_file:
        json_text = json.dumps(data, indent=2)
        w_file.write(json_text)


def get_file_size():
    return os.stat(CHAT_FILE).st_size


def get_iq():
    data = get_chat_data()
    answer_count = 0
    for answers in data.values():
        answer_count += len(answers)
    iq = math.log10(answer_count) * 50
    return iq


def get_question_count():
    data = get_chat_data()
    return len(data.keys())


def get_unique_answer_count():
    data = get_chat_data()
    all_answers = []
    for answers in data.values():
        all_answers += answers
    unique_answers = set(all_answers)
    return len(unique_answers)


def get_answers(question):
    question = format_question(question)
    print(question)
    with open(CHAT_FILE) as file:
        data = json.load(file)
        answers = data.get(question, [])
        return answers


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
    question = question.strip().lower()
    question = SPACE_SEP.join(question.split())
    return ''.join(c for c in question if c.isalnum() or c == SPACE_SEP)
