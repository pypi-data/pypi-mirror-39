# -*- coding: utf-8 -*-
import json
from .common import Node
from .render import Render
import yaml
import os
import shutil


class Extension(object):

    def preprocess(self, source):
        """
        DSL预处理程序，将输入的source做预处理，默认直接返回，不做任何处理
        :param source:
        :return:
        """
        return source

    def semantic_parse(self, grammar_model):
        """语义分析
        """
        return grammar_model

    def code_optimize(self, out_code):
        """代码优化
        """
        return out_code


class ZionExtension(Extension):

    def __init__(self, *args, **kwargs):
        pass

    def semantic_parse(self, grammar_model):
        """语义分析
        """
        return grammar_model.nodes


class JsonExtension(Extension):

    def __init__(self, **kwargs):
        self.source = None
        self.data = None
        self.template_path = kwargs.get('template_path')

    def preprocess(self, source):
        """
        DSL预处理程序，将输入的source做预处理，默认直接返回，不做任何处理
        :param source:
        :return:
        """
        self.data = json.loads(source)
        return source

    def semantic_parse(self, grammar_model):
        """语义分析
        """
        template_name = self.get_template_name(self.data)
        member = self.get_member(self.data)
        g_model = [Node(name=template_name, member=member)]
        return g_model

    def code_optimize(self, out_code):
        """代码优化
        """
        return out_code

    @staticmethod
    def get_template_name(model):
        try:
            template_name = model['template']
        except Exception as _:
            raise Exception('Format Error')

        return template_name

    @staticmethod
    def get_member(model):
        try:
            member = model['member']
        except Exception as _:
            raise Exception('Format Error')

        return member


class PipelineExtension(Extension):

    def __init__(self, **kwargs):
        self.source = None
        self.data = None
        self.template_path = kwargs.get('template_path')

    def preprocess(self, source):
        """
        DSL预处理程序，将输入的source做预处理，默认直接返回，不做任何处理
        :param source:
        :return:
        """
        self.data = yaml.load(source)
        source = json.dumps(self.data)
        return source

    def semantic_parse(self, grammar_model):
        """语义分析
        """

        global_member = self.get_global_member(self.data)
        pipeline_member = self.get_pipeline_member(self.data)
        g_model = pipeline_member.copy()
        local_data = self.parse_model(pipeline_member, 'g_model', list())

        while local_data[0][1] != 'pipeline':
            for ae in local_data:
                node = Node(name=ae[1], member=ae[2], global_member=global_member)
                code = self.render_node([node])
                locals()['code'] = code
                m_str = ae[0] + "['" + ae[1] + "'] = code"
                exec(m_str)
                g_model = locals()['g_model']
            local_data = self.parse_model(g_model, 'g_model', list())

        pipeline_code = self.get_pipeline_code(local_data[-1][-1])
        g_model = [Node(name='pipeline', member={'pipeline': pipeline_code}, global_member=global_member)]
        return g_model

    def code_optimize(self, out_code):
        """代码优化
        """
        return out_code

    @staticmethod
    def get_pipeline_code(model):
        pipeline_code = ''
        for k, v in model.items():
            pipeline_code = pipeline_code + '\n' + v
        return pipeline_code

    @staticmethod
    def get_pipeline_member(model):
        pipeline_member = {'pipeline': model.get('pipeline')}
        return pipeline_member

    @staticmethod
    def get_global_member(model):
        global_member = dict()
        for k, v in model.items():
            if isinstance(v, str):
                global_member.update({k: v})
        return global_member

    def render_node(self, nodes):
        render = Render(self.template_path)
        return render.run(nodes)

    def parse_model(self, model, path, result_data=list()):
        if isinstance(model, dict):
            for first_k, first_v in model.items():
                if isinstance(first_v, dict) or isinstance(first_v, list):
                    is_last_node = True

                    if isinstance(first_v, dict):
                        for second_k, second_v in first_v.items():
                            if not isinstance(second_v, str):
                                is_last_node = False
                                break
                    elif isinstance(first_v, list):
                        for ele in first_v:
                            if not (len(ele) == 1 and
                                    isinstance(ele, dict)
                                    and isinstance(ele[list(ele.keys())[0]], str)):
                                is_last_node = False
                                break

                    if is_last_node:
                        result_data.append((path, first_k, first_v))
                    else:
                        next_path = path + "['" + first_k + "']"
                        self.parse_model(first_v, next_path, result_data)

            return result_data
        elif isinstance(model, list):
            for index, model_ele in enumerate(model):
                self.parse_model(model_ele, path + "[" + str(index) + "]", result_data)


