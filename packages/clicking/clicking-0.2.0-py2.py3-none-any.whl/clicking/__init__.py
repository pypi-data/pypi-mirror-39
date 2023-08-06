from click import echo as _echo, ClickException as _ClickException
from . import style
from click_help_colors import (
    HelpColorsGroup as _HelpColorsGroup,
    HelpColorsCommand as _HelpColorsCommand,
)


__title__ = 'Clicking'
__version__ = '0.2.0'
__description__ = 'Convenience function for Click.'
__author__ = 'Andy Yulius'
__email__ = 'andy.julot@gmail.com'
__copyright__ = '© 2017-2018 Andy Yulius <andy.julot@gmail.com>'


def info(message, nl=True):
    """Print message in bold white."""
    return _echo(message=style.info(message), nl=nl)


def progress(message, nl=True):
    """Print message in bold blue."""
    return _echo(message=style.progress(message), nl=nl)


def working(message, nl=True):
    """Print message in bold cyan."""
    return _echo(message=style.working(message), nl=nl)


def success(message, nl=True):
    """Print message in bold green."""
    return _echo(message=style.success(message), nl=nl)


def warning(message, nl=True):
    """Print message in bold yellow."""
    return _echo(message=style.warning(message), nl=nl)


def fail(message, nl=True):
    """Print message in bold red."""
    return _echo(message=style.fail(message), nl=nl)


class Error(_ClickException):
    """Print an exception in bold red."""
    def show(self, file=None):
        fail('Error: %s' % self.format_message())


class _ColorMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help_headers_color = 'yellow'
        self.help_options_color = 'green'


class Group(_ColorMixin, _HelpColorsGroup):
    """Group with color."""


class Command(_ColorMixin, _HelpColorsCommand):
    """Command with color."""
