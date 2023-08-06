from click import style as _style


def info(text):
    """Text in bold white."""
    return _style(text=text, bold=True)


def progress(text):
    """Text in bold blue."""
    return _style(text=text, fg='blue', bold=True)


def working(text):
    """Text in bold cyan."""
    return _style(text=text, fg='cyan', bold=True)


def success(text):
    """Text in bold green."""
    return _style(text=text, fg='green', bold=True)


def warning(text):
    """Text in bold yellow."""
    return _style(text=text, fg='yellow', bold=True)


def fail(text):
    """Text in bold red."""
    return _style(text=text, fg='red', bold=True)
