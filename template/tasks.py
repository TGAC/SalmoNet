#!/usr/bin/env python3
from invoke import task
import os

@task
def test(ctx):
    ctx.run("echo \"template - OK\"")

@task
def npm(ctx):
    os.chdir("template")
    ctx.run("npm install")

