#!/usr/bin/env python
# pylint: disable=W0612,W1202

import os
import logging
import getpass
import shlex
from subprocess import Popen, PIPE
from murano_client import logger
from murano_client.client import WatchQueue, StoppableThread
from murano_client.__version__ import __version__


LOG = logger.getLogger('gwshell')
# LOG.setLevel(logging.DEBUG)


def which(pgm):
    path=os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p=os.path.join(p,pgm)
        if os.path.exists(p) and os.access(p,os.X_OK):
            return p

class GWShell(StoppableThread):
    def __init__(self):
        StoppableThread.__init__(self, name='GWShell')
        self.stdin = WatchQueue()
        self.stdout = WatchQueue()


    def run(self):

        LOG.info("Starting")
        current_dir = os.path.expanduser("~")
        shell = which('bash')
        LOG.info("shell: {}".format(shell))
        while not self.is_stopped():

            cmd = self.stdin.safe_get()
            if cmd:
                # get command from termin dataport
                try:
                    LOG.info("Received command: {}".format(cmd))
                    if cmd == 'exit':
                        self.stop()
                    cmd = [shell, '-c'] + shlex.split(cmd)
                    LOG.info("cwd: {}".format(current_dir))
                    LOG.info("cmd: {}".format(cmd))
                    process = Popen(
                        cmd,
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE,
                        # shell=True,
                        cwd=current_dir
                    )

                    # process.stdin.write(cmd.encode('utf-8')+'\n')
                    # process.stdin.flush()
                    # out, error = process.communicate(cmd.encode('utf-8'))
                    current_dir = os.path.abspath(os.getcwd())
                    # LOG.info("Command output: {}: {}".format(out, error))


                    result = ''
                    while True:
                        out = process.stdout.readline()

                        if out == '' and process.poll() != None:
                            # process.stdout.close()
                            break
                        # if out != '':
                        result += out
                        # print("{}".format(len(out)))

                    LOG.critical("{}".format(result))
                    self.stdout.put(result)

                except OSError as err:
                    # something went wrong with the Popen call.
                    # likely it's because there was nothing in termin. just fail silently
                    # TERM.write_stdout(str(err))
                    LOG.error("error: {}".format(err))
            # else:
            #     LOG.debug("No commands to process.")


