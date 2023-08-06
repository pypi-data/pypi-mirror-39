from __future__ import print_function

import os
import platform
import string
import subprocess
import sys
import threading

class RunCmdResult(object):
    """ Container for the results of run_cmd """
    def __init__(self,echoStdout,echoStderr):
        self.retCode = 0;
        self.stdout = [];
        self.stderr = [];
        self.echoStdout = echoStdout;
        self.echoStderr = echoStderr;
    def addStdOut(self,lines):
        if (len(lines)==0):
            return;
        lines = map(lambda line: line.rstrip('\n'),lines)
        if (self.echoStdout):
            print("\n".join(lines), file=sys.stdout)
        self.stdout.extend(lines)
    def addStderr(self,lines):
        if (len(lines)==0):
            return;
        lines = map(lambda line: line.rstrip('\n'),lines)
        if (self.echoStderr):
            print("\n".join(lines), file=sys.stderr)
        self.stderr.extend(lines)

def run(command,echoCommand=True,throwOnNonZero=True):
    """ Run a command, but do not capture its output. Raise exception on non-zero status """
    if echoCommand:
        print( command )
        sys.stdout.flush()
    result = os.system(command)
    if throwOnNonZero and 0 != result:
        raise Exception("Command '{}' failed with status {}".format(command,result))
    return result
        
def run_cmd(args,throwOnNonZero = True,echoCommand=True,echoStdout=False,echoStderr=True):
    """ Run a command and capture its output. Optionally raise exception on non-zero status """
    if echoCommand:
        print(' '.join(args))
        sys.stdout.flush()
    # set the use show window flag, might make conditional on being in Windows:
    if platform.system() == 'Windows':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        startupinfo = None
    # pass as the startupinfo keyword argument:
    p=subprocess.Popen(args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=open(os.devnull), # subprocess.PIPE,
                             startupinfo=startupinfo)

    result = RunCmdResult(echoStdout,echoStderr);

    class StdoutReaderThread(threading.Thread):
        def __init__(self, stream, result):
            threading.Thread.__init__(self)
            self.stream = stream
            self.result = result
        def run(self):
            while True:
                lines = self.stream.readlines(1024)
                if len(lines) == 0:
                    break
                self.result.addStdOut(lines)
    class StderrReaderThread(threading.Thread):
        def __init__(self, stream, result):
            threading.Thread.__init__(self)
            self.stream = stream
            self.result = result
        def run(self):
            while True:
                lines = self.stream.readlines(1024)
                if len(lines) == 0:
                    break
                self.result.addStderr(lines)

    stdOutReader = StdoutReaderThread(p.stdout,result)
    stdOutReader.start()
    stdErrReader = StderrReaderThread(p.stderr,result)
    stdErrReader.start()

    result.retCode = p.wait()
    stdOutReader.join()
    stdErrReader.join()

    if (throwOnNonZero and result.retCode != 0):
        sys.stdout.flush();
        print( result.stderr, file=sys.stderr)
        sys.stderr.flush();
        raise Exception("Command Exited with status=%d" %result.retCode)
    return result;

