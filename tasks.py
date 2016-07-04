#!/usr/bin/env python3
from invoke import task
from invoke import Collection
import template.tasks
import scripts.tasks
import SalmoNet.tasks
import os

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
dist_path = "dist"
git_url = "git@github.com:TGAC/SalmoNet.git"
main_branch = "master"
deploy_branch = "gh-pages"

ns = Collection()

@task()
def test(ctx):
    ctx.run("echo \"main - OK\"")
ns.add_task(test)

@task()
def dist_clean(ctx):
    ctx.run("rm -rf %s" % dist_path, warn=True)
ns.add_task(dist_clean)

@task(dist_clean)
def dist_clone(ctx):
    ctx.run("git clone %s %s" % (git_url, dist_path))
    os.chdir(dist_path)
    ctx.run("git checkout %s" % deploy_branch)
    ctx.run("git rm -rf *")
ns.add_task(dist_clone)

@task(SalmoNet.tasks.generate_site)
def copy_deploy(ctx):
    os.chdir(ROOT_PATH)
    ctx.run("cp -r SalmoNet/public/* %s" % dist_path)
    ctx.run("echo \"salmonet.org\" > %s/CNAME" % dist_path)
ns.add_task(copy_deploy)

@task()
def clean_all(ctx):
    ctx.run("rm -rf %s" % dist_path, warn=True)
    ctx.run("rm -rf SalmoNet/public/*", warn=True)
    ctx.run("rm -rf SalmoNet/content/protein/*", warn=True)
    ctx.run("rm -rf scripts/temp_data/*", warn=True)
ns.add_task(clean_all)

@task(pre=[copy_deploy], post=[clean_all])
def deploy(ctx):
    os.chdir(dist_path)
    ctx.run("git add --all")
    ctx.run("git commit -am \"automatic deploy\"")
    ctx.run("git push origin %s" % deploy_branch)
ns.add_task(deploy)

ns.add_collection(template.tasks, 'template')
ns.add_collection(scripts.tasks, 'data')
ns.add_collection(SalmoNet.tasks, 'site')
