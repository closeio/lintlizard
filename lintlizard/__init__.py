import subprocess
from typing import Iterable, Tuple

from attr import attrib, attrs

__version__ = '0.0.3'


@attrs(frozen=True)
class CommandTool:
    executable: str = attrib()
    run_params: Tuple[str, ...] = attrib(default=())

    def run_command(self) -> Tuple[str, ...]:
        return (self.executable,) + self.run_params

    def version_command(self) -> Tuple[str, ...]:
        return self.executable, '--version'


TOOLS = [
    CommandTool('flake8'),
    CommandTool('isort', run_params=('-rc', '-c', '.')),
    CommandTool('mypy'),
    CommandTool('black', run_params=('--check', '.')),
]


def execute_tools() -> Iterable[bool]:
    for tool in TOOLS:
        print('*' * 79)
        try:
            subprocess.run(args=tool.version_command(), check=True)
            subprocess.run(args=tool.run_command(), check=True)
        except subprocess.CalledProcessError:
            yield False
        else:
            yield True


def main() -> None:
    tool_results = list(execute_tools())
    if not all(tool_results):
        exit(1)


if __name__ == '__main__':
    main()
