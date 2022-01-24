import os
import pathlib

import invoke

from .base import print_done, finalize


@invoke.task
def build_app(context):
    print("Building app...")
    context.run('poetry build --format=wheel > /dev/null')
    print_done()


@invoke.task(default=True, post=[build_app, finalize, ])
def build(_):
    print("Building...")


builder = invoke.Collection('build')
builder.add_task(build_app, 'app')
builder.add_task(build, 'all')
