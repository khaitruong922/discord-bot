import random as rd
import json
import os
from discord.ext import commands

CHAT_FILE = 'data/chat.json'
NO_QUESTIONS = 'Câu hỏi đâu?'
NO_ANSWERS = 'Câu trả lời đâu?'
INSERT_SUCCESSFULLY = ':thumbsup:'


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
        question = ''.join(args)
        answers = get_answers(question)
        answers = answers if answers else get_answers('ngoaitamhieubiet')
        answers = answers if answers else ["Em không biết câu này. Dạy em với [name] ơi :yum:"]
        answer = rd.choice(answers)
        answer = parse_answer(answer, ctx)
        await ctx.send(answer)

    @commands.command(brief='Show chat bot IQ.')
    async def iq(self, ctx: commands.Context):
        data = get_chat_bot_data()
        iq = data.get('iq', 0)
        await ctx.send(f'{iq} IQ')

    @commands.command(aliases=['chatbot'], brief='Show chat bot data.')
    async def chat_bot(self, ctx: commands.Context):
        data = get_chat_bot_data()
        iq = data.get('iq', 0)
        question_count = data.get('question_count', 0)
        unique_answer_count = data.get('unique_answer_count', 0)
        await ctx.send(
            f'Chat Bot Profile:\n'
            f'- {iq} IQ\n'
            f'- Size: {os.stat(CHAT_FILE).st_size} B\n'
            f'- Trả lời được {question_count} câu hỏi.\n'
            f'- Học được {unique_answer_count} câu trả lời khác nhau.')


def insert(questions, answers):
    questions = [q for q in questions if q != '']
    answers = [a for a in answers if a != '']
    if not questions:
        return NO_QUESTIONS
    if not answers:
        return NO_ANSWERS
    with open(CHAT_FILE) as file:
        data = json.load(file)
        iq = 0
        for question in questions:
            file_answers = data.get(question, [])
            new_answers = [answer for answer in answers if answer not in file_answers and answer != '']
            iq += len(new_answers)
            file_answers += new_answers
            data[question] = file_answers
        with open(CHAT_FILE, 'w') as w_file:
            json_text = json.dumps(data, indent=2)
            w_file.write(json_text)
            return f'Chỉ số IQ tăng thêm {iq}'


def get_chat_bot_data():
    chat_bot_data = {}
    with open(CHAT_FILE) as file:
        data = json.load(file)
        iq = 0
        items = data.items()
        all_answers = []
        for question, answers in items:
            iq += len(answers)
            for answer in answers:
                all_answers.append(answer)
        unique_answer_count = len(set(all_answers))
        chat_bot_data['iq'] = iq
        chat_bot_data['question_count'] = len(items)
        chat_bot_data['unique_answer_count'] = unique_answer_count
        return chat_bot_data


def get_answers(question):
    question = format_question(question)
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
    return ''.join(c for c in question if c.isalnum()).lower()
