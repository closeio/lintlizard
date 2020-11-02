import subprocess

__version__ = '0.0.2'


TOOLS = [
    ['flake8', '--version'],
    ['flake8'],
    ['isort', '--version'],
    ['isort', '-rc', '-c', '.'],
    ['mypy', '--version'],
    ['mypy'],
    ['black', '--version'],
    ['black', '--check', '.'],
]


def execute_tools() -> bool:
    for tool in TOOLS:
        try:
            subprocess.run(args=tool, check=True)
        except subprocess.CalledProcessError:
            return False

    return True


def main() -> None:
    if not execute_tools():
        exit(1)


if __name__ == '__main__':
    main()
