import re


# =============================================================================
# VarsFile
# =============================================================================
class VarsFile:

    # self.file_name = str
    # self.lines = [VarsLine]

    # =========================================================================
    # __init__
    # =========================================================================
    def __init__(self, file_name=''):
        self.file_name = file_name
        self.lines = []
        if file_name:
            line = VarsLine()
            self.lines.append(line)
            lines = open(file_name, 'r').read().splitlines()
            for full_line in lines:
                line.add_line(full_line)
                if line.name != '':
                    line = VarsLine()
                    self.lines.append(line)
            if line.name == '' and len(line.comments) == 0:
                self.lines.remove(line)

    # =========================================================================
    # save
    # =========================================================================
    def save(self, file_name=''):
        if file_name == '':
            file_name = self.file_name
        else:
            self.file_name = file_name
        with open(file_name, 'w') as f:
            for line in self.lines:
                for comment in line.comments:
                    f.write(comment + '\n')
                if line.name != '':
                    f.write('{0!r}\n'.format(line))

    # =========================================================================
    # print
    # =========================================================================
    def print(self):
        for line in self.lines:
            for comment in line.comments:
                print(comment)
            if line.name != '':
                print('{0!r}'.format(line))

    # =========================================================================
    # get_line
    # =========================================================================
    def get_line(self, name):
        name = name.lower()
        for line in self.lines:
            if line.name.lower() == name:
                return line
        return None

    # =========================================================================
    # get_value
    # =========================================================================
    def get_value(self, name):
        line = self.get_line(name)
        return None if line is None else line.value

    # =========================================================================
    # set_value
    # =========================================================================
    def set_value(self, name, value):
        if value is None:
            self.remove_value(name)
        else:
            line = self.get_line(name)
            if line is None:
                line = VarsLine()
                line.add_line(name + '=' + value)
                self.lines.append(line)
            else:
                line.value = value

    # =========================================================================
    # remove_value
    # =========================================================================
    def remove_value(self, name):
        line = self.get_line(name)
        if line is not None:
            self.lines.remove(line)


# =============================================================================
# VarsLine
# =============================================================================
class VarsLine:

    def __init__(self):
        self.comments = []
        self.name = ''
        self.value = ''
        self._allowed = re.compile('^[A-Za-z0-9]*$')

    def add_line(self, full_line):
        line = full_line.strip()
        if line != '' and line[0] != '#':
            i = line.find('=')
            if i != -1:
                self.name = line[:i].rstrip()
                self.value = line[i+1:].lstrip()
                if self.value[0] == '"' and self.value[-1] == '"':
                    self.value = self.value[1:-1]
            else:
                self.name = line
        else:
            self.comments.append(full_line)

    def __repr__(self):
        value = self.value
        if not self._allowed.match(value):
            value = '"' + value + '"'
        return self.name + '=' + value
