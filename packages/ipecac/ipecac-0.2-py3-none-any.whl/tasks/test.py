from invoke import task


@task
def lint(ctx):
    """ Run the pylint linter """
    directories = ['examples', 'ipecac', 'tasks', 'test']
    disabled_checks = [
        'missing-docstring',
        'too-few-public-methods',
        'import-error,'
        'pointless-string-statement',
        'no-value-for-parameter',
        'len-as-condition',
        'consider-using-in',
        'no-self-use',
        'R0801', # similar lines in 2 files
        'invalid-name'
    ]
    dirs_to_check = ' '.join(directories)
    checks_to_ignore = ','.join(disabled_checks)
    ctx.run(f"pylint {dirs_to_check} --disable={checks_to_ignore}")

@task
def unit(ctx):
    """ Run the unit tests for ipecac """
    ctx.run("pytest")


@task
def full(ctx):
    """ Execute all test types """
    ctx.run("inv test.lint && inv test.unit")
