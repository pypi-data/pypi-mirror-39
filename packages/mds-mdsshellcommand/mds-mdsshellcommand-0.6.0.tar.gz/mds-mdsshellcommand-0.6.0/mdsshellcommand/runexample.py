# -*- coding: utf-8 -*-

from mdslogger import MdsLogger
from libcommandrun import ShellCommandRun

if __name__ == '__main__':
    # test der funktion
    log1 = MdsLogger('logtest', conlogger=True, loglev='debug')
    ob2 = ShellCommandRun('jobtest', log1.getLogObj())
    (status, text1, code1) = ob2.runShellCmd2('ls -lah', 10)
    if status == True:
        log1.getLogObj().info('erfolgreich: Text: %s, Code=%d' % (text1, code1))
    else :
        log1.getLogObj().warning('upps: Text: %s, Code=%s' % (str(text1), str(code1)))
    del ob2
    del log1
    
