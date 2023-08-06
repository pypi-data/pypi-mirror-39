# =============================================================================
# ValueFile
# =============================================================================
class ValueFile:

    def __init__(self, file_name=''):
        self.file_name = file_name
        self.lines = []
        self.value = ''
        if file_name:
            self.lines = open(file_name, 'r').read().splitlines()
            for line in self.lines:
                line = line.strip()
                if line != '' and line[0] != '#':
                    self.value = line
                    break

    def save(self, file_name=''):
        if file_name == '':
            file_name = self.file_name
        else:
            self.file_name = file_name
        with open(file_name, 'w') as f:
            for full_line in self.lines:
                line = full_line.strip()
                if line == '' or line[0] == '#':
                    f.write(full_line)
                else:
                    f.write(self.value)
                f.write('\n')
