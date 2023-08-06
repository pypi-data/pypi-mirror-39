# -*- coding: utf-8 -*-
from .extension import Extension
from .grammar_parse import GrammarParse
from .render import Render


class Compiler(object):

    def __init__(self, **kwargs):
        """
        :param kwargs: 参数字典，
        dsl_str: 为dsl字符串，
        lang_tx_str: 为规则字符串，
        template_path: 为模版路径，
        extension: 为extension
        对象
        """
        self._dsl_str = kwargs.get('dsl_str')
        self._lang_tx_str = kwargs.get('lang_tx_str')
        self._template_path = kwargs.get('template_path')
        self._extension = kwargs.get('extension', Extension())
        self._grammar_parse = self._get_grammar_parse(kwargs.get('grammar_parse'))
        self._render = self._get_render(kwargs.get('render'))
        self.out_code = ''
        self._one_to_more = kwargs.get('one2more')
        self.parse = self.compile

    def compile(self):
        # DSL 预处理
        self._dsl_str = self._extension.preprocess(self._dsl_str)
        # 语法分析
        grammar_model = self._grammar_parse.parse(self._dsl_str)
        # 语义分析
        grammar_model = self._extension.semantic_parse(grammar_model)
        # 一对多解析
        if self._one_to_more:
            return grammar_model

        # 代码生成
        self.out_code = self._render.run(grammar_model)
        # 代码优化
        self.out_code = self._extension.code_optimize(self.out_code)
        return self.out_code

    def save_to(self, file_name):
        with open(file_name, 'w', encoding='utf8') as f:
            f.write(self.out_code)

    def save(self, file_name):
        self.save_to(file_name)

    def _get_grammar_parse(self, grammar_parse):
        if grammar_parse is None:
            grammar_parse = GrammarParse(self._lang_tx_str)
        return grammar_parse

    def _get_render(self, render):
        if render is None:
            render = Render(self._template_path)
        return render

    def save_code_to(self, file_name, code):
        with open(file_name, 'w', encoding='utf8') as f:
            f.write(code)
