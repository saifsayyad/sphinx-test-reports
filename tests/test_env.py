from sphinx_testing import with_app
import re
import sphinx

sphinx_version = int(sphinx.__version__.split('.')[0] + sphinx.__version__.split('.')[1])

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

try:
    from StringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO  # Python 3
from subprocess import check_output, STDOUT


@with_app(buildername='html', srcdir='doc_test/env_report_doc')
def test_doc_env_report_build_html(app, status, warning):
    app.build()
    html = (app.outdir / 'index.html').read_text()

    assert '<h1>Test-Env report' in html
    assert '<th class="head">Variable</th>' in html

    tables = re.findall("(<table .*?</table>)", html, re.DOTALL)

    assert len(tables) == 2

    # All requested data should be in both tables
    assert 'name' in tables[0]
    assert 'path' in tables[0]
    assert 'host' in tables[0]

    assert 'name' in tables[1]
    assert 'path' in tables[1]
    assert 'host' in tables[1]

    # table 0 should contain py35
    assert 'py35' in tables[0]
    assert 'flake8' not in tables[0]

    # table 1 should contain flake8
    assert 'flake8' in tables[1]
    assert 'py35' not in tables[1]


@with_app(buildername='html', srcdir='doc_test/env_report_doc_raw')
def test_doc_env_report_raw_build_html(app, status, warning):
    app.build()
    html = (app.outdir / 'index.html').read_text()

    tables = re.findall("(<table .*?</table>)", html, re.DOTALL)
    assert len(tables) == 0

    # only requested data should be in the output document
    assert 'name' in html
    assert 'path' in html
    assert 'host' in html
    assert 'installed_packages' not in html

    # only requested environment should be present in output document
    assert 'py35' in html
    assert 'flake8' in html
    assert 'pylint' not in html


@with_app(buildername='html', srcdir='doc_test/env_report_doc_default')
def test_doc_env_report_default_build_html(app, status, warning):
    app.build()
    html = (app.outdir / 'index.html').read_text()

    tables = re.findall("(<table .*?</table>)", html, re.DOTALL)
    assert len(tables) == 3

    # checking if all env from JSON file is present in output or not in table format
    assert 'pylint' in tables[0] or 'pylint' in tables[1] or 'pylint' in tables[2]
    assert 'py35' in tables[0] or 'py35' in tables[1] or 'py35' in tables[2]
    assert 'flake8' in tables[0] or 'flake8' in tables[1] or 'flake8' in tables[2]
    assert 'py36' not in tables[0] or 'py36' not in tables[1] or 'py36' not in tables[2]

    # checking if all dataoptions are present in each output table or not
    for table in tables:
        assert 'path' in table
        assert 'name' in table
        assert 'reportversion' in table
        assert 'host' in table
        assert 'setup' in table
        assert 'platform' in table
        assert 'test' in table
        assert 'toxversion' in table
        assert 'python' in table
        assert 'installed_packages' in table
        assert 'installpkg' in table


@with_app(buildername='html', srcdir='doc_test/env_report_warnings')  # , warningiserror=False, verbosity=2)
def test_doc_env_report_warning_build_html(app, status, warning):

    # it should pass all test cases from: test_doc_env_report_build_html
    # generated output data will be stored here
    output = str(check_output(["sphinx-build", "-a", "-E", "-b", "html", app.srcdir, app.outdir],
                              stderr=STDOUT, universal_newlines=True))
    # app.build()
    html = (app.outdir / 'index.html').read_text()

    assert '<h1>Test-Env report' in html
    assert '<th class="head">Variable</th>' in html

    tables = re.findall("(<table .*?</table>)", html, re.DOTALL)

    assert len(tables) == 2

    # All requested data should be in both tables
    assert 'name' in tables[0]
    assert 'path' in tables[0]
    assert 'host' in tables[0]

    assert 'name' in tables[1]
    assert 'path' in tables[1]
    assert 'host' in tables[1]

    # table 0 should contain py35
    assert 'py35' in tables[0]
    assert 'flake8' not in tables[0]

    # table 1 should contain flake8
    assert 'flake8' in tables[1]
    assert 'py35' not in tables[1]

    """
    Taken from solution of this issue:
        https://github.com/useblocks/sphinxcontrib-needs/issues/44
    """
    
    if sphinx_version > 15:
        assert "WARNING: environment 'defs' is not present in JSON file" in output
        assert "WARNING: option 'abc' is not present in JSON file" in output
    else:
        assert "environment 'defs' is not present in JSON file" in output
        assert "option 'abc' is not present in JSON file" in output