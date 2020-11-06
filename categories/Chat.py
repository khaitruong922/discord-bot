import random as rd
import json
import os
from _datetime import datetime
from discord.ext import commands
import math
import re

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
        old_question = format_question(old_question)
        answers = get_answers(old_question)
        if not answers:
            await ctx.send(f'Không tìm thấy câu hỏi: {old_question}')
            return
        message = insert(new_questions, answers)
        await ctx.send(message)

    @commands.command(aliases=['ask', 'c'], brief='Chat with bot.')
    async def chat(self, ctx: commands.Context, *args):
        question = format_question(' '.join(args))
        answers = get_answers(question)
        answers = answers if answers else get_answers('ngoai_tam_hieu_biet')
        answers = answers if answers else ["Em không biết câu này. Dạy em với [name] ơi :yum:"]
        answer = rd.choice(answers)
        answer = parse_answer(answer, ctx)
        if not answer:
            await ctx.send("Không có nội dung.")
        await ctx.send(answer)

    @commands.command(aliases=['chatbotinfo'], brief='Show chat bot data.')
    async def chatbot(self, ctx: commands.Context):
        await ctx.send(
            f'Chat Bot Profile:\n'
            f'- {round(get_iq(), 2)} IQ\n'
            f'- Size: {get_file_size_kb()} KB\n'
            f'- Trả lời được {get_question_count()} câu.\n')


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
    with open(CHAT_FILE, 'w') as file:
        json_text = json.dumps(data, indent=2)
        file.write(json_text)


def get_file_size_kb():
    return round(os.stat(CHAT_FILE).st_size / 1024, 2)


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


def get_answers(question):
    data = get_chat_data()
    answers = data.get(question, [])
    return answers


def format_answer(answer):
    return answer.strip()


def get_markdown_dict(ctx: commands.Context):
    now = datetime.now()
    return {
        "[hour]": now.hour,
        "[min]": now.minute,
        "[grade]": rd.choice(['NN', 'PA', 'CR', 'DI', 'HD']),
        "[name]": ctx.author.name,
        "[random-name]": rd.choice(ctx.guild.members).name
    }


def parse_answer(answer, ctx: commands.Context):
    answer = translate(get_markdown_dict(ctx), answer)
    answer = parse_conditional(answer)
    return answer


def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


def parse_conditional(answer):
    condition_groups = re.findall('{.*?}', answer)
    condition_inners = re.findall('{(.*?)}', answer)
    for i, condition in enumerate(condition_inners):
        condition = condition.strip()
        conditional_data = get_conditional_data(condition)
        if not conditional_data:
            continue
        var = conditional_data.get('var')
        op = conditional_data.get('op')
        compare_value = conditional_data.get('compare_value')
        true_value = conditional_data.get('true_value')
        false_value = conditional_data.get('false_value')
        if is_number(var):
            var = float(var)
            if is_number(compare_value):
                compare_value = float(compare_value)
        compare_result = compare(var, op, compare_value)
        if compare_result is None:
            continue
        value = true_value if compare_result else false_value
        answer = answer.replace(condition_groups[i], value)
        # print(f'Result: {compare_result}')
        # print(f'Value: {value}')
    return answer


def compare(this, op, that):
    if op == '==':
        return this == that
    if op == '!=':
        return this != that
    if op == '>':
        return this > that
    if op == '>=':
        return this >= that
    if op == '<=':
        return this <= that
    if op == '<':
        return this < that
    if op.lower() == 'in':
        try:
            open_bracket, close_bracket = that[0], that[-1]
            lower, upper = tuple(that[1:-1].strip().split(','))
            if is_number(lower) and is_number(upper):
                lower, upper = float(lower), float(upper)
                lower_condition, upper_condition = False, False
                if open_bracket == '(':
                    lower_condition = lower < this
                if open_bracket == '[':
                    lower_condition = lower <= this
                if close_bracket == ')':
                    upper_condition = upper > this
                if close_bracket == ']':
                    upper_condition = upper >= this
                return lower_condition and upper_condition
        except IndexError:
            return None
    return None


def translate(d: dict, content: str):
    for key, str_to_replace in d.items():
        if "[" not in content:
            break
        content = content.replace(key, str(str_to_replace))
    return content


def format_question(question):
    question = question.strip().lower()
    question = ''.join(c for c in question if c.isalnum() or c.isspace())
    question = SPACE_SEP.join(question.split())
    return question


def get_conditional_data(content: str):
    try:
        parts = content.split('?')
        condition = parts[0].split(' ')
        var = condition[0].strip()
        op = condition[1].strip()
        compare_value = condition[2].strip()
        values = parts[1].split(':')
        true_value = values[0].strip()
        false_value = ''
        if len(values) > 1:
            false_value = values[1].strip()

        return {
            'var': var,
            'op': op,
            'compare_value': compare_value,
            'true_value': true_value,
            'false_value': false_value
        }
    except IndexError:
        return None
