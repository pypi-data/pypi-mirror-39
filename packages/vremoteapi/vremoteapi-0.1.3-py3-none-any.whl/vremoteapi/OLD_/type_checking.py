# check if data type is right

from command import Value
from typing import Tuple, List, Optional
from types_ import suported_types, Type


# NOTA: o tipo de conteudo futuramente pode ser compativel com mais de um Type da libraria, por isto o retorno é uma lista
def _getMyPossibleTypes(content) -> Optional[List[str]]:
    if isinstance(content, str):
        return [Type().str]
    if isinstance(content, int):
        return [Type().int]
    if isinstance(content, list):
        return [Type().bytes, Type().list]
    if content is None:
        return [Type().none]
    else:
        return None

def _isSuportedType(type_) -> bool:
    for each in suported_types:
        if each == type_:
            return True
    return False

ErrMsg = Optional[str]

def isTypeCorrect(value: Value) -> Tuple[bool, ErrMsg]:

    # check if type informed is suported
    if not _isSuportedType(value.type_):
        return False, f"Tipo informado '{value.type_}' não é valido. Tipos validos são: {suported_types}"


    # check if type informed represent the value.content

    possibleRealDataTypes: List[str] = _getMyPossibleTypes(value.content)
    informedType = value.type_

    match = False
    for p in possibleRealDataTypes:
        #print(p)
        if p== informedType:
            match = True

    if match == False:
        errmsg = f"Tipo do valor invalido. Tipo informado é '{informedType}', porém o tipo real detectado é algum destes {possibleRealDataTypes}."
        return False, errmsg
    else:
        return True, None



if __name__ == '__main__':
    v = Value('list', [12,12,'com1','com2'])
    v = Value('none', None)
    tuple_ = (isCorrect, errMsg) = isTypeCorrect(v)
    dic = v._asdict()

    import json
    print(json.dumps(dic))

    print(tuple_)