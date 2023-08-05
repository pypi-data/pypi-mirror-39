#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re


RED = ['\033[0;31;m', '\033[0m']
GREEN = ['\033[0;32;m', '\033[0m']
BLUE = ['\033[0;34;m', '\033[0m']



class ColorPrinter(object):

    
    _instance = None
    
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    @classmethod
    def warning_print(cls, msg, sep=' ', end='\n'):
        cls.color_print(msg, color=RED, sep=sep, end=end)

    @classmethod
    def common_print(cls, msg, sep=' ', end='\n'):
        cls.color_print(msg, color=GREEN, sep=sep, end=end)

    @classmethod
    def color_print(cls, msg, color=BLUE, sep=' ', end='\n'):
        print(cls.format_msg_with_color(str(msg), color), sep=sep, end=end)
    
    @classmethod
    def format_msg_with_color(cls, msg, color=BLUE):
        if sys.platform == 'win32':
            return msg
        return ''.join([color[0], msg, color[1]])
                


class FilePaster(object):
    
    
    _instance = None
    file_pattern = re.compile(r'\[.*\.(?:txt|py|c|cpp|h|hpp|cxx|hxx|java|tmp|jh)\]')
    # file_pattern = re.compile(r'\[.*\.txt\]')

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance
        

    def __init__(self, fname):
        self.fname_ = fname
        self.lineno_file_ = {}
        self.fout_ = ''
    
    def paste(self):
        if not self._pickfnames():
            return False

        if not len(self.lineno_file_):
            # ColorPrinter.warning_print("Warning: " + self.fname_ + "doesn't contain labels")
            self.fout_ = "Error: " + self.fname_ + "doesn't contain labels!"
            return False
        try:
            with open(self.fname_, 'r') as fin:
                with open(self.fname_ + '.jh', 'w') as fout:
                    for (lineno, linestr) in enumerate(fin):
                        if lineno not in self.lineno_file_:
                            fout.write(linestr)
                        else:
                            fname = self.lineno_file_[lineno]
                            if os.path.exists(fname):
                                with open(fname, 'r') as fid:
                                    fout.write(fid.read())
                            else:
                                # ColorPrinter.warning_print("Error: " + fname + " doesn't exist!")
                                self.fout_ = "Error: " + fname + " doesn't exist!"
                                return False
        except Exception as e:
            # ColorPrinter.warning_print("Unexpected Error Raised When Pasting!")
            self.fout_ = "Error: Unexpected Error Raised When Pasting!"
            return False

        return True


    def _pickfname(self, label):
        return label.strip('[]') 

    def _pickfnames(self):
        try:
            with open(self.fname_, 'r') as fid:
                for (lineno, foutline) in enumerate(fid):
                    matched = self.file_pattern.findall(foutline)
                    if matched:
                        for i in range(len(matched)):
                            self.lineno_file_[lineno] = self._pickfname(matched[i])
        except Exception as e:
            # ColorPrinter.warning_print("Unexcepted Error Raised When Reading File " + self.fname_)
            self.fout_ = "Error: Unexcepted Error Raised When Reading File " + self.fname_ + "!"
            return False

        return True

    def __str__(self):
        return str(self.file_lineno_)


def main():
    # fname = input(ColorPrinter.format_msg_with_color("Please enter a filename which you want to be pasted: ", GREEN))
    fname = ''
    try:
        fname = sys.argv[1]
    except IndexError as e:
        ColorPrinter.warning_print('A File Name Is Required')
        return
    filepaster = FilePaster(fname)
    if not filepaster.paste():
        ColorPrinter.warning_print(filepaster.fout_)
    else:
        ColorPrinter.common_print("Successfully!")


if __name__ == '__main__':
    main()