class FrameExtension(Extension):

    def __init__(self, **kwargs):
        """
        :param kwargs: 字典，key 为 template_path 和 base_path
        """
        self.source = None
        self.data = None
        self.template_path = kwargs.get('template_path')
        self.output_path = kwargs.get('base_path')
        self.resource_path = os.path.join(kwargs.get('template_path'), 'resource')

    def preprocess(self, source):
        """
        DSL 预处理程序，将输入的 source 做预处理，默认直接返回，不做任何处理
        :param source:
        :return:
        """
        self.data = yaml.load(source)
        source = json.dumps(self.data)
        static_template_member = self.get_member_by_key('static_template', self.data)
        self._copy_tree(self.resource_path, self.output_path, static_template_member)
        return source

    def semantic_parse(self, grammar_model):
        """语义分析
        """
        global_member = self.get_global_member(self.data)

        dynamic_data_result = []
        dynamic_template_member = self.get_member_by_key('dynamic_template', self.data)
        if isinstance(dynamic_template_member, dict):
            for dynamic_k, dynamic_v in dynamic_template_member.items():
                # 解析template模板
                dynamic_data = self.parse_model({dynamic_k: dynamic_v}, self.output_path, list())

                if dynamic_data and len(dynamic_data) > 0:
                    for ae in dynamic_data:
                        node = Node(name=ae[1], member=ae[2], global_member=global_member)
                        # 读取模板,替换节点内容, 返回数据
                        code = self.render_node([node])
                        # 返回每个模板对应的路径, 替换内容, 文件名, 文件类型后缀
                        dynamic_data_result.append({
                            'output_path': ae[0],
                            'code': code,
                            'name': ae[1],
                            'ext': ae[2].get('ext', 'py'),
                            'file_name': ae[1] + '.' + ae[2].get('ext', 'py')
                        })

        return dynamic_data_result

    def code_optimize(self, out_code):
        """代码优化
        """
        return out_code

    @staticmethod
    def get_dynamic_member(model):
        dynamic_member = {'dynamic_template': model.get('dynamic_template')}
        return dynamic_member

    @staticmethod
    def get_member_by_key(key, model):
        return model.get(key)

    @staticmethod
    def get_global_member(model):
        global_member = dict()
        for k, v in model.items():
            if isinstance(v, str) or isinstance(v, int):
                global_member.update({k: v})
        return global_member

    def render_node(self, nodes):
        render = Render(self.template_path)
        return render.run(nodes)

    def parse_model(self, model, path, result_data=list()):
        if isinstance(model, dict):
            for first_k, first_v in model.items():
                if isinstance(first_v, dict) or isinstance(first_v, list):
                    is_last_node = True

                    if isinstance(first_v, dict):
                        for second_k, second_v in first_v.items():
                            if not isinstance(second_v, str) \
                                    and not isinstance(second_v, int):
                                is_last_node = False
                                break
                    elif isinstance(first_v, list):
                        for ele in first_v:
                            if not (len(ele) == 1 and
                                    isinstance(ele, dict)
                                    and isinstance(ele[list(ele.keys())[0]], str)):
                                is_last_node = False
                                break

                    if is_last_node:
                        result_data.append((path, first_k, first_v))
                    else:
                        next_path = path + "/" + first_k + "/"
                        self.parse_model(first_v, next_path, result_data)

            return result_data
        elif isinstance(model, list):
            for index, model_ele in enumerate(model):
                self.parse_model(model_ele, path + "/" + str(index) + "/", result_data)

    @staticmethod
    def _create_null_file(file_path):
        if os.path.isfile(file_path) is False:
            with open(file_path, 'wb') as f:
                f.close()

    @staticmethod
    def _makedirs_if_not_extis(dir_path):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

    def _makedirs_and_files(self, rootdir, tree):
        if not tree:
            return
        for item in tree:
            if isinstance(item, str):
                file_path = os.path.join(rootdir, item)
                self._create_null_file(file_path)
            elif isinstance(item, dict):
                subdir = list(item.keys())[0]
                subdir_path = os.path.join(rootdir, subdir)
                self._makedirs_if_not_extis(subdir_path)
                self._makedirs_and_files(subdir_path, item[subdir])

    @staticmethod
    def _copy_tree(source_dir, dst_dir, member):
        if not member:
            return

        for item in member:
            if isinstance(item, str):
                file_path = os.path.join(source_dir, item)
                dst_path = os.path.join(dst_dir, item)
                shutil.copy(file_path, dst_path)
            elif isinstance(item, dict):
                subdir = list(item.keys())[0]
                file_path = os.path.join(source_dir, subdir)
                dst_path = os.path.join(dst_dir, subdir)
                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)

                shutil.copytree(file_path, dst_path)
