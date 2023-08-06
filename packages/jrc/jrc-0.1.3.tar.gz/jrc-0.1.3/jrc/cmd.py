from importlib import import_module
from .compiler import Compiler
from .parser import parser_dict
import os
import click
import configparser
from termcolor import cprint
import sys
sys.path.append('.')


@click.group()
def main():
    """jr compiler 命令行工具"""

    pass


@main.command()
# 应用名, 根据应用名编译
@click.argument('app_name', required=False, default='.')
# 应用描述文件, 应用配置信息
@click.option('--ini', '-i', default=False)
# 生成frame
@click.option('--create_frame', default=False, help='create jr_frame')
def compile(app_name, ini, create_frame):
    """编译"""
    cprint('开始编译...', 'blue')
    if not os.path.exists(app_name):
        cprint('编译失败', 'red')
        cprint('应用：' + app_name + ' 不存在', 'red')
        sys.exit(1)
    # 进入目录
    os.chdir(app_name)
    appinfo_dict = load_appinfo(ini)
    do_compile(appinfo_dict, create_frame)
    cprint('编译完成', 'green')


def do_compile(appinfo, create_frame=False):
    parser = appinfo['parser']

    # 读取规则文件
    if os.path.isfile(parser):
        with open(parser, 'r', encoding='utf-8') as f:
            lang_tx_str = f.read()
    elif parser in parser_dict.keys():
        lang_tx_str = parser_dict.get(parser)
    else:
        cprint('编译失败', 'red')
        cprint('DSL 语法解析文件 ' + parser + ' 不存在', 'red')
        sys.exit(1)
    input_path = appinfo['input_path']
    output_path = appinfo['output_path']
    output_ext = appinfo.get('output_ext')
    output_prefix = appinfo['output_prefix']

    template_path = appinfo['template_path']

    # 动态导入 Extension
    extension = appinfo['extension']
    _LOAD_MODULE = import_module(extension.split(':')[0])
    module_object = getattr(_LOAD_MODULE, extension.split(':')[1])  # 获取Extension
    exec_module_object = module_object(**{"template_path": template_path, 'base_path': output_path})  # 实例化 Extension

    # 创建frame
    if create_frame:
        for file_path, _, files in os.walk(input_path):
            for file in files:
                input_file = os.path.join(file_path, file)
                print('input_file --> ',input_file)
                with open(input_file, 'r', encoding='utf-8') as f:
                    dsl_str = f.read()
                compiler_param = {
                    'dsl_str': dsl_str,
                    'lang_tx_str': lang_tx_str,
                    'template_path': template_path,
                    'extension': exec_module_object,
                    'one2more': True
                }
                compile_obj = Compiler(**compiler_param)
                out_compile_list = compile_obj.parse()
                if isinstance(out_compile_list, list):
                    for item in out_compile_list:
                        output_file = os.path.join(item.get('output_path'), item.get('file_name'))
                        compile_obj.save_code_to(output_file, item.get('code'))
                        cprint('compile --> ' + output_file + ' 成功 ', 'blue')

    else:
        for file_path, _, files in os.walk(input_path):
            for file in files:
                input_file = os.path.join(file_path, file)
                output_file = os.path.join(file_path.replace(input_path, output_path), output_prefix + file)
                if output_ext:
                    output_file = output_file.replace(output_file.split('.')[-1], output_ext)
                with open(input_file, 'r', encoding='utf-8') as f:
                    dsl_str = f.read()
                compiler_param = {
                    "dsl_str": dsl_str,
                    "lang_tx_str": lang_tx_str,
                    "template_path": template_path,
                    "extension": exec_module_object,
                }
                compile_obj = Compiler(**compiler_param)
                compile_obj.compile()
                compile_obj.save_to(output_file)
                cprint(input_file + ' --> ' + output_file + ' 成功 ', 'blue')


def load_appinfo(ini):
    config_info = {}
    if not ini:
        ini = 'appinfo.ini'
    if os.path.isfile(ini):
        config = configparser.ConfigParser()
        try:
            config.read(ini)
            config_info = {x[0]: x[1] for x in config.items(config.sections()[0])}
        except Exception as e:
            cprint('编译失败', 'red')
            raise Exception(e)

    else:
        # 创建默认配置信息
        try:
            config_info['parser_file'] = os.path.join('parser', os.listdir('parser')[0])
            config_info['input_path'] = 'input'
            config_info['output_path'] = 'output'
            config_info['output_prefix'] = 'JR_'
            config_info['template_path'] = 'template'
        except Exception as e:
            cprint('编译失败', 'red')
            raise Exception(e)
    return config_info


if __name__ == '__main__':
    main()

