class CommandTypes():
    native = 'native'
    shell = 'shell'
    powershell = 'powershell'
    python = 'python'
    java = 'java'
    javascript = 'javascript'
    typescript = 'typescript'
    sql = 'sql'


class CommandGroup():

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.commands = [Command.build(c) for c in kwargs.get('commands')]
        self.invoke = kwargs.get('invoke', None)
        self.type = kwargs.get('type', CommandTypes.shell)

    def build(cmd_group_kwargs: dict) -> 'CommandGroup':
        if cmd_group_kwargs:
            return CommandGroup(**cmd_group_kwargs)

    def __repr__(self):
        return str(self.__dict__)

    def __add__(self, other: 'CommandGroup') -> 'CommandGroup':
        pass

    def generate_cli_module(self, module_file):
        pass


class Command():

    def __int__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.invoke = kwargs.get('invoke', '')
        self.type = kwargs.get('type', CommandTypes.shell)

    @staticmethod
    def build(cmd_kwargs: dict) -> 'Command':
        if cmd_kwargs:
            return Command(**cmd_kwargs)

    def __repr__(self):
        return str(self.__dict__)

    def __add__(self, other: 'Command') -> 'Command':
        pass
