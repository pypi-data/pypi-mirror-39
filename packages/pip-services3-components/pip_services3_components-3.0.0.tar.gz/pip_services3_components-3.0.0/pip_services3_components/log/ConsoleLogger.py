# -*- coding: utf-8 -*-
"""
    pip_services3_components.log.ConsoleLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Console logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import sys
import datetime
import traceback

from .LogLevel import LogLevel
from .ILogger import ILogger
from .LogLevelConverter import LogLevelConverter
from .Logger import Logger

class ConsoleLogger(Logger):
    """
    Logger that writes log messages to console.

    Errors are written to standard err stream and all other messages to standard out stream.

    ### Configuration parameters ###

        - level:             maximum log level to capture
        - source:            source (context) name

    ### References ###
        - *:context-info:*:*:1.0     (optional) [[ContextInfo]] to detect the context id and specify counters source

    Example:
        logger = ConsoleLogger()
        logger.set_level(LogLevel.debug)

        logger.error("123", ex, "Error occured: %s", ex.message)
        logger.debug("123", "Everything is OK.")
    """
    def _compose_error(self, error):
        result = ""
        while error != None:
            if len(result) > 0:
                result += " Cause by error: "

            result += result + str(error)
            
            if hasattr(error, 'stack_trace'):
                result += " StackTrace: " + error.stack_trace

            if hasattr(error, 'cause'):
                error = error.cause
            elif hasattr(error, '__traceback__'):
                error = error.__traceback__
            else:
                error = None

        return result

    def _write(self, level, correlation_id, error, message):
        """
        Writes a log message to the logger destination.

        :param level: a log level.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param error: an error object associated with this message.

        :param message: a human-readable message to log.
        """
        if (self._level < level):
            return

        output = "["
        output += correlation_id if correlation_id != None else "---"
        output += ":"
        output += LogLevelConverter.to_string(level)
        output += ":"
        output += datetime.datetime.utcnow().isoformat()
        output += "] "

        output += message

        if error != None:
            if len(message) == 0:
                output += "Error: "
            else:
                output += ": "

            output += self._compose_error(error)

        output += "\n"

        if level >= LogLevel.Fatal and level <= LogLevel.Warn:
            sys.stderr.write(output)
        else:
            sys.stdout.write(output)