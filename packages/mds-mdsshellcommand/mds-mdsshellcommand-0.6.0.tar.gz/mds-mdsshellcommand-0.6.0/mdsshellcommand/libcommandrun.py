# -*- coding: utf-8 -*-


import subprocess, shlex, os, threading, time, sys
from mdslogger import formatExceptionInfo 


class ShellCommandRun:
    """ executes a shell command
    """
    def __init__(self, jobname, logger):
        """ settings
        """
        self.__jobname = jobname
        self.__log = logger
      
    def __del__(self):
        """ cleanup
        """
        self.__jobname = ''
        self.__log = None
        
    def lowpriority(self):
        """ Set the priority of the process to below-normal.
        """
        self.__log.debug('+- Reduce process priority')
        try:
            sys.getwindowsversion()
        except:
            isWindows = False
        else:
            isWindows = True
        
        if isWindows:
            self.__log.debug('|- use Windows method')
            # Based on:
            #   "Recipe 496767: Set Process Priority In Windows" on ActiveState
            #   http://code.activestate.com/recipes/496767/
            import win32api, win32process, win32con
            
            pid = win32api.GetCurrentProcessId()
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
            win32process.SetPriorityClass(handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)
        else:
            self.__log.debug('|- use Linux method')
            os.nice(1)
        self.__log.debug('-- Process priority successfully reduced')
    
    def runShellCmd(self, cmdtxt):
        """ executes a shell command
            returncodes: (<status>, <text>, <retcode>)
            status: True = Action successful, False: OS- oder Programerror
            text: if <status>=True: Text output of the program,
                  if (<status>=False) and (OS-Error): Errortext from OS
                  if (<status>=False) and (program error): Errortext from program
            retcode: if <status>=True: 0
                     if (<status>=False) and OS-Error: Errorcode vom OS
                     if (<status>=False) and program error: Errorcode from Program
        """
        try :
            self.__log.debug('+- Execute shell command: %s' % cmdtxt)
            errno = 0
            retcode = 0
            stdout = ''
            try :
                if os.name == 'posix':
                    if ('|' in cmdtxt) or ('>' in cmdtxt) or ('<' in cmdtxt):
                        cmd1 = cmdtxt
                    else :
                        cmd1 = shlex.split(cmdtxt)
                else :
                    cmd1 = cmdtxt
              
                stderr = ''
                stdout = ''
                if ('|' in cmdtxt) or ('>' in cmdtxt) or ('<' in cmdtxt):
                    # the pipe treatment is done by the shell
                    retcode = 0
                    try :
                        retcode = subprocess.check_call(cmd1, shell=True)
                    except subprocess.CalledProcessError as e:
                        retcode = e.returncode
                        stderr = e.output
                else :
                    proc = subprocess.Popen(cmd1, bufsize=1, \
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = proc.communicate()
                    retcode = proc.returncode
            except OSError as e:
                stderr = 'OSError: %s' % e.strerror
                errno = e.errno
            self.__log.debug('-- Shell command finished')
    
            if (retcode == 0) and (errno == 0):
                return (True, str(stdout) + str(stderr), retcode)
            else :
                if errno != 0:
                    return (False, str(stdout) + str(stderr), errno)
                else :
                    return (False, str(stdout) + str(stderr), retcode)
        except :
            self.__log.error(str(formatExceptionInfo()))

    def runShellCmd2(self, cmd, timeout_sec):
        """ runs a shell command as a thread, kills it if it takes too long
        """
        self.__log.debug("+- Execute shell command: '%s'" % cmd)
        class CmdThread(threading.Thread):
            def __init__(self, kwargs):
                threading.Thread.__init__(self, kwargs=kwargs)
                self.proc = None
                self.stdout = None
                self.stderr = None
                self.errno = 0
                self.cmd = kwargs['cmd']
  
            def run(self):
                """ run-function
                """ 
                try :
                    if os.name == 'posix':
                        cmd1 = shlex.split(self.cmd)
                    else :
                        cmd1 = self.cmd
                    self.proc = subprocess.Popen(cmd1, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.stdout, self.stderr = self.proc.communicate()
                except OSError as e:
                    self.stderr = 'OSError: %s' % e.strerror
                    self.errno = e.errno
        # end CmdThread
  
        # prepare job
        job1 = CmdThread(kwargs={'cmd':cmd})
        job1.start()
        self.__log.debug("|- Job started: '%s'" % cmd)
        # wait for the end of the job or the timeout
        job1.join(float(timeout_sec))
        self.__log.debug("|- Job finished: '%s'" % cmd)
      
        ok1 = True
        # possibly cancel job
        if job1.isAlive() == True:
            self.__log.info("|- job is still running, terminate '%s'" % cmd)
            job1.proc.terminate()
            ok1 = False
            time.sleep(1)
              
        # if 'terminate' did not work -> send kill
        if job1.isAlive() == True:
            self.__log.info("|- job is still running, killing: '%s'" % cmd)
            job1.proc.kill()
            time.sleep(1)
              
        stdout = ''
        if isinstance(job1.stdout, type(None)) == False:
            stdout = job1.stdout
        stderr = ''
        if isinstance(job1.stderr, type(None)) == False:
            stderr = job1.stderr
      
        # accept error codes
        try :
            retcode = job1.proc.returncode
        except :
            retcode = 0
        errno = job1.errno

        if (retcode == 0) and (errno == 0) and (ok1 == True):
            erg1 = (True, stdout + stderr, retcode)
        else :
            if errno != 0:
                erg1 = (False, stdout + stderr, errno)
            else :
                erg1 = (False, stdout + stderr, retcode)
    
        del job1.proc
        del job1
        self.__log.debug("-- job done: status=%s\nText: %s\nCode = %s" % erg1)
        return erg1

# end ShellCommandRun
