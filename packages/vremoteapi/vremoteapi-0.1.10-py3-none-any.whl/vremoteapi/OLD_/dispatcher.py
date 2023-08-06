from typing import Callable

# Recebe stream de commandos em json, verifica integridade e assinatura, e caso ok dispacha para funcao de modo
# sincrono. Ao receber a resposta da funcao, reempacota resposta em json.

'''
def _jsonToCommand(json) -> Command:
    
    raise TypeError("Wrong signature!")
    pass


def _bind_run(c:Command, func) -> Answer:
    pars: Dictionary = _extract_parameters_from_command(Command)
    try:
        answer: = run(pars)
    except:
        # an exception was raised at-run-time during function execution
    ans: Answer = _convert_function_return_to_Answer(resp)
    return ans

Answer_Signature = DictSignature
Param_Signature = DictSignature
Func_Name_UUID = str
Function = Callable[[Any], Answer]
FunctionSignature = Tuple[Func_Name_UUID, Function, Param_Signature, Answer_Signature]
# ex: func = ('listaCom', None, 'list')

def addFunction(fun: VFunction):
    
    pass

'''

def me():
    print("me running...")
    pass

def metoo():
    print("metoo running...")
    pass




if __name__ == '__main__':

    from command import Command
    from typing import NamedTuple

    import json
    inidata = { 'cmd_uuid': 'serial_ports', 'parameters': {'a':1, 'b':2, 'd': 'juca', 'c': None} }
    cmd = Command(**inidata)
    print(cmd)
    parsed = json.dumps(cmd._asdict())
    print(parsed)
    d = json.loads(parsed)
    print(inidata == d)
    cmd = Command(**d)
    print(cmd.parameters)
    print(json.dumps(d))

    li = [me, metoo]
    for f in li:
        callf = f.__name__ + '()'
        eval(callf)

