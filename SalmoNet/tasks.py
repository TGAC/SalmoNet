#!/usr/bin/env python3
from invoke import task
import os
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


@task()
def test(ctx):
    ctx.run("echo \"site - OK\"")

@task()
def cd(ctx):
    os.chdir(ROOT_PATH)

@task(cd)
def generate_site(ctx):
    ctx.run("hugo --uglyURLs")