class File:
    def __init__(self, name):
        self.name = name
        pass
    def write(self, content):
        file = open(self.name, 'w')
        file.write(content)
        file.close()

    def get_lines(self):
        lines = []
        file = open(self.name)
        for line in file:
            lines.append(line)
        file.close()
        return lines

    def get_lines_until_latest(self, latest):
        lines = self.get_lines()
        latest = min(len(lines), latest)
        content = ''.join(lines[:-latest])
        return content

    def get_latest_lines(self, amount):
        lines = self.get_lines()
        amount = min(len(lines), amount)
        content = ''.join(lines[-amount:])
        return content

    def append(self, content):
        file = open(self.name, 'a')
        file.write(content)
        file.close()
