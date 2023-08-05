#!/usr/bin/env python3

'''
utility module;
'''

import sys

def die(s):

    '''
    print an error message and exit;
    '''

    print('error: ' + s, file=sys.stderr)
    sys.exit(1)

