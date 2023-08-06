from __future__ import absolute_import
from ._info import __doc__  # @UnresolvedImport
from ._core import *
from .objects import *


__version__ = "0.6.0"


def test(*options):
    """
    usage: test(option1, option2, ...., file_or_dir)

    positional arguments:
      file_or_dir

    general:
      -k EXPRESSION         only run tests which match the given substring
                            expression. An expression is a python evaluatable
                            expression where all names are substring-matched
                            against test names and their parent classes. Example:
                            -k 'test_method or test_other' matches all test
                            functions and classes whose name contains
                            'test_method' or 'test_other'. Additionally keywords
                            are matched to classes and functions containing extra
                            names in their 'extra_keyword_matches' set, as well as
                            functions which have names assigned directly to them.
      -m MARKEXPR           only run tests matching given mark expression.
                            example: -m 'mark1 and not mark2'.
      --markers             show markers (builtin, plugin and per-project ones).
      -x, --exitfirst       exit instantly on first error or failed test.
      --maxfail=num         exit after first num failures or errors.
      --strict              marks not registered in configuration file raise
                            errors.
      -c file               load configuration from `file` instead of trying to
                            locate one of the implicit configuration files.
      --continue-on-collection-errors
                            Force test execution even if collection errors occur.
      --fixtures, --funcargs
                            show available fixtures, sorted by plugin appearance
      --fixtures-per-test   show fixtures per test
      --import-mode={prepend,append}
                            prepend/append to sys.path when importing test
                            modules, default is to prepend.
      --pdb                 start the interactive Python debugger on errors.
      --pdbcls=modulename:classname
                            start a custom interactive Python debugger on errors.
                            For example:
                            --pdbcls=IPython.terminal.debugger:TerminalPdb
      --capture=method      per-test capturing method: one of fd|sys|no.
      -s                    shortcut for --capture=no.
      --runxfail            run tests even if they are marked xfail
      --lf, --last-failed   rerun only the tests that failed at the last run (or
                            all if none failed)
      --ff, --failed-first  run all tests but run the last failures first. This
                            may re-order tests and thus lead to repeated fixture
                            setup/teardown
      --cache-show          show cache contents, don't perform collection or tests
      --cache-clear         remove all cache contents at start of test run.
      --flakes              run pyflakes on .py files
      --pep8                perform some pep8 sanity checks on .py files

    reporting:
      -v, --verbose         increase verbosity.
      -q, --quiet           decrease verbosity.
      -r chars              show extra test summary info as specified by chars
                            (f)ailed, (E)error, (s)skipped, (x)failed, (X)passed,
                            (p)passed, (P)passed with output, (a)all except pP.
                            Warnings are displayed at all times except when
                            --disable-warnings is set
      --disable-warnings, --disable-pytest-warnings
                            disable warnings summary
      -l, --showlocals      show locals in tracebacks (disabled by default).
      --tb=style            traceback print mode (auto/long/short/line/native/no).
      --full-trace          don't cut any tracebacks (default is to cut).
      --color=color         color terminal output (yes/no/auto).
      --durations=N         show N slowest setup/test durations (N=0 for all).
      --pastebin=mode       send failed|all info to bpaste.net pastebin service.
      --junit-xml=path      create junit-xml style report file at given path.
      --junit-prefix=str    prepend prefix to classnames in junit-xml output
      --result-log=path     DEPRECATED path for machine-readable result log.

    collection:
      --collect-only        only collect tests, don't execute them.
      --pyargs              try to interpret all arguments as python packages.
      --ignore=path         ignore path during collection (multi-allowed).
      --confcutdir=dir      only load conftest.py's relative to specified dir.
      --noconftest          Don't load any conftest.py files.
      --keep-duplicates     Keep duplicate tests.
      --collect-in-virtualenv
                            Don't ignore tests in a local virtualenv directory
      --doctest-modules     run doctests in all .py modules
      --doctest-report={none,cdiff,ndiff,udiff,only_first_failure}
                            choose another output format for diffs on doctest
                            failure
      --doctest-glob=pat    doctests file matching pattern, default: test*.txt
      --doctest-ignore-import-errors
                            ignore doctest ImportErrors

    test session debugging and configuration:
      --basetemp=dir        base temporary directory for this test run.
      --version             display pytest lib version and import information.
      -h, --help            show help message and configuration info
      -p name               early-load given plugin (multi-allowed). To avoid
                            loading of plugins, use the `no:` prefix, e.g.
                            `no:doctest`.
      --trace-config        trace considerations of conftest.py files.
      --debug               store internal tracing debug information in
                            'pytestdebug.log'.
      -o [OVERRIDE_INI [OVERRIDE_INI ...]], --override-ini=[OVERRIDE_INI [OVERRIDE_I
    NI ...]]
                            override config option with option=value style, e.g.
                            `-o xfail_strict=True`.
      --assert=MODE         Control assertion debugging tools. 'plain' performs no
                            assertion debugging. 'rewrite' (the default) rewrites
                            assert statements in test modules on import to provide
                            assert expression information.
      --setup-only          only setup fixtures, do not execute tests.
      --setup-show          show setup of fixtures while executing tests.
      --setup-plan          show what fixtures and tests would be executed but
                            don't execute anything.

    pytest-warnings:
      -W PYTHONWARNINGS, --pythonwarnings=PYTHONWARNINGS
                            set which warnings to report, see -W option of python
                            itself.

    distributed and subprocess testing:
      -n numprocesses, --numprocesses=numprocesses
                            shortcut for '--dist=load --tx=NUM*popen', you can use
                            'auto' here for auto detection CPUs number on host
                            system
      --max-slave-restart=MAX_SLAVE_RESTART
                            maximum number of slaves that can be restarted when
                            crashed (set to zero to disable this feature)
      --dist=distmode       set mode for distributing tests to exec environments.
                            each: send each test to all available environments.
                            load: load balance by sending any pending test to any
                            available environment. loadscope: load balance by
                            sending pending groups of tests in the same scope to
                            any available environment. (default) no: run tests
                            inprocess, don't distribute.
      --tx=xspec            add a test execution environment. some examples: --tx
                            popen//python=python2.5 --tx socket=192.168.1.102:8888
                            --tx ssh=user@codespeak.net//chdir=testcache
      -d                    load-balance tests. shortcut for '--dist=load'
      --rsyncdir=DIR        add directory for rsyncing to remote tx nodes.
      --rsyncignore=GLOB    add expression for ignores when rsyncing to remote tx
                            nodes.
      --boxed               backward compatibility alias for pytest-forked
                            --forked
      -f, --looponfail      run tests in subprocess, wait for modified files and
                            re-run failing test set until all pass.

    Interrupt test run and dump stacks of all threads after a test times out:
      --timeout=TIMEOUT     Timeout in seconds before dumping the stacks. Default
                            is 0 which means no timeout.
      --timeout_method={signal,thread}
                            Depreacted, use --timeout-method
      --timeout-method={signal,thread}
                            Timeout mechanism to use. 'signal' uses SIGALRM if
                            available, 'thread' uses a timer thread. The default
                            is to use 'signal' and fall back to 'thread'.

    forked subprocess test execution:
      --forked              box each test run in a separate process (unix)

    coverage reporting with distributed testing support:
      --cov=[path]          measure coverage for filesystem path (multi-allowed)
      --cov-report=type     type of report to generate: term, term-missing,
                            annotate, html, xml (multi-allowed). term, term-
                            missing may be followed by ":skip-covered". annotate,
                            html and xml may be followed by ":DEST" where DEST
                            specifies the output location. Use --cov-report= to
                            not generate any output.
      --cov-config=path     config file for coverage, default: .coveragerc
      --no-cov-on-fail      do not report coverage if test run fails, default:
                            False
      --no-cov              Disable coverage report completely (useful for
                            debuggers) default: False
      --cov-fail-under=MIN  Fail if the total coverage is less than MIN.
      --cov-append          do not delete coverage but append to current, default:
                            False
      --cov-branch          Enable branch coverage.

    Hypothesis:
      --hypothesis-profile=HYPOTHESIS_PROFILE
                            Load in a registered hypothesis.settings profile
      --hypothesis-show-statistics
                            Configure when statistics are printed
      --hypothesis-seed=HYPOTHESIS_SEED
                            Set a seed to use for all Hypothesis tests


    [pytest] ini-options in the first pytest.ini|tox.ini|setup.cfg file found:

      markers (linelist)       markers for test functions
      norecursedirs (args)     directory patterns to avoid for recursion
      testpaths (args)         directories to search for tests when no files or dire

      usefixtures (args)       list of default fixtures to be used with this project

      python_files (args)      glob-style file patterns for Python test module disco

      python_classes (args)    prefixes or glob names for Python test class discover

      python_functions (args)  prefixes or glob names for Python test function and m

      xfail_strict (bool)      default for the strict parameter of xfail markers whe

      junit_suite_name (string) Test suite name for JUnit report
      doctest_optionflags (args) option flags for doctests
      doctest_encoding (string) encoding used for doctest files
      cache_dir (string)       cache directory path.
      filterwarnings (linelist) Each line specifies a pattern for warnings.filterwar

      addopts (args)           extra command line options
      minversion (string)      minimally required pytest version
      rsyncdirs (pathlist)     list of (relative) paths to be rsynced for remote dis

      rsyncignore (pathlist)   list of (relative) glob-style paths to be ignored for

      looponfailroots (pathlist) directories to check for changes
      timeout (string)         Timeout in seconds before dumping the stacks.  Defaul

      timeout_method (string)  Timeout mechanism to use.  'signal' uses SIGALRM if a

      flakes-ignore (linelist) each line specifies a glob pattern and whitespace sep

      pep8ignore (linelist)    each line specifies a glob pattern and whitespace sep

      pep8maxlinelength (string) max. line length (default: 79)

    environment variables:
      PYTEST_ADDOPTS           extra command line options
      PYTEST_PLUGINS           comma-separated plugins to load during startup
      PYTEST_DEBUG             set to enable debug tracing of pytest's internals


    to see available markers type: pytest --markers
    to see available fixtures type: pytest --fixtures
    (shown according to specified file_or_dir or current dir if not specified)
    """

    import pytest
    pytest.main(['--pyargs', 'nvector'] + list(options))
