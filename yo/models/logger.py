import click


class Logger(object):
    def __init__(self):
        self.prefix = 'Yo, '

    def is_verbose(self):
        ctx = click.get_current_context()
        assert isinstance(ctx, click.core.Context)
        ctx.ensure_object(dict)
        return ctx.obj.get('verbose', False)

    def log(self, msg: str, **kwargs):
        """Logs a message."""
        click.secho(msg, **kwargs)

    def yo(self, msg: str, **kwargs):
        self.log(f'{self.prefix} {msg}', **kwargs)

    def green(self, msg: str):
        self.log(msg, fg='green')

    def yellow(self, msg: str):
        self.log(msg, fg='yellow')

    def red(self, msg: str):
        self.log(msg, fg='red')

    def vlog(self, msg: str, **kwargs):
        """Logs a message if verbose is enabled."""
        if self.is_verbose():
            self.log(f'[Verbose]: {msg}', **kwargs)
