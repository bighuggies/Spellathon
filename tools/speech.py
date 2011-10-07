"""
Module to handle text to speech.

Exported classes:

Speech -- Text to speech

"""
import subprocess
import os
import signal
import tkMessageBox

class Speech(object):
    """Takes strings and converts them to audio (speech).
    
    Public functions:
    speak -- Given a string, speak it out loud
    kill -- Stop all currently running speech processes
        
    """            
    def __init__(self):
        self.procs = []

    def speak(self, text):
        """
        Open a festival subprocess which will have a new session id, send the
        text to be spoken to festival, and add the subprocess to a list of
        festival subprocesses.
        
        Arguments:
        text -- The text to be spoken
        
        """
        try:
            p = subprocess.Popen('festival', preexec_fn=os.setsid,
                                 stdin=subprocess.PIPE)

            p.stdin.write('(SayText "%s")' % text)
            p.stdin.close()
            self.procs.append(p)
        except OSError:
            tkMessageBox.showinfo('Festival error!',
                                  'Error opening festival! Are you sure you have it correctly installed?')

    def kill(self):
        """Kill all running instances of festival."""
        while self.procs:
            p = self.procs.pop()
            if p.poll() is None:
                os.killpg(os.getpgid(p.pid), signal.SIGKILL)