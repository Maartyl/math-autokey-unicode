import sys
import functools
import json
from copy import deepcopy

def template_script(replacement):
    return """
keyboard.send_keys("<ctrl>+<shift>+u%s")
#keyboard.send_keys("<ctrl>+<shift>+u   <ctrl>")
keyboard.send_keys("<ctrl>")
    """ % replacement

t_json = {'filter': {'regex': None, 'isRecursive': False},
          'omitTrigger': False,
          'store': {},
          'abbreviation': {'ignoreCase': False,
                           'wordChars': '[\\w]',
                           'backspace': True,
                           'immediate': False,
                           'abbreviations': [],  # add abbrev to this list
                           'triggerInside': True},
          'type': 'script',
          'prompt': False,
          'modes': [1],
          'usageCount': 0,
          'showInTrayMenu': False,
          'description': '',
          'hotkey': {'modifiers': [], 'hotKey': None}}

def template_json(abbrev):
    z = deepcopy(t_json)
    z["abbreviation"]["abbreviations"] = [abbrev]
    # extra changes to tree
    return json.dumps(z)

encode_file_name_dict = {
    '`': 'backtick_',
    '/': 'slash_',
    '\\': 'backslash_',
    '|': 'pipe_',
    '_': 'underscore_',
    '&': 'and_',
    '+': 'plus_',
    '-': 'minus_',
    ',': 'comma_',
    ';': 'semicolon_',
}

def encode_file_name(abbrev):
    return ''.join(encode_file_name_dict.get(c, c) for c in abbrev)

def file_push(fname, data):
    with open(fname, "w") as f:
        f.write(data)

def template_run(abbrev, replacement):
    # h = "\\U" + hex(ord(replacement))[2:].zfill(8)  # char -> num -> hex to 8 places
    h = '%x' % (ord(replacement))  # char -> num -> hex

    fname = encode_file_name(abbrev)
    fname_json = '.' + fname + '.json'
    fname_script = fname + '.py'

    print(abbrev, h, fname_json, fname_script)

    file_push(fname_json, template_json(abbrev))
    file_push(fname_script, template_script(h))

def char_range(start, end):
    """ a..z == char_range('a', 'z') """
    return map(chr, range(ord(start), ord(end) + 1))

def chars(src):
    if len(src) == 4 and src[1:3] == '..':
        return char_range(src[0], src[3])
    else:
        return src.split()

# convention: rules :: line -> (abbrev, replacement)

def rule_exact(line):
    ls = line.split()
    if len(ls) != 2:
        raise Exception("incorrect line for exact_rule: " + line)
    return ls[1], ls[0]

def rule_combine(fmtr, line):
    ls = line.split()
    if len(ls) != 2:
        raise Exception("incorrect line for combine_rule: " + line)
    return fmtr(ls[1]), ls[0]

def rule_gen_zip(fmtr, names):
    # print(list(names))
    gen = iter(names)
    return lambda line: (fmtr(next(gen)), line.strip())

def formatter(fmt):
    return lambda char: fmt.replace('_', char)

def processor_rule(line):
    lr = line.split(';', 1)
    l = lr[0].strip()
    r = lr[1].strip() if len(lr) == 2 else None

    ls = l.split()
    # print(lr, l, r, ls)
    if r is None:
        if len(ls) == 1:
            if ls[0] == ':exact':
                return rule_exact
            else:
                return functools.partial(rule_combine, formatter(ls[0]))
    else:
        if len(ls) == 1:
            return rule_gen_zip(formatter(ls[0]), chars(r))
    return None

def processor(line):
    rule = processor_rule(line[1:])
    if rule is None: raise Exception("rule not matched: " + line)
    return rule

def proc_err(line):
    raise Exception("no rule before data")

def remove_comment_norm(line):
    """ remove comment (#...) from line  and normalize (strip)"""
    return line[:line.find('#')].strip()

def main_loop(lines):
    p = proc_err
    for line in filter(None, map(remove_comment_norm, lines)):
        if line[0] == '$':
            p = processor(line)
        else:
            template_run(*p(line))

if __name__ == "__main__":
    main_loop(sys.stdin)
