# -*- coding: utf-8 -*-
from .compiler import *
from .common import *
from .extension import *
from .grammar_parse import *
from .render import *
from .cmd import main
from .parser import parser_dict

# 提供 Parser 入口, 兼容老版本
Parser = Compiler
# 提供 rule_dict 变量, 兼容老版本
rule_dict = parser_dict


__version__ = '0.1.3.1'
