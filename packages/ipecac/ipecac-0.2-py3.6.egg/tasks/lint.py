from invoke import task


@task
def flake8(ctx):
    """ Run the flake8 linter """
    ctx.run("python -m flake8 --exclude=docs,env,venv,ipecac.egg-info,.idea")
