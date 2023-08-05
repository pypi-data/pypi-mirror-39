"""Entry point of framework."""
import argparse
import functools
import sys

from scripted.core.bases import (
    BaseClass,
    ControllerBaseClass
)


class Script(BaseClass):
    """Decorators for creating MVC style command line tools."""

    controller_base_class = ControllerBaseClass

    @property
    def Controller(self):
        """Superclass of user defined Controller classes.

        Currently stubbing superclass of user defined controllers.
        Terminal instance decorators and inheritance used to create
        argparser and add utility functions to Controller subclasses.
        """
        self.fn.log("Inherited from ControllerBaseClass.")
        return self.controller_base_class


    def __init__(self):
        """Initialize main parser and sub-parser factory."""
        self.parsers = {'main': argparse.ArgumentParser()}
        self.factory = self.parsers['main'].add_subparsers()
        self.args = None
        self.argv = None
        self.decorated_class = None
        self.fn.log(f"Initialized {self} decorator.")


    def __route(self, command):
        """Route commands to Controller methods."""

        if command == '-h':
            self.parsers['main'].print_help()
        else:
            getattr(self.decorated_class, command)()

        self.fn.log(f"Called {command} on {self.decorated_class}")


    def __subparser(self, method):
        """Get or create subparsers created per Controller method."""

        self.fn.log(f"Get or create {method.__name__} sub-parser.")

        if method.__name__ in self.parsers:
            return self.parsers[method.__name__]

        subparser = self.factory.add_parser(
            method.__name__,
            description=method.__doc__,
            help=method.__doc__)

        self.parsers[method.__name__] = subparser
        return self.parsers[method.__name__]


    def add_controller(self, cls):
        """Decorating class builds its parsers."""

        self.parsers['main'].description = cls.__doc__
        self.decorated_class = cls()
        self.fn.log(f"Wrapped {self.decorated_class}")


    def argument(self, method, *args, **kwargs):
        """Add argparse arguments to decorated Controller methods"""

        @functools.wraps(method)
        def method_wrapper(method):
            self.__subparser(method).add_argument(*args, **kwargs)
            self.fn.log(msg=f'Added argument for {method.__name__}')
            return method

        return method_wrapper


    def execute(self):
        """Parse arguments and invoke Controller method."""

        self.fn.log(f"Routing arguments for Controller.")

        if len(sys.argv) <= 1:
            self.parsers['main'].print_help()
            sys.exit()

        self.argv = sys.argv
        self.args = self.parsers['main'].parse_args()
        self.decorated_class.args = self.args
        self.__route(sys.argv[1])


    def option(self, klass, *args, **kwargs):
        """Add argparse arguments to decorated Controller methods"""

        @functools.wraps(klass)
        def class_wrapper(kls):
            self.parsers['main'].add_argument(*args, **kwargs)
            self.fn.log(msg=f'Added option for {kls} with {args, kwargs}')
            return kls

        return class_wrapper
