# permite checar assinatura de funcoes (se tipos correspondem a uma determinada assinatura)

from command import Dictionary, Parameter
from typing import List, Tuple, Optional
from type_checking import isTypeCorrect

Type = str
ErrMsg = Optional[str]
DictSignature = List[Tuple[str, Type]]  # ex: [('nome', 'str'), ('idade','int'), ( 'packet', 'bytes' )]


# checa apenas p tipo do valor
def isFlatDictSignatureCorrect(dic: Dictionary, sig: DictSignature) -> Tuple[bool, ErrMsg]:
    expectedSig:DictSignature = sig
    realSig: DictSignature = []

    # get real signature
    for param in dic:
        p: Parameter = param
        # confirme if param value is right
        (isOk, errMsg) = isTypeCorrect(p.value)
        if not isOk:
            return False, f"Assinatura de Dictionary incorreta. Parametro '{param}' possui tipo imcompativel com valor. Detalhe: {errMsg}"
        # get real param signature
        par_name = p.par_name
        type_ = p.value.type_
        tuple_ = (par_name, type_)
        realSig.append( tuple_ )


    # compare real w/ expected
    hasError = False
    if not len(expectedSig) == len(realSig):
        errmsg = f"Assinatura de Dictionary invalida. Assinatura esperada é '{expectedSig}', porem assinatura atual é {realSig}. "
        return False, errmsg

    for k in range(len(expectedSig)):
        if not realSig[k] == expectedSig[k]:
            errmsg = f"Assinatura de Dictionary invalida. Assinatura esperada é '{expectedSig}', porem assinatura atual é {realSig}. "
            errmsg = errmsg + f"Observe que o parametro '{realSig[k]}' é diferente do esperado '{expectedSig[k]}'"
            return False, errmsg

    return True, None


if __name__ == '__main__':

    d = {'a':2, 'z':66, 'texto': 'oi malandro', 'data': b'Flavinho', 'ports': ['com1', 'com2'], 'nenhum': None}
    from factories import flatdict_to_flatDictionary as dict_to_Dictionary
    dic = dict_to_Dictionary(d)

    sig = [ ('a','int'), ('z','int'), ('texto','str'), ('data','bytes'), ('ports', 'list'), ('nenhum', 'none') ]
    print(d)
    print(dic)
    print(sig)
    res = isOk, errMsg = isFlatDictSignatureCorrect(dic, sig)
    print(res)


    pass