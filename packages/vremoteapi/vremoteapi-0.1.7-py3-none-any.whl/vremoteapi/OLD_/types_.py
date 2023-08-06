from typing import NamedTuple


# tipos considerados validos
# este objeto na verdade funciona como um Enum
class Type(NamedTuple):
    str = 'str'
    int = 'int'
    bytes = 'bytes' #bytes sao armazenados como uma lista de inteiros (entre 0<255)
    list = 'list'  #heterogeneous list
    none = 'none'

# universo de tipos suportados
suported_types = [ Type().str, Type().int, Type().bytes, Type().list, Type().none ]
