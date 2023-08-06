# helper object

from main import Interface, run, cast_result, create_remote_json_call
from typing import Dict, Any

from typing import NamedTuple

class RemoteApi:
    def __init__(self, api: Interface) -> None:
        self._api = api

    def _run_dont_cast_result(self, _json:str) -> Any:
        return run(_json, self._api)

    def run(self, _json:str) -> Dict[str, Any]:
        result = self._run_dont_cast_result(_json)
        return cast_result(result)


# -------- Test

def me():
    print("me running...")
    pass

def metoo(a, b):
    print("metoo running...")
    return {'a=': a, 'b=' : b}

def me2():
    print("me2 running...")
    pass

def metoo2(a, b):
    print("metoo2 running...")
    return {'a=': a, 'b=' : b}


if __name__ == '__main__':

    api: Interface = [ me, metoo, me2, metoo2 ]

    remoteApi = RemoteApi(api)
    rcall = create_remote_json_call
    calls = [
        rcall('me', None),
        rcall('me2', None),
        rcall('metoo2', [1,2]),
        rcall('metoo2', [1, 'flavitcho']),
        rcall('metoo', [1, {'dict': 'olha só'}]),
        rcall('NON_EXISTENT_FUNC', [1, {'dict': 'olha só'}])
    ]

    for _call in calls:
        res = remoteApi.run(_call)
        print(res)


