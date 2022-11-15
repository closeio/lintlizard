import argparse
import subprocess
from typing import Iterable, Optional, Tuple

from attr import attrib, attrs

__version__ = '0.26.0'


Command = Tuple[str, ...]


@attrs(frozen=True)
class CommandTool:
    executable: str = attrib()
    ci_command: Optional["CommandTool"] = attrib(default=None)
    run_params: Command = attrib(default=())
    fix_params: Optional[Command] = attrib(default=None)

    # if set, supports running with individually specified files.
    # Otherwise, always runs without specifying files.
    default_files: Optional[Command] = attrib(default=None)

    def run_command(self, ci: bool) -> Command:
        if ci and self.ci_command is not None:
            return self.ci_command.run_command(ci=False)
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
    # Python source formatters
    CommandTool('flake8', default_files=()),
    CommandTool(
        'isort', run_params=('-c',), fix_params=(), default_files=('.',)
    ),
    CommandTool('dmypy', run_params=('run',), ci_command=CommandTool('mypy')),
    CommandTool(
        'black',
        run_params=('--check',),
        fix_params=(),
        default_files=('.',),
    ),
]


def execute_tools(
    fix: bool, check: bool, ci: bool, files: Tuple[str, ...]
) -> Iterable[Tuple[str, bool]]:
    # We need to run fixable tools first
    tools = sorted(TOOLS, key=lambda tool: not tool.fixable)

    if fix and not check:
        tools = [tool for tool in tools if tool.fixable]

    for tool in tools:
        print('*' * 79)
        try:
            subprocess.run(args=tool.version_command(), check=True)
            cmd = (
                tool.fix_command()
                if fix and tool.fix_params is not None
                else tool.run_command(ci=ci)
            )
            if tool.default_files is not None:
                cmd = cmd + (files or tool.default_files)
            subprocess.run(args=cmd, check=True)
        except subprocess.CalledProcessError:
            yield tool.executable, False
        else:
            yield tool.executable, True


def get_changed_files() -> Iterable[str]:
    try:
        subprocess.run(args=['git', '--version'], check=True)
        result = subprocess.run(
            args=[
                "git",
                "diff",
                "--name-only",
                "--cached",
                "--diff-filter=d",
                "HEAD",
                "--",
                "*.py",
            ],
            stdout=subprocess.PIPE,
        )
        # if no files are changed, don't return ['']
        return [
            i for i in result.stdout.decode('utf8').strip().split('\n') if i
        ]
    except subprocess.CalledProcessError:
        raise Exception('Error encountered when determining changed files.')


def main() -> None:
    args = make_arg_parser().parse_args()
    if args.version:
        print(f"lintlizard v{__version__}")
        return

    files = list(args.files) or []

    if args.changed:
        changed_files = get_changed_files()
        if not changed_files and not files:
            # ran as `lintlizard --changed` but nothing changed, don't run
            # anything
            return

        files.extend(changed_files)

    fix = args.fix or args.fix_and_check
    check = not fix or args.fix_and_check

    failed_tool_names = [
        name
        for name, result in execute_tools(
            fix=fix, check=check, ci=args.ci, files=tuple(files)
        )
        if not result
    ]

    print("\n" + "*" * 79)
    print("* Lintlizard summary")
    print("*" * 79)

    if failed_tool_names:
        print(
            "\033[0;31mThe following tools detected issues: "
            f"{', '.join(failed_tool_names)}\033[0m"
        )
        exit(1)

    print("\033[0;92mAll tools finished successfully.\033[0m")


def make_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ci', action='store_true')

    fix_group = parser.add_mutually_exclusive_group()
    fix_group.add_argument(
        '--fix',
        action='store_true',
        help=(
            "Fix issues that can be fixed automatically. "
            "Some code analysis will be omitted."
        ),
    )
    fix_group.add_argument(
        '--fix-and-check',
        action='store_true',
        help="Same as --fix, but also run a complete code analysis.",
    )

    parser.add_argument('--changed', action='store_true')
    parser.add_argument('--version', action='store_true')
    parser.add_argument('files', nargs='*', default=None)

    return parser


if __name__ == '__main__':
    main()
