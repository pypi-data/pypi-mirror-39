

from typing import Optional, Dict, Any, Union, List, Callable
from typing import NamedTuple
import json

# a list of functions that may be called
Interface = List[ Callable[[Any], Any] ]
Params = Optional[ Union[Dict[str, Any], List[Any] ] ]

# representa o objeto de chamada remota
class FuncCall(NamedTuple):
    '''
    params = may be xargs=dict or args=list format
    '''
    funcname: str
    params: Params


def _json_to_dict(_json):
    return json.loads(_json)

def _dict_to_json(d: Dict[str, Any]):
    return json.dumps(d)

def _call_no_args(_func:str) -> Any:
    return _func()

# used when params are a list=*args
def _call_args(_func, args: List[Any]) -> Any:
    return _func(*args)

# used when params are a dict=*xargs
def _call_xargs(_func, xargs: Dict[str, Any]) -> Any:
    return _func(**xargs)

# interface is a list with remote callable functions
# NOTE: This function DO NOT cast the function result
def run(_json, api: Interface) -> Any:
    # load json
    d = _json_to_dict(_json)
    fname = d['funcname']
    _params = d['params']

    # select choosen functoin from function interface
    _func = None
    for func in api:
        if func.__name__ == fname:
            _func = func
            break
    if _func is None:
        raise ValueError("Tentativa de chamada de funcao remota falhou. Funcao não localizada na api")


    # call function
    if _params == [] or _params is None:
        res = _call_no_args(_func)
    elif isinstance(_params, list):
        res = _call_args(_func, _params)
    elif isinstance(_params, dict):
        res = _call_xargs(_func, _params)
    else:
        raise ValueError(f"Tentativa de chamada de funcao remota {funcname} falhou. Parametro(s) da funcao precisa ser ou vazio, ou uma lista, ou um dicionario")
    # create response
    return res # as dict


def cast_result(data: Any) -> Dict[str, Any]:
    res = { 'result' : data }
    return res


# helper for log/debug
def create_remote_json_call(funcname:str, params: Params) -> str:
    return FuncCall(funcname, params)._asdict()


# -------------- TEST

def me():
    print("me running...")
    return ['com1', 'com2', None]

def metoo(a, b):
    print("metoo running...")
    return {'a=': a, 'b=' : b, 'c=': ['com1', 'com2'], 'nada': None}


if __name__ == '__main__':

    api: Interface = [me, metoo]

    # function without params
    _json = create_remote_json_call('me', None)
    print(_json)
    print(_json_to_dict(_json))
    res = run(_json, api)
    res = cast_result(res)
    print(_dict_to_json(res))


    # function with list arguments
    _json = create_remote_json_call('metoo', [10,20])
    print(_json)
    print(_json_to_dict(_json))
    res = run(_json, api)
    res = cast_result(res)
    print(_dict_to_json(res))


    # function with xargs arguments
    _json = create_remote_json_call('metoo', {'a':66, 'b': 77})
    print(_json)
    print(_json_to_dict(_json))
    res = run(_json, api)
    res = cast_result(res)
    print(_dict_to_json(res))