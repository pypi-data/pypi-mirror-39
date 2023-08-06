from subprocess import run as subprocess_run


def run(command, **kwargs):
    subprocess_run(command, shell=True, **kwargs)


def shell(command, **kwargs):
    return subprocess_run(command, shell=True, capture_output=True, text=True, **kwargs)


def shell_list(command, **kwargs):
    yield subprocess_run(
        command, shell=True, capture_output=True, text=True, **kwargs
    ).stdout.split("\n")

