#!/usr/bin/env python3
import re
import argparse


class ConfigItem:
    line_regex = re.compile(r"^([#\s]*)([^#=\s]*)\s*=*\s*([^#=]*)\s*$")
    comment_char = '#'
    def __init__(self, line):
        self.key, self.value, self.is_commentouted = self.parese_line(line)

    @classmethod
    def parese_line(cls, line):
        comment, key, value = cls.line_regex.match(line).groups()
        is_commentouted = False
        if cls.comment_char in comment:
            is_commentouted = True
        return key, value, is_commentouted


class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        lines = self._read(file_path)
        self.items = self._convert_lines2items(lines)

    def __str__(self):
        lines = []
        for item in self.items.values():
            if item.is_commentouted:
                lines.append(f'#{item.key} = {item.value}')
            else:
                lines.append(f'{item.key} = {item.value}')
        return '\n'.join(lines)
    
    @staticmethod
    def _read(file_path):
        with open(file_path) as f:
            lines = map(str.strip, f.readlines())
            lines = list(filter(lambda s: len(s) > 0, lines))
        return lines

    @staticmethod
    def _convert_lines2items(lines):
        items = {}
        for line in lines:
            item = ConfigItem(line)
            if item.key == "":
                continue
            items[item.key] = item
        return items
    
    @property
    def keys(self):
        return [item.key for item in self.items.values()]

    @property
    def values(self):
        return [item.value for item in self.items.values()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("original", help="original config file")
    parser.add_argument("update", help="update config file")
    args = parser.parse_args()
    original_file = args.original 
    update_file = args.update
    original_conf = Config(original_file)
    update_conf = Config(update_file)
    print(update_conf)
