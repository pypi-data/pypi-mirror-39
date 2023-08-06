from invoke import task


@task
def save_deps(ctx):
    """ Generate a new requirements.txt file """
    ctx.run("pip freeze > requirements.txt")


@task
def install_deps(ctx):
    """ Install the requirements.txt file """
    ctx.run("pip install -r requirements.txt")


@task
def install_dev(ctx):
    """ Install the current branch of ipecac """
    ctx.run("python setup.py develop")


@task
def install(ctx):
    """ Install ipecac for regular usage """
    ctx.run("inv build.install-deps && python setup.py install")
