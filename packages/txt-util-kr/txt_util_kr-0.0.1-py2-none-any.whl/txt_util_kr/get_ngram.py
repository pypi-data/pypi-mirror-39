# -*- coding: utf-8 -*-
'''/**
     * created by M. Im 2017-11-10
     */'''

def ngram(L,ngramN):
    L2,size=[],len(L)
    for i in range(size):
        for n in ngramN:
            if i+n<=size: L2.append('_'.join(L[i:i+n]))
        # end for
    # end for

    return L2

def Space_skip_ngram(L,ngramN):
    Ls = L.split()
    Space_skip_ngrams = []
    for l in Ls:

        if len(l)<ngramN[0]:
            pass
        else:

            Space_skip_ngrams+=ngram(l,ngramN)

    return Space_skip_ngrams