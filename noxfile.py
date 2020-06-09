import nox


file_locations = 'src', 'tests', 'noxfile.py'


@nox.session(python='3.8')
def coverage(session):
    session.install('coverage[toml]', 'codecov')
    session.run('coverage', 'xml', '--fail-under=0')
    session.run('codecov', *session.posargs)


@nox.session(python='3.8')
def lint(session):
    flake8_args = session.posargs or file_locations
    session.install(
        'darglint',
        'flake8',
        'flake8-black',
        'flake8-docstrings',
        'flake8-import-order',
    )
    session.run('flake8', *flake8_args)


@nox.session(python=['3.8', '3.7'])
def tests(session):
    pytest_args = session.posargs or ['--cov']
    session.run('poetry', 'install', external=True)
    session.run('poetry', 'run', 'pytest', *pytest_args, external=True)
