"""
Virtualenv and launcher script rolled into one.

This is copied in part from https://docs.python.org/3/library/venv.html.
"""

import os.path
import sys
import venv
from subprocess import Popen

win32 = os.name == 'nt'


class ExtendedEnvBuilder(venv.EnvBuilder):
    def post_setup(self, context):
        # install the bot-specific packages
        if win32:
            pip = "./venv/Scripts/pip.exe"
        else:
            pip = "./venv/bin/pip"
        with open("requirements.txt", "r") as f:
            requirements = f.readlines()
        proc = Popen([pip, "install"] + requirements)
        proc.communicate()


def run():
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    if win32:
        path = "./venv/Scripts/python.exe"
    else:
        path = "./venv/bin/python3"

    print("\n\nSpawning: {} tests/{}\n\n".format(os.path.abspath(path), sys.argv[1]))
    proc = Popen([os.path.abspath(path), "tests/{}".format(sys.argv[1])],
                 cwd=os.getcwd(), env=env)

    proc.communicate()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("home.py")

    print("Need to create environment:", not os.path.exists("./venv"))
    if not os.path.exists("./venv"):
        print("Creating a new virtual environment...")
        builder = ExtendedEnvBuilder(with_pip=True)
        builder.create("./venv")

    while True:
        run()
