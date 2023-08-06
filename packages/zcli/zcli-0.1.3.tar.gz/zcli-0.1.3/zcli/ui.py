import sys
import time
import functable


UI_CLASSES = functable.FunctionTable()


def make_ui(verbosity):
    return UI_CLASSES[verbosity]()


def _write_line(tmpl, *args, **kw):
    sys.stderr.write(
        '{} {}\n'.format(
            time.strftime('%Y-%m-%d %H:%M:%S%z'),
            tmpl.format(*args, **kw),
        ),
    )


@UI_CLASSES.register
class quiet (object):
    def handle_failure(self, tmpl, *args, **kw):
        _write_line('FAILURE: {}'.format(tmpl), *args, **kw)

    def status(self, tmpl, *args, **kw):
        pass

    def debug(self, tmpl, *args, **kw):
        pass


@UI_CLASSES.register
class standard (quiet):
    def status(self, tmpl, *args, **kw):
        _write_line(tmpl, *args, **kw)


@UI_CLASSES.register
class debug (standard):
    def debug(self, tmpl, *args, **kw):
        _write_line('debug: {}'.format(tmpl), *args, **kw)
