#helpers factories and conversors

from typing import Dict, Tuple, Optional, Any, List
from command import Dictionary, Parameter, Value
from types_ import Type
from type_checking import isTypeCorrect

ErrMsg = Optional[str]

def create_Value_from_int(i:int) -> Value:
    return Value(Type.int,i)

def create_Value_from_str(s:str) -> Value:
    return Value(Type.str,s)

def create_Value_from_bytes(b:bytes) -> Value:
    l: List = []
    for each in b:
        l.append(each)
    return Value(Type.bytes,l)

def create_Value_from_list(li:list) -> Value:
    l: List = []
    for each in li:
        l.append(each)
    return Value(Type.list, l)

def create_Value_from_None() -> Value:
    return Value(Type.none,None)


def create_Value_From_Any(d: Any) -> Tuple[Value, bool, ErrMsg]:
    if isinstance(d, str):
        return create_Value_from_str(d), False, None
    elif isinstance(d, int):
        return create_Value_from_int(d), False, None
    elif isinstance(d, bytes): # NOTE: there is no difference currently between list and bytes. bytes is a list
        return create_Value_from_bytes(d), False, None
    elif isinstance(d, list):
        return create_Value_from_list(d), False, None
    elif d is None:
        return create_Value_from_None(), False, None
    else:
        return None, True, 'type not suported'

def flatdict_to_flatDictionary(dic: Dict) -> Optional[Dictionary]:

    if dic == []:
        return None

    Dic: Dictionary = []
    for key,value in dic.items():
        value_, isErr, errmsg = create_Value_From_Any(value)
        if isErr:
            err = f"Can't create Dictionary from dict specified. Key '{key}' of the dict has a value '{value}' unsupported."
            raise ValueError(err)
        param = Parameter(key, value_)
        Dic.append(param)

    return Dic


def _convertValue_to_pythondata(v: Value):
    if v.type_ == Type().int:
        return v.content
    elif v.type_ == Type().str:
        return v.content
    elif v.type_ == Type().bytes:
        return bytes(v.content) # v.content is a list of integer each one representing a byte
    elif v.type_ == Type().list:
        return v.content # v.content is a list of integer each one representing a byte
    elif v.type_ == Type().none:
        return None # v.content is a list of integer each one representing a byte
    else:
        raise TypeError(f"Cannot convert py-Type {v} to Value object. Conversion routine not implemented.")

def flatDictionary_to_flatdict(Dic: Dictionary) -> Optional[Dict]:
    if Dic is None:
        return None

    dic = {}
    for param in Dic:
        p: Parameter = param
        key = p.par_name

        (isCorrect, errMsg) = isTypeCorrect(p.value)
        if not isCorrect:
            raise TypeError(errMsg)

        value = _convertValue_to_pythondata(p.value)

        dic[key] = value

    return dic


if __name__ == '__main__':
    dic = {'xip': 2, 'msg': 'elemtar caro whatson', 'stream': b'Flavio', 'nomes': ['fla', 'flu'], 'nenhum': None}
    D: Dictionary = flatdict_to_flatDictionary(dic)
    print(D)

    dic = flatDictionary_to_flatdict(D)
    print(dic)

    pass