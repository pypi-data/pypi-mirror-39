# J Kyle Medley 2018

from __future__ import print_function, division, absolute_import

from subprocess import Popen
from os.path import join, dirname
from time import sleep

p = Popen([],executable=join(dirname(__file__),'semgenapi'))
sleep(2)

from atexit import register
@register
def cleanup():
    p.kill()
