from typing import NamedTuple, List, Any, Optional

# a ideia é: passa um commando com parametros, e retorna um tuple com resultado ou erro


class Value(NamedTuple):
    type_: str    # int, str! (maybe on future) -> float, binary, bool...
    content: Any

class Parameter(NamedTuple):
    par_name: str
    value: Value


# ATTENTION: In this version Dictionary is always Flat !!
Dictionary = List[Parameter]

# representa o objeto de commando
class Command(NamedTuple):
    cmd_uuid: str
    parameters: Optional[Dictionary] = None

class ErrorInfo(NamedTuple):
    message: bool
    has_error: bool

class Answer(NamedTuple):
    response: Optional[Dictionary] = None
    error: Optional[ErrorInfo] = None
    history: Optional[List[Any]] = None



if __name__ == '__main__':

    a = Answer()

    import json
    print(json.dumps(a._asdict()))


    pass