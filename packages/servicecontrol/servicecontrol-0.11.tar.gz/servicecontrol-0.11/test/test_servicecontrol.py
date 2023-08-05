import os
import time
import signal
try:
    import prctl
    has_prctl = True
except:
    has_prctl = False


# from ctypes import cdll
# libc = cdll['libc.so.6']

def sigterm_handler(_signo, _stack_frame):
    print('PID {}. Got signal {}, but ignoring because I am naughty'.format(os.getpid(), _signo))


for i in range(3):
    pid = os.fork()
    if pid == 0:
        signal.signal(signal.SIGTERM, sigterm_handler)
    my_pid = os.getpid()

    # if os.getpgid(my_pid) != my_pid:
    #     os.setsid()

    if pid != 0:
        print('{} created a new process {}'.format(os.getpid(), pid))


time.sleep(.2)
# libc.prctl(1, signal.SIGTERM)#signal.SIGKILL)
if has_prctl:
    deathsig = prctl.get_pdeathsig()
else:
    deathsig = 'UNKNOWN'

print('My PID={}, My PGPID = {}, MySID = {}, My PR_DEATHSIG={}'.format(my_pid, os.getpgid(my_pid), os.getsid(my_pid), deathsig))


for i in range(90):
    try:
        time.sleep(1.0)
    except Exception as e:
        print('Exception {}: {}'.format(e.__class__.__name__, e))

print("{} Exiting".format(my_pid))

