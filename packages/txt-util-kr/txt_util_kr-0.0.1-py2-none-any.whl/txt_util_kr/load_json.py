# -*- coding: utf-8 -*-
'''/**
     * created by M. Im 2017-11-03
     */'''

def load(jf):
    import json
    with open(jf) as json_data:
        return json.load(json_data)