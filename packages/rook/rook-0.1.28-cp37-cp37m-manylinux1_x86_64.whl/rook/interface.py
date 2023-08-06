"""This is the external interface to the Rook package."""
import sys
import os
import traceback

import six

_rook = None
_debug = False
_silence_errors = True

_TRUE_VALUES = ['y', 'Y', 'yes',  'Yes',  'YES', 'true', 'True', 'TRUE', '1', True]

def start(token=None,
          tags=None,
          host=None,
          port=None,
          debug=None,
          silence_errors=None,
          log_file=None,
          log_level=None,
          log_to_stderr=None,
          **kwargs):
    global _rook, _debug, _silence_errors

    if _rook is not None:
        return

    if isinstance(debug, bool):
        _debug = debug
    else:
        _debug = os.environ.get('ROOKOUT_DEBUG') in _TRUE_VALUES

    if isinstance(log_to_stderr, bool):
        log_to_stderr = log_to_stderr
    else:
        log_to_stderr = os.environ.get('ROOKOUT_LOG_TO_STDERR') in _TRUE_VALUES

    if isinstance(silence_errors, bool):
        _silence_errors = silence_errors

    if tags is None and isinstance(os.environ.get('ROOKOUT_ROOK_TAGS'), str):
        raw_tags = os.environ.get('ROOKOUT_ROOK_TAGS')

        # copied from Namespace serializer so to not import it
        def normalize_string(obj):
            if six.PY2:
                if isinstance(obj, str):
                    return unicode(obj, errors="replace")
                else:
                    return unicode(obj)
            else:
                return str(obj)

        tags = [normalize_string(tag.strip()) for tag in raw_tags.split(';') if tag]

    log_file = log_file or os.environ.get('ROOKOUT_LOG_FILE')
    log_level = log_level or os.environ.get('ROOKOUT_LOG_LEVEL')
    host = host or os.environ.get('ROOKOUT_AGENT_HOST')
    port = port or os.environ.get('ROOKOUT_AGENT_PORT')
    token = token or os.environ.get('ROOKOUT_TOKEN')

    try:
        from rook.exceptions.tool_exceptions import RookMissingToken, RookInvalidToken, RookVersionNotSupported, \
            RookCommunicationException, RookInvalidOptions
        try:
            from rook.config import LoggingConfiguration

            if log_file is not None:
                if not isinstance(log_file, str):
                    raise RookInvalidOptions('Rook log file should be a String')
                LoggingConfiguration.FILE_NAME = log_file

            if log_level is not None:
                if not isinstance(log_level, str):
                    raise RookInvalidOptions('Rook log level should be a String')
                LoggingConfiguration.LOG_LEVEL = log_level

            if log_to_stderr is not None:
                LoggingConfiguration.LOG_TO_STDERR = log_to_stderr

            if _debug:
                LoggingConfiguration.LOG_LEVEL = 'DEBUG'
                LoggingConfiguration.LOG_TO_STDERR = True
                LoggingConfiguration.DEBUG = True

            if isinstance(tags, list):
                for tag in tags:
                    if not isinstance(tag, six.string_types):
                        raise RookInvalidOptions('Rook tags should be array of strings')
            else:
                if tags:
                    raise RookInvalidOptions('Rook tags should be array of strings')

            if not host and not token:
                raise RookMissingToken()
            else:
                if token:
                    if not isinstance(token, str):
                        raise RookInvalidOptions('Rook token should be a String')

            if (host == "staging.cloud.agent.rookout.com") or (host == "cloud.agent.rookout.com"):
                host = "https://" + host

            import rook.singleton
            _rook = rook.singleton.singleton_obj

            return _rook.connect(token, host, port, tags)
        except (RookMissingToken, RookInvalidToken, RookVersionNotSupported) as e:
            six.print_("[Rookout] Failed to connect to the agent:", e, file=sys.stderr)
            raise
        except RookCommunicationException:
            six.print_("[Rookout] Failed to connect to the agent - will continue attempting in the background", file=sys.stderr)
            raise
        except ImportError as e:
            six.print_("[Rookout] Failed to import dependencies:", e, file=sys.stderr)
            raise
        except Exception as e:
            six.print_("[Rookout] Failed initialization:", e, file=sys.stderr)
            raise
    except Exception:
        if not _silence_errors:
            raise

        if _debug:
            traceback.print_exc()


def flush():
    global _rook
    if _rook is None:
        return

    _rook.flush()


def stop():
    global _rook
    if _rook is None:
        return

    _rook.stop()
    _rook = None
