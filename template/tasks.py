#!/usr/bin/env python3
from invoke import task
import os



@task()
def test(ctx):
    ctx.run("echo \"template - OK\"")

@task()
def cd(ctx):
    os.chdir("template")

@task(cd)
def npm_install(ctx):
    ctx.run("npm install")

@task(npm_install)
def grunt_build(ctx):
    ctx.run("grunt build")

@task(grunt_build)
def copy_js(ctx):
    ctx.run("cp dist/js/app.js ../SalmoNet/themes/SalmoNet/static/js/app.js")

@task(grunt_build)
def copy_css(ctx):
    ctx.run("cp dist/css/style.css ../SalmoNet/themes/SalmoNet/static/css/style.css")

@task(copy_js, copy_css)
def deploy(ctx):
    print(" template - DONE")