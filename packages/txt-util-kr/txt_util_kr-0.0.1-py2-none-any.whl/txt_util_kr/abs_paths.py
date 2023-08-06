# -*- coding: utf-8 -*-
'''/**
     * created by M. Im 2017-08-03
     */'''

def get_paths(directory):
    import os
    try:
        os.path.exists(directory)
        return [os.path.join(directory,f) for f in os.listdir(directory)]
    except:
        print('Path doesn\'t exists or it is not a directory! ')