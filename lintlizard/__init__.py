import argparse
import subprocess
from typing import Iterable, Optional, Tuple

from attr import attrib, attrs

__version__ = '0.0.4'


Command = Tuple[str, ...]


@attrs(frozen=True)
class CommandTool:
    executable: str = attrib()
    run_params: Command = attrib(default=())
    fix_params: Optional[Command] = attrib(default=None)

    def run_command(self) -> Command:
        return (self.executable,) + self.run_params

    @property
    def fixable(self):
        return self.fix_params is not None

    def fix_command(self) -> Command:
        if self.fix_params is None:
            raise RuntimeError('Command is not fixable')
        return (self.executable,) + self.fix_params

    def version_command(self) -> Command:
        return self.executable, '--version'


TOOLS = [
    CommandTool('flake8'),
    CommandTool('isort', run_params=('-c', '.'), fix_params=('.',)),
    CommandTool('mypy'),
    CommandTool('black', run_params=('--check', '.'), fix_params=('.',)),
]


def execute_tools(fix: bool) -> Iterable[bool]:
    tools = TOOLS
    if fix:
        tools = [tool for tool in tools if tool.fixable]
    for tool in tools:
        print('*' * 79)
        try:
            subprocess.run(args=tool.version_command(), check=True)
            cmd = tool.fix_command() if fix else tool.run_command()
            subprocess.run(args=cmd, check=True)
        except subprocess.CalledProcessError:
            yield False
        else:
            yield True


def main() -> None:
    args = make_arg_parser().parse_args()
    tool_results = list(execute_tools(fix=args.fix))
    if not all(tool_results):
        exit(1)


def make_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fix', action='store_true')

    return parser


if __name__ == '__main__':
    main()
