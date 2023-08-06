import re


# =============================================================================
# HostsFile
# =============================================================================
class HostsFile:

    HOSTS_FILE = '/etc/hosts'

    def __init__(self, file_name=HOSTS_FILE):
        self.file_name = file_name
        line = HostsLine()
        self.lines = [line]
        lines = open(file_name, 'r').read().splitlines()
        for text_line in lines:
            line.add_line(text_line)
            if line.address != '':
                line = HostsLine()
                self.lines.append(line)
        if line.address == '' and len(line.comments) == 0:
            self.lines.remove(line)

    def save(self, file_name=''):
        if file_name == '':
            file_name = self.file_name
        else:
            self.file_name = file_name
        with open(file_name, 'w') as f:
            for line in self.lines:
                for comment in line.comments:
                    f.write(comment + '\n')
                if line.address != '':
                    f.write(line.address)
                    if line.name != '':
                        f.write('\t' + line.name)
                        for alias in line.aliases:
                            f.write('\t' + alias)
                    if line.comment != '':
                        f.write('\t' + line.comment)
                    f.write('\n')

    def get_line(self, address):
        if address is not None and address != '':
            for i, line in enumerate(self.lines):
                if line.address == address:
                    return i, line
        return -1, None

    @property
    def host_name(self):
        i, line = self.get_line('127.0.1.1')
        if line is not None:
            return line.name.split('.')[0]
        return ''

    @host_name.setter
    def host_name(self, host_name):

        # get the new host and domain names
        if not HostsFile.is_valid_hostname(host_name):
            return
        parts = host_name.split('.')
        domain_name = '.'.join(parts[1:])
        host_name = parts[0]

        # get the host name line
        i, line = self.get_line('127.0.1.1')

        # create a new host name line if there isn't one
        if line is None:
            line = HostsLine()
            line.address = '127.0.1.1'
            if domain_name != '':
                line.name = host_name + '.' + domain_name
                line.aliases.insert(0, host_name)
            else:
                line.name = host_name
            j, line2 = self.get_line('127.0.0.1')
            self.lines.insert(j + 1, line)

        # otherwise update the existing host name line
        else:
            # get the current host and domain names
            parts = line.name.split('.')
            curr_host_name = parts[0]
            curr_domain_name = '.'.join(parts[1:])

            # update the aliases
            alias_index = -1
            for j, alias in enumerate(line.aliases):
                if alias == curr_host_name:
                    alias_index = j
                line.aliases[j] = alias.replace(curr_host_name, host_name)

            # update the name and alias
            if domain_name == '' and curr_domain_name != '':
                domain_name = curr_domain_name
            if domain_name != '':
                line.name = host_name + '.' + domain_name
                if len(line.aliases) == 0:
                    line.aliases.insert(0, host_name)
            else:
                line.name = host_name
                if alias_index != -1:
                    del line.aliases[alias_index]

    @property
    def domain_name(self):
        i, line = self.get_line('127.0.1.1')
        if line is not None:
            return '.'.join(line.name.split('.')[1:])
        return ''

    @domain_name.setter
    def domain_name(self, domain_name):
        if not HostsFile.is_valid_hostname(domain_name):
            return
        parts = domain_name.split('.')
        host_name = self.host_name
        if parts[0] == host_name:
            domain_name = '.'.join(parts[1:])
        self.host_name = host_name + '.' + domain_name

    @staticmethod
    def is_valid_hostname(host_name):
        if host_name is None or len(host_name) > 255:
            return False
        if host_name[-1] == '.':
            host_name = host_name[:-1]
        allowed = re.compile('(?!-)[A-Z\d-]{1,63}(?<!-)$', re.IGNORECASE)
        return all(allowed.match(x) for x in host_name.split('.'))


# =============================================================================
# HostsLine
# =============================================================================
class HostsLine:

    def __init__(self):
        self.comments = []
        self.address = ''
        self.name = ''
        self.aliases = []
        self.comment = ''

    def add_line(self, full_line):
        comment = ''
        line = full_line
        i = line.find('#')
        if i >= 0:
            comment = line[i:]
            line = line[:i]
        line = line.strip()
        if len(line) > 0:
            parts = line.split()
            self.address = parts[0]
            if len(parts) > 1:
                self.name = parts[1]
            if len(parts) > 2:
                self.aliases = parts[2:]
            if len(comment) > 0:
                self.comment = comment
        else:
            self.comments.append(full_line)

    def __repr__(self):
        return '({0} {1} {2})'.format(self.address, self.name, ' '.join(self.aliases))
