# -*- coding: utf-8 -*-
import os
import copy
import cStringIO
import json as js
from collections import OrderedDict
import uuid
import requests
import jsonschema
import validators


def refactor_validation_line_error(e, json_obj, context_line=9):
    if not json_obj:
        raise Exception('Invalid parameter: %s' % (json_obj,))
    # 为了不影响源数据json_obj，因此使用deepcopy
    copy_obj = copy.deepcopy(json_obj)
    origin_serializer = js.dumps(copy_obj, indent=4)
    # 定义一个serializer_obj中没有出现过的字符标记
    symbol = uuid.uuid4().get_hex()
    while symbol in origin_serializer:
        symbol = uuid.uuid4().get_hex()
    # 用temp_obj来递归找到并修改指定的地方，利用python的浅复制特性，会自动修改到copy_obj上，因此这里不用deepcopy
    temp_obj = copy_obj
    for item in list(e.path)[:-1]:
        temp_obj = temp_obj[item]
    temp_obj[e.path[-1]] = symbol
    # 注意此时copy_obj已被修改
    modified_serializer = js.dumps(copy_obj, indent=4)
    ios = cStringIO.StringIO(modified_serializer)
    for idx, text in enumerate(ios):
        if text.find(symbol) != -1:
            err_line = idx
            break
    else:
        raise Exception('Can\'t find symbol: %s' % (symbol,))

    message = []
    ios = cStringIO.StringIO(origin_serializer)
    for idx, text in enumerate(ios):
        if idx == err_line:
            line_text = '{:6}: >>>'.format(idx + 1)
        else:
            line_text = '{:6}:    '.format(idx + 1)
        if idx > err_line + context_line:
            break
        message.append(line_text + text)
    message = message[max(0, err_line-context_line):]
    e.message = ''.join([e.message, '\nValidate error in line {}:\n'.format(err_line + 1), ''.join(message)])
    raise e


class JsdKeywords(object):
    """
    JsdLibrary is a JSD keyword library that uses to validate JSON
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        pass

    @staticmethod
    def json_should_match_jsd(json, jsd, msg=None):
        """ Validate if the `json` match the `jsd`

        ``json`` can be json file path, URL path or a string containing the JSON data.

        ``jsd`` can be jsd file path, URL path or a string containing the JSON Schemas Definition.

        ``msg`` if set, it will override the default error message when match failed.

        Examples:
        | Json Should Match Jsd | {"ipAddress": "10.16.96.31"} | http://www.domain.com/xxx/yyy/zzz.jsd |
        | Json Should Match Jsd | http://www.domain.com/xxx/yyy/zzz.json | /home/some_user/path_to_file.jsd |
        | Json Should Match Jsd | /home/some_user/path_to_file.json | {"$schema": "http://json-schema.org/draft-04/schema#", "type": "object",...} |
        """
        if validators.url(json):
            headers = {'content-type': 'application/json'}
            _json = requests.get(json, headers=headers).json(object_pairs_hook=OrderedDict)
        elif os.path.exists(json):
            with open(json, 'r') as f:
                _json = js.loads(f.read(), object_pairs_hook=OrderedDict)
        else:
            _json = js.loads(json, object_pairs_hook=OrderedDict)

        if validators.url(jsd):
            headers = {'content-type': 'application/json'}
            _schema = requests.get(jsd, headers=headers).json(object_pairs_hook=OrderedDict)
        elif os.path.exists(jsd):
            with open(jsd, 'r') as f:
                _schema = js.loads(f.read(), object_pairs_hook=OrderedDict)
        else:
            _schema = js.loads(jsd, object_pairs_hook=OrderedDict)

        try:
            jsonschema.validate(_json, _schema)
        except jsonschema.ValidationError as e:
            refactor_validation_line_error(e, _json)
