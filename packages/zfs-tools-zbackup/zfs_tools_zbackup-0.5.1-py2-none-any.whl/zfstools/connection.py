'''
ZFS connection classes
'''

import subprocess
import os
from zfstools.models import PoolSet
from zfstools.util import progressbar, SpecialPopen, verbose_stderr
from Queue import Queue
from threading import Thread


# Work-around for check_output not existing on Python 2.6, as per
# http://stackoverflow.com/questions/4814970/subprocess-check-output-doesnt-seem-to-exist-python-2-6-5
# The implementation is lifted from
# http://hg.python.org/cpython/file/d37f963394aa/Lib/subprocess.py#l544
if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd) # , output=output)
        return output
    subprocess.check_output = f

class ZFSConnection:
    host = None
    _poolset = None
    _dirty = True
    _trust = False
    _properties = None
    def __init__(self,host="localhost", trust=False, sshcipher=None, properties=None, identityfile=None, knownhostsfile=None, verbose=False):
        self.host = host
        self._trust = trust
        self._properties = properties if properties else []
        self._poolset= PoolSet()
        self.verbose = verbose
        if host in ['localhost','127.0.0.1']:
            self.command = []
        else:
            self.command = ["ssh","-o","BatchMode=yes","-a","-x"]
            if self._trust:
                self.command.extend(["-o","CheckHostIP=no"])
                self.command.extend(["-o","StrictHostKeyChecking=no"])
            if sshcipher != None:
                self.command.extend(["-c",sshcipher])
            if identityfile != None:
                self.command.extend(["-i",identityfile])
            if knownhostsfile != None:
                self.command.extend(["-o","UserKnownHostsFile=%s" % knownhostsfile])
            self.command.extend([self.host])

    def _get_poolset(self):
        if self._dirty:
            properties = [ 'creation' ] + self._properties
            stdout2 = subprocess.check_output(self.command + ["zfs", "list", "-Hpr", "-o", ",".join( ['name'] + properties ), "-t", "all"])
            self._poolset.parse_zfs_r_output(stdout2,properties)
            self._dirty = False
        return self._poolset
    pools = property(_get_poolset)

    def create_dataset(self, name, parents=False):
        parents_opt = ["-p"] if parents else []
        subprocess.check_call(self.command + ["zfs", "create"] + parents_opt + [name])
        self._dirty = True
        return self.pools.lookup(name)

    def destroy_dataset(self, name):
        subprocess.check_call(self.command + ["zfs", "destroy", name])
        self._dirty = True

    def destroy_recursively(self, name, returnok=False):
        """If returnok, then simply return success as a boolean."""
        ok = True
        cmd = self.command + ["zfs", "destroy", '-r', name]
        if returnok:
            ok = subprocess.call(cmd) == 0
        else:
            subprocess.check_call(cmd)
        self._dirty = True
        return ok

    def snapshot_recursively(self,name,snapshotname,properties={}):
        plist = sum( map( lambda x: ['-o', '%s=%s' % x ], properties.items() ), [] )
        subprocess.check_call(self.command + ["zfs", "snapshot", "-r" ] + plist + [ "%s@%s" % (name, snapshotname)])
        self._dirty = True

    def send(self,name,opts=None,bufsize=-1,compression=False,lockdataset=None):
        if not opts: opts = []
        cmd = list(self.command)
        if compression and cmd[0] == 'ssh': cmd.insert(1,"-C")
        if lockdataset is not None:
            cmd += ["zflock"]
            if self.verbose:
                cmd += ["-v"]
            cmd += [lockdataset, "--"]
        cmd += ["zfs", "send"] + opts
        if "-t" not in opts:
            # if we're resuming, don't specify the name of what to send
            cmd += [name]
        verbose_stderr("%s\n" % ' '.join(cmd))
        p = SpecialPopen(cmd,stdin=file(os.devnull),stdout=subprocess.PIPE,bufsize=bufsize)
        return p

    def receive(self,name,pipe,opts=None,bufsize=-1,compression=False,lockdataset=None):
        if not opts: opts = []
        cmd = list(self.command)
        if compression and cmd[0] == 'ssh': cmd.insert(1,"-C")
        if lockdataset is not None:
            cmd += ["zflock"]
            if self.verbose:
                cmd += ["-v"]
            cmd += [lockdataset, "--"]
        cmd = cmd + ["zfs", "receive"] + opts + [name]
        verbose_stderr("%s\n" % ' '.join(cmd))
        p = SpecialPopen(cmd,stdin=pipe,bufsize=bufsize)
        return p

    def transfer(self, dst_conn, s, d, fromsnapshot=None, showprogress=False, bufsize=-1, send_opts=None, receive_opts=None, ratelimit=-1, compression=False, locksrcdataset=None, lockdstdataset=None, verbose=False, resumable=False):
        if send_opts is None: send_opts = []
        if receive_opts is None: receive_opts = []

        try:
            resume_token = dst_conn.pools.lookup(d).get_property("receive_resume_token")
        except:
            resume_token = None

        queue_of_killables = Queue()

        if fromsnapshot: fromsnapshot=["-i",fromsnapshot]
        else: fromsnapshot = []
        if verbose: verbose_opts = ["-v"]
        else: verbose_opts = []
        # Regardless of whether resumable is requested this time , if
        # there's a resume token on the destination, we have to use it.
        if resume_token is not None:
            all_send_opts = ["-t", resume_token] + verbose_opts
        else:
            all_send_opts = [] + fromsnapshot + send_opts + verbose_opts
        sndprg = self.send(s, opts=all_send_opts, bufsize=bufsize, compression=compression, lockdataset=locksrcdataset)
        sndprg_supervisor = Thread(target=lambda: queue_of_killables.put((sndprg, sndprg.wait())))
        sndprg_supervisor.start()

        if showprogress:
            try:
                        barprg = progressbar(pipe=sndprg.stdout,bufsize=bufsize,ratelimit=ratelimit)
                        barprg_supervisor = Thread(target=lambda: queue_of_killables.put((barprg, barprg.wait())))
                        barprg_supervisor.start()
                        sndprg.stdout.close()
            except OSError:
                        os.kill(sndprg.pid,15)
                        raise
        else:
            barprg = sndprg

        try:
                        if resumable: resumable_recv_opts = ["-s"]
                        else: resumable_recv_opts = []
                        all_recv_opts = ["-Fu"] + verbose_opts + resumable_recv_opts + receive_opts
                        rcvprg = dst_conn.receive(d,pipe=barprg.stdout,opts=all_recv_opts,bufsize=bufsize,compression=compression, lockdataset=lockdstdataset)
                        rcvprg_supervisor = Thread(target=lambda: queue_of_killables.put((rcvprg, rcvprg.wait())))
                        rcvprg_supervisor.start()
                        barprg.stdout.close()
        except OSError:
                os.kill(sndprg.pid, 15)
                if sndprg.pid != barprg.pid: os.kill(barprg.pid, 15)
                raise

        dst_conn._dirty = True
        allprocesses = set([rcvprg, sndprg]) | ( set([barprg]) if showprogress else set() )
        while allprocesses:
            diedprocess, retcode = queue_of_killables.get()
            allprocesses = allprocesses - set([diedprocess])
            if retcode != 0:
                [ p.kill() for p in allprocesses ]
                raise subprocess.CalledProcessError(retcode, diedprocess._saved_args)
