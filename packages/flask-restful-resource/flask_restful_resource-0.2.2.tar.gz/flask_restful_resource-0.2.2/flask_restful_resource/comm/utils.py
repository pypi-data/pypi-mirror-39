from datetime import datetime

from schema import Schema, SchemaError


def move_space(data: dict):
    if data:
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = str.strip(v)
        return data
    return {}


def validate_schema(schema: Schema, data: dict, remove_blank=False):
    """schema验证,验证成功返回数据，验证失败返回错误信息
    Parameters
    ----------
    schema:Schema: 验证规则
    data: 验证数据
    remove_blank : 是否去除空白字段

    Returns (data,errors)
    -------

    """
    if not isinstance(data, dict):
        return {}, "Not found params"
    d = {}
    if remove_blank:
        for k, v in data.items():
            if v != "":
                d[k] = v
    else:
        d = data
    try:
        validate_data = schema.validate(d)
        return validate_data, []
    except SchemaError as e:
        return {}, str(e.autos)
    else:
        return validate_data, []


def utc_timestamp():
    """返回utc时间戳（秒）"""
    return int(datetime.now().timestamp())
