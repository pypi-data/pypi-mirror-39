import re


# =============================================================================
# IniFile
# =============================================================================
class IniFile:

    SECONDS_INFINITY = -1
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = SECONDS_PER_MINUTE * 60
    SECONDS_PER_DAY = SECONDS_PER_HOUR * 24
    SECONDS_PER_WEEK = SECONDS_PER_DAY * 7
    SECONDS_PER_MONTH = SECONDS_PER_DAY * 30.44
    SECONDS_PER_YEAR = SECONDS_PER_DAY * 365.25
    SECONDS_PER_MS = 0.001
    SECONDS_PER_US = 0.000001
    SECONDS_PER_NS = 0.000000001

    KILOBYTE = 1024
    MEGABYTE = KILOBYTE * 1024
    GIGABYTE = MEGABYTE * 1024
    TERABYTE = GIGABYTE * 1024
    PETABYTE = TERABYTE * 1024
    EXABYTE = PETABYTE * 1024
    THOUSAND = 1000
    MILLION = THOUSAND * 1000
    BILLION = MILLION * 1000

    # self.file_name = str
    # self.properties = {name:IniProperty}
    # self.lines = [IniLine]
    # self.sections = [(IniLine, [IniLine])]

    # =========================================================================
    # __init__
    # =========================================================================
    def __init__(self, file_name=''):
        self.properties = {}
        self.file_name = file_name
        self.lines = []
        self.sections = []
        options = None
        if file_name:
            line = IniLine()
            self.lines.append(line)
            lines = open(file_name, 'r').read().splitlines()
            continue_line = ''
            for full_line in lines:
                full_line = continue_line + full_line.strip()
                if full_line != '' and full_line[-1] == '\\':
                    continue_line = full_line[:-1]
                    continue
                else:
                    continue_line = ''
                line, options = self._process_line(line, full_line, options)
            if continue_line != '':
                line, options = self._process_line(line, continue_line, options)
            if line.name == '' and len(line.comments) == 0:
                self.lines.remove(line)

    # =========================================================================
    # _process_line
    # =========================================================================
    def _process_line(self, line, full_line, options):
        line.add_line(full_line)
        if line.name != '':
            if line.is_section:
                options = []
                self.sections.append((line, options))
            elif options is not None:
                i, existing = IniFile.find_option(options, line.name)
                if existing is not None:
                    if isinstance(existing, list):
                        existing.append(line)
                    else:
                        options[i] = [existing, line]
                else:
                    options.append(line)
            line = IniLine()
            self.lines.append(line)
        return line, options

    # =========================================================================
    # __getattr__
    # =========================================================================
    def __getattr__(self, name):
        if name != 'properties':
            if name in self.properties:
                prop = self.properties[name]
                if prop.type == 'i':
                    return self.get_int(prop.section_name, prop.option_name)
                if prop.type == 'b':
                    return self.get_bool(prop.section_name, prop.option_name)
                if prop.type == 'l':
                    return self.get_list(prop.section_name, prop.option_name, prop.separator)
                if prop.type == 'ns':
                    return self.get_sec(prop.section_name, prop.option_name, prop.max_per_line)
                if prop.type == 'nb':
                    return self.get_nb(prop.section_name, prop.option_name)
                if prop.type == 'bps':
                    return self.get_bps(prop.section_name, prop.option_name)
                if prop.type == 'fm':
                    return self.get_fm(prop.section_name, prop.option_name)
                return self.get_str(prop.section_name, prop.option_name)

    # =========================================================================
    # __setattr__
    # =========================================================================
    def __setattr__(self, name, value):
        if name != 'properties':
            if name in self.properties:
                prop = self.properties[name]
                if prop.type == 'i':
                    self.set_int(prop.section_name, prop.option_name, value)
                elif prop.type == 'b':
                    self.set_bool(prop.section_name, prop.option_name, value)
                elif prop.type == 'l':
                    self.set_list(prop.section_name, prop.option_name, value,
                                  prop.separator, prop.max_per_line)
                elif prop.type == 'ns':
                    self.set_sec(prop.section_name, prop.option_name, value)
                elif prop.type == 'nb':
                    self.set_nb(prop.section_name, prop.option_name, value)
                elif prop.type == 'bps':
                    self.set_bps(prop.section_name, prop.option_name, value)
                elif prop.type == 'fm':
                    self.set_fm(prop.section_name, prop.option_name, value)
                else:
                    self.set_str(prop.section_name, prop.option_name, value)
                return
        super(IniFile, self).__setattr__(name, value)

    # =========================================================================
    # save
    # =========================================================================
    def save(self, file_name=''):
        if file_name == '':
            file_name = self.file_name
        else:
            self.file_name = file_name
        with open(file_name, 'w') as f:
            first = True
            for line in self.lines:
                for comment in line.comments:
                    f.write(comment + '\n')
                if not first and line.is_section and (len(line.comments) == 0 or line.comments[0].strip() != ''):
                    f.write('\n')
                if len(line.name) > 0:
                    f.write('{0!r}\n'.format(line))
                first = False

    # =========================================================================
    # print
    # =========================================================================
    def print(self):
        for line in self.lines:
            for comment in line.comments:
                print(comment)
            if len(line.name) > 0:
                print('{0!r}'.format(line))

    # =========================================================================
    # print_properties
    # =========================================================================
    def print_properties(self, section_name=''):
        if section_name != '':
            parts = section_name.lower().split('_')
            section_name = ''.join(part.title() for part in parts)
        for name, property in self.properties.items():
            if section_name == '' or property.section_name == section_name:
                s = "* {0}".format(name, property.type)
                t = ''
                if property.type == 'i':
                    t = 'int'
                elif property.type == 'b':
                    t = 'bool'
                elif property.type == 'l':
                    t = 'list'
                elif property.type == 'ns':
                    t = 'seconds'
                elif property.type == 'nb':
                    t = 'bytes'
                elif property.type == 'bps':
                    t = 'bits'
                elif property.type == 'fm':
                    t = 'mode'
                if t:
                    s += ' - ' + t
                if (property.type == 'l' and (property.separator != ' ' or property.max_per_line != 0))\
                    or (property.type == 'nb' and property.max_per_line != 0):
                    s += " '{0}' {1}".format(property.separator, property.max_per_line)
                print(s)

    # =========================================================================
    # add_properties
    # =========================================================================
    def add_properties(self, section_name, properties):
        parts = section_name.split('_')
        real_section_name = ''.join(part.title() for part in parts)
        for prop in properties:
            property_name = prop[0]
            parts = property_name.split('_')
            option_name = ''.join(part.title() for part in parts)
            property_name = section_name + '_' + property_name
            option_type = prop[1] if len(prop) > 1 else 's'
            ini_prop = IniProperty(real_section_name, option_name, option_type)
            if len(prop) > 2:
                ini_prop.separator = prop[2]
            if len(prop) > 3:
                ini_prop.max_per_line = prop[3]
            self.properties[property_name] = ini_prop

    # =========================================================================
    # get_section
    # =========================================================================
    def get_section(self, section_name):
        if section_name[0] == '[' and section_name[-1] == ']':
            section_name = section_name[1:-1]
        section_name = section_name.lower()
        for line, options in self.sections:
            if line.name.lower() == section_name:
                return line, options
        return None, None

    # =========================================================================
    # add_section
    # =========================================================================
    def add_section(self, section_name):
        section, options = self.get_section(section_name)
        if section is None:
            if section_name[0] != '[':
                section_name = '[' + section_name + ']'
            section = IniLine()
            section.add_line(section_name)
            section.is_section = True
            options = []
            self.lines.append(section)
            self.sections.append((section, options))
        return section, options

    # =========================================================================
    # remove_section
    # =========================================================================
    def remove_section(self, section_name):
        section, options = self.get_section(section_name)
        if options:
            for option in options:
                self.lines.remove(option)
            options.clear()
        if section is not None:
            self.lines.remove(section)
            self.sections.remove((section, options))

    # =========================================================================
    # get_option
    # =========================================================================
    def get_option(self, section_name, option_name):
        section_line, section_options = self.get_section(section_name)
        if section_line is not None:
            options = []
            option_name = option_name.lower()
            for option_line in section_options:
                if isinstance(option_line, list):
                    if option_line[0].name.lower() == option_name:
                        options.extend(option_line)
                elif option_line.name.lower() == option_name:
                    options.append(option_line)
            return section_line, options
        return None, None

    # =========================================================================
    # set_option
    # =========================================================================
    def set_option(self, section_name, option_name, values):
        section, options = self.get_option(section_name, option_name)
        if section is None:
            options = []
        section, section_options = self.add_section(section_name)
        if values is None:
            values = []
        elif not isinstance(values, list) and not isinstance(values, tuple):
            values = [values]
        for i, value in enumerate(values):
            if i < len(options):
                options[i].value = str(values[i])
            else:
                if len(section_options) > 0:
                    last = section_options[-1]
                    if isinstance(last, list):
                        index = self.lines.index(last[-1])
                    else:
                        index = self.lines.index(last)
                else:
                    index = self.lines.index(section)
                option = IniLine()
                option.add_line(option_name + '=' + str(values[i]))
                section_options.append(option)
                self.lines.insert(index + 1, option)
        n = len(options) - len(values)
        if n > 0:
            del_options = options[-n:]
            for option in del_options:
                self.lines.remove(option)
                section_options.remove(option)

    # =========================================================================
    # remove_option
    # =========================================================================
    def remove_option(self, section_name, option_name):
        section, options = self.get_option(section_name, option_name)
        if options:
            section, section_options = self.get_section(section_name)
            for option in options:
                self.lines.remove(option)
                section_options.remove(option)

    # =========================================================================
    # get_str
    # =========================================================================
    def get_str(self, section_name, option_name):
        section, options = self.get_option(section_name, option_name)
        if options is not None and len(options) > 0:
            return options[0].value
        return None

    # =========================================================================
    # set_str
    # =========================================================================
    def set_str(self, section_name, option_name, value):
        if value is None:
            self.remove_option(section_name, option_name)
        else:
            self.set_option(section_name, option_name, [value])

    # =========================================================================
    # get_bool
    # =========================================================================
    def get_bool(self, section_name, option_name):
        s = self.get_str(section_name, option_name)
        if s is not None:
            s = s.lower()
            return s == 'yes' or s == 'true' or s == 'on' or s == '1'
        return None

    # =========================================================================
    # set_bool
    # =========================================================================
    def set_bool(self, section_name, option_name, value):
        if value is None:
            self.remove_option(section_name, option_name)
        else:
            self.set_str(section_name, option_name, 'yes' if value else 'no')

    # =========================================================================
    # get_int
    # =========================================================================
    def get_int(self, section_name, option_name):
        s = self.get_str(section_name, option_name)
        if s is not None:
            try:
                return int(s)
            except (ValueError, TypeError):
                raise
        return None

    # =========================================================================
    # set_int
    # =========================================================================
    def set_int(self, section_name, option_name, value):
        if value is None:
            self.remove_option(section_name, option_name)
        else:
            self.set_str(section_name, option_name, str(value))

    # =========================================================================
    # get_list
    # =========================================================================
    def get_list(self, section_name, option_name, separator=' '):
        section, options = self.get_option(section_name, option_name)
        if not options:
            return None
        values = []
        for option in options:
            if separator:
                parts = option.value.split(separator)
                values.extend(parts)
            else:
                values.append(option.value)
        return values

    # =========================================================================
    # set_list
    # =========================================================================
    def set_list(self, section_name, option_name, value, separator=' ', max_per_line=0):
        if value is None:
            self.remove_option(section_name, option_name)
        else:
            values = []
            if isinstance(value, list):
                for v in value:
                    if separator:
                        parts = str(v).split(separator)
                        values.extend(parts)
                    else:
                        values.append(v)
            elif separator:
                parts = str(value).split(separator)
                values.extend(parts)
            else:
                values.append(value)
            line_values = []
            if max_per_line <= 0:
                max_per_line = len(values)
            i = 0
            while i < len(values):
                new_value = separator.join(values[i:i + max_per_line])
                line_values.append(new_value)
                i += max_per_line
            self.set_option(section_name, option_name, line_values)

    # ==============================================================================
    # get_sec
    # ==============================================================================
    def get_sec(self, section_name, option_name, default_time_unit=1):
        s = self.get_str(section_name, option_name)
        return IniFile.str_to_sec(s, default_time_unit)

    # ==============================================================================
    # set_sec
    # ==============================================================================
    def set_sec(self, section_name, option_name, sec):
        if sec is None:
            self.remove_option(section_name, option_name)
        else:
            s = IniFile.sec_to_str(sec)
            self.set_str(section_name, option_name, s)

    # ==============================================================================
    # get_nb
    # ==============================================================================
    def get_nb(self, section_name, option_name):
        s = self.get_str(section_name, option_name)
        return IniFile.str_to_nb(s)

    # ==============================================================================
    # set_nb
    # ==============================================================================
    def set_nb(self, section_name, option_name, nb):
        if nb is None:
            self.remove_option(section_name, option_name)
        else:
            s = IniFile.nb_to_str(nb)
            self.set_str(section_name, option_name, s)

    # ==============================================================================
    # get_bps
    # ==============================================================================
    def get_bps(self, section_name, option_name):
        s = self.get_str(section_name, option_name)
        return IniFile.str_to_bps(s)

    # ==============================================================================
    # set_bps
    # ==============================================================================
    def set_bps(self, section_name, option_name, bps):
        if bps is None:
            self.remove_option(section_name, option_name)
        else:
            s = IniFile.bps_to_str(bps)
            self.set_str(section_name, option_name, s)

    # ==============================================================================
    # get_fm
    # ==============================================================================
    def get_fm(self, section_name, option_name):
        s = self.get_str(section_name, option_name)
        return IniFile.str_to_fm(s)

    # ==============================================================================
    # set_fm
    # ==============================================================================
    def set_fm(self, section_name, option_name, fm):
        if fm is None:
            self.remove_option(section_name, option_name)
        else:
            s = IniFile.fm_to_str(fm)
            self.set_str(section_name, option_name, s)

    # =========================================================================
    # find_option
    # =========================================================================
    @staticmethod
    def find_option(options, name):
        name = name.lower()
        for i, line in enumerate(options):
            if line.name.lower() == name:
                return i, line
        return -1, None

    # ==============================================================================
    # str_to_sec
    # ==============================================================================
    @staticmethod
    def str_to_sec(time_span, default_time_unit=1):
        if time_span is None:
            return None
        if time_span == 'infinity':
            return IniFile.SECONDS_INFINITY
        if default_time_unit <= 0:
            default_time_unit = 1
        seconds = 0
        part_seconds = 0
        parts = re.findall('\d+|\D+', time_span)
        for i, part in enumerate(parts):
            part = part.strip()
            if part == '':
                continue
            if part.isdigit():
                seconds += part_seconds * default_time_unit
                part_seconds = int(part)
            else:
                time_unit = default_time_unit
                if part == 'years' or part == 'year' or part == 'y':
                    time_unit = IniFile.SECONDS_PER_YEAR
                elif part == 'months' or part == 'month' or part == 'M':
                    time_unit = IniFile.SECONDS_PER_MONTH
                elif part == 'weeks' or part == 'week' or part == 'w':
                    time_unit = IniFile.SECONDS_PER_WEEK
                elif part == 'days' or part == 'day' or part == 'd':
                    time_unit = IniFile.SECONDS_PER_DAY
                elif part == 'hours' or part == 'hour' or part == 'hr' or part == 'h':
                    time_unit = IniFile.SECONDS_PER_HOUR
                elif part == 'minutes' or part == 'minute' or part == 'min' or part == 'm':
                    time_unit = IniFile.SECONDS_PER_MINUTE
                elif part == 'seconds' or part == 'second' or part == 'sec' or part == 's':
                    time_unit = 1
                elif part == 'msec' or part == 'ms':
                    time_unit = IniFile.SECONDS_PER_MS
                elif part == 'usec' or part == 'us':
                    time_unit = IniFile.SECONDS_PER_US
                elif part == 'nsec' or part == 'ns':
                    time_unit = IniFile.SECONDS_PER_NS
                seconds += part_seconds * time_unit
                part_seconds = 0
        return seconds + part_seconds * default_time_unit

    # ==============================================================================
    # sec_to_str
    # ==============================================================================
    @staticmethod
    def sec_to_str(seconds):
        if seconds is None:
            return None
        if seconds < 0:
            return 'infinity'
        s = ''
        n = seconds // IniFile.SECONDS_PER_YEAR
        if n > 0:
            s += ' ' + str(int(n)) + 'y'
            seconds -= n * IniFile.SECONDS_PER_YEAR
        n = seconds // IniFile.SECONDS_PER_MONTH
        if n > 0:
            s += ' ' + str(int(n)) + 'M'
            seconds -= n * IniFile.SECONDS_PER_MONTH
        n = seconds // IniFile.SECONDS_PER_WEEK
        if n > 0:
            s += ' ' + str(int(n)) + 'w'
            seconds -= n * IniFile.SECONDS_PER_WEEK
        n = seconds // IniFile.SECONDS_PER_DAY
        if n > 0:
            s += ' ' + str(int(n)) + 'd'
            seconds -= n * IniFile.SECONDS_PER_DAY
        n = seconds // IniFile.SECONDS_PER_HOUR
        if n > 0:
            s += ' ' + str(int(n)) + 'h'
            seconds -= n * IniFile.SECONDS_PER_HOUR
        n = seconds // IniFile.SECONDS_PER_MINUTE
        if n > 0:
            s += ' ' + str(int(n)) + 'm'
            seconds -= n * IniFile.SECONDS_PER_MINUTE
        n = int(seconds)
        if n > 0:
            s += ' ' + str(n) + 's'
            seconds -= n
        n = int(seconds / IniFile.SECONDS_PER_MS)
        if n > 0:
            s += ' ' + str(int(n)) + 'ms'
            seconds -= int(n) * IniFile.SECONDS_PER_MS
        n = int(seconds / IniFile.SECONDS_PER_US)
        if n > 0:
            s += ' ' + str(int(n)) + 'us'
            seconds -= int(n) * IniFile.SECONDS_PER_US
        n = int(seconds / IniFile.SECONDS_PER_NS)
        if n > 0:
            s += ' ' + str(int(n)) + 'ns'
            seconds -= int(n) * IniFile.SECONDS_PER_NS
        if s == '':
            s = '0s'
        return s.lstrip()

    # ==============================================================================
    # str_to_nb
    # ==============================================================================
    @staticmethod
    def str_to_nb(s):
        if not isinstance(s, str):
            return None
        mult = 1
        suffix = s[-1].upper()
        if suffix == 'K':
            mult = IniFile.KILOBYTE
            s = s[:-1]
        elif suffix == 'M':
            mult = IniFile.MEGABYTE
            s = s[:-1]
        elif suffix == 'G':
            mult = IniFile.GIGABYTE
            s = s[:-1]
        elif suffix == 'T':
            mult = IniFile.TERABYTE
            s = s[:-1]
        elif suffix == 'P':
            mult = IniFile.PETABYTE
            s = s[:-1]
        elif suffix == 'E':
            mult = IniFile.EXABYTE
            s = s[:-1]
        return int(s) * mult

    # ==============================================================================
    # nb_to_str
    # ==============================================================================
    @staticmethod
    def nb_to_str(nb):
        if not isinstance(nb, int):
            return None
        n = nb % IniFile.EXABYTE
        if n == 0:
            return str(nb // IniFile.EXABYTE) + 'E'
        n = nb % IniFile.PETABYTE
        if n == 0:
            return str(nb // IniFile.PETABYTE) + 'P'
        n = nb % IniFile.TERABYTE
        if n == 0:
            return str(nb // IniFile.TERABYTE) + 'T'
        n = nb % IniFile.GIGABYTE
        if n == 0:
            return str(nb // IniFile.GIGABYTE) + 'G'
        n = nb % IniFile.MEGABYTE
        if n == 0:
            return str(nb // IniFile.MEGABYTE) + 'M'
        n = nb % IniFile.KILOBYTE
        if n == 0:
            return str(nb // IniFile.KILOBYTE) + 'K'
        return str(nb)

    # ==============================================================================
    # str_to_bps
    # ==============================================================================
    @staticmethod
    def str_to_bps(s):
        if not isinstance(s, str):
            return None
        mult = 1
        suffix = s[-1].upper()
        if suffix == 'K':
            mult = IniFile.THOUSAND
            s = s[:-1]
        elif suffix == 'M':
            mult = IniFile.MILLION
            s = s[:-1]
        elif suffix == 'G':
            mult = IniFile.BILLION
            s = s[:-1]
        return int(s) * mult

    # ==============================================================================
    # bps_to_str
    # ==============================================================================
    @staticmethod
    def bps_to_str(bps):
        if not isinstance(bps, int):
            return None
        n = bps % IniFile.BILLION
        if n == 0:
            return str(bps // IniFile.BILLION) + 'G'
        n = bps % IniFile.MILLION
        if n == 0:
            return str(bps // IniFile.MILLION) + 'M'
        n = bps % IniFile.THOUSAND
        if n == 0:
            return str(bps // IniFile.THOUSAND) + 'K'
        return str(bps)


    # ==============================================================================
    # str_to_fm
    # ==============================================================================
    @staticmethod
    def str_to_fm(s):
        if not isinstance(s, str):
            return None
        return int(s, 8)

    # ==============================================================================
    # fm_to_str
    # ==============================================================================
    @staticmethod
    def fm_to_str(fm):
        if not isinstance(fm, int):
            return None
        return '{0:04o}'.format(fm)


# =============================================================================
# IniLine
# =============================================================================
class IniLine:

    def __init__(self):
        self.comments = []
        self.name = ''
        self.value = ''
        self.is_section = False

    def add_line(self, full_line):
        line = full_line.strip()
        if line != '' and line[0] != '#' and line[0] != ';':
            if line[0] == '[' and line[-1] == ']':
                self.name = line[1:-1].strip()
                self.is_section = True
            else:
                i = line.find('=')
                if i != -1:
                    self.name = line[:i].rstrip()
                    self.value = line[i+1:].lstrip()
                else:
                    self.name = line
        else:
            self.comments.append(full_line)

    def __repr__(self):
        if self.is_section:
            s = '[' + self.name + ']'
        else:
            s = self.name + '=' + self.value
        return s


# =============================================================================
# IniProperty
# =============================================================================
class IniProperty:

    def __init__(self, section_name, option_name, option_type):
        self.section_name = section_name
        self.option_name = option_name
        self.type = option_type
        self.separator = ' '
        self.max_per_line = 0
