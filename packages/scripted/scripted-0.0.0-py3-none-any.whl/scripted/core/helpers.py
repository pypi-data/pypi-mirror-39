"""Helper class of utility functions."""
import getpass
import inspect
import os
import subprocess


class Helpers(object):
    """Misc helper functions needed."""


    @property
    def scope(self):
        """Get name of current scope.

        Access the identifier of the current scope.
        Intended for accessing the name of the current method.

        Returns:
            str: name of scope where property is accessed.
        """
        return inspect.stack()[1][3]


    def __str__(self):
        return self.__class__.__name__


    def log(self, msg, level='INFO'):
        """Stub for logging module."""
        if os.getenv('DEBUGGING', False) == 'true':
            print(f"Logged {level}: {msg}")


    def print(self, *args):
        """Stub for safely handling stdout."""
        print(' '.join(list(args)))


    def prompt(self, msg, mode='stdin'):
        """Stub for safely handling stdin."""
        if mode == 'stdin':
            return input(msg)
        elif mode in ['un', 'user', 'username']:
            return getpass.getuser()
        elif mode in ['pw', 'pass', 'password']:
            return getpass.getpass()


    def shell(self, cmd=str):
        """Safely handle stdin with child processes.

        Args:
            cmd (str): shell command to run

        Returns:
            tuple: (stdout,stderr) of subprocess
        """
        return subprocess.Popen(cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT).communicate()
