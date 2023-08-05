# -*- coding: utf-8 -*-
"""librpi2caster - common classes, functions and definitions
for rpi2caster utility and hardware control daemons"""


class InterfaceException(Exception):
    """Base class for interface-related exceptions"""
    message = 'General interface error.'
    offending_value = ''

    def __str__(self):
        return self.message


class MachineStopped(InterfaceException):
    """machine not turning exception"""
    code = 0
    message = 'The machine was abnormally stopped.'


class UnsupportedMode(InterfaceException):
    """The operation mode is not supported by this interface."""
    code = 1

    @property
    def message(self):
        """error message with wrong mode"""
        return ('The {} mode is not supported by this interface.'
                .format(self.offending_value))


class UnsupportedRow16Mode(InterfaceException):
    """The row 16 addressing mode is not supported by this interface."""
    code = 2

    @property
    def message(self):
        """error message with wrong mode"""
        return ('The {} row 16 addressing mode is not supported '
                'by this interface.'.format(self.offending_value))


class InterfaceBusy(InterfaceException):
    """the interface was claimed by another client and cannot be used
    until it is released"""
    code = 3
    message = ('This interface was started and is already in use. '
               'If this is not the case, restart the interface.')


class InterfaceNotStarted(InterfaceException):
    """the interface was not started and cannot accept signals"""
    code = 4
    message = 'Trying to cast or punch with an interface that is not started.'


class ConfigurationError(InterfaceException):
    """configuration error: wrong name or cannot import module"""
    code = 5
    message = 'Hardware configuration error'


class CommunicationError(InterfaceException):
    """Error communicating with the interface."""
    code = 6
    message = ('Cannot communicate with the interface. '
               'Check the network connection and/or configuration.')
