import os

_current_path = os.path.dirname(os.path.abspath(__file__))


_tx_file_dict = {'python_tx': 'python.tx',
                 'json_tx': 'json.tx',
                 'pipeline_tx': 'json.tx'}


def get_parser_dict(tx_dict):
    _parser_dict = dict()
    for k, file_name in tx_dict.items():
        tx_file = os.path.join(_current_path, 'tx', file_name)
        with open(tx_file, encoding='utf8') as tx_contex:
            tx_string = tx_contex.read()
            _parser_dict.update({k: tx_string})
    return _parser_dict


parser_dict = get_parser_dict(_tx_file_dict)

