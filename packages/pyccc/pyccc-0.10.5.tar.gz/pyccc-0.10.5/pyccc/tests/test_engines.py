# -*- coding: utf-8 -*-
"""
Basic test battery for regular and python jobs on all underlying engines

This can be used to test external engines (in a hacky, somewhat brittle way right now):

```python
import pytest
from pyccc.tests import engine_fixtures

@pytest.fixture(scope='module')
def my_engine():
    return MyEngine()

engine_fixtures.fixture_types['engine'] = ['my_engine']
from pyccc.tests.test_engines import *  # imports all the tests
```

A less hacky way to via a parameterized test strategy similar to testscenarios:
https://docs.pytest.org/en/latest/example/parametrize.html#a-quick-port-of-testscenarios
"""
import os
import sys
import pytest
import pyccc
from .engine_fixtures import *
from . import function_tests

from future.utils import PY2


PYVERSION = '%s.%s' % (sys.version_info.major, sys.version_info.minor)
PYIMAGE = 'python:%s-slim' % PYVERSION
THISDIR = os.path.dirname(__file__)

########################
# Python test objects  #
########################

def _raise_valueerror(msg):
    raise ValueError(msg)


###################
# Tests           #
###################
@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_hello_world(fixture, request):
    engine = request.getfixturevalue(fixture)
    job = engine.launch('alpine', 'echo hello world')
    print(job.rundata)
    job.wait()
    assert job.stdout.strip() == 'hello world'


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_job_status(fixture, request):
    engine = request.getfixturevalue(fixture)
    job = engine.launch('alpine', 'sleep 3', submit=False)
    assert job.status.lower() == 'unsubmitted'
    job.submit()
    print(job.rundata)
    assert job.status.lower() in ('queued', 'running', 'downloading')
    assert not job.stopped
    job.wait()
    assert job.status.lower() == 'finished'
    assert job.stopped


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_file_glob(fixture, request):
    engine = request.getfixturevalue(fixture)
    job = engine.launch('alpine', 'touch a.txt b c d.txt e.gif')
    print(job.rundata)
    job.wait()

    assert set(job.get_output().keys()) <= set('a.txt b c d.txt e.gif'.split())
    assert set(job.glob_output('*.txt').keys()) == set('a.txt d.txt'.split())


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_output_dump(fixture, request, tmpdir):
    from pathlib import Path
    import shutil

    engine = request.getfixturevalue(fixture)
    dirpath = Path(str(tmpdir))
    subdir = dirpath / 'test'
    expected_exception = OSError if PY2 else FileExistsError
    expected_files = set('a.txt b c d.txt e.gif dirA/A dirA/B dirB/C'.split())

    job = engine.launch('alpine',
                        'mkdir dirA dirB && touch a.txt b c d.txt e.gif dirA/A dirA/B dirB/C')
    print(job.rundata)
    job.wait()
    job.dump_all_outputs(str(dirpath), exist_ok=True, update_references=False)
    _verify_output_dump(dirpath, expected_files, job, outputs_updated=False)

    # test that exception raised if directory exists and exist_ok is False
    subdir.mkdir()
    with pytest.raises(expected_exception):
        job.dump_all_outputs(str(subdir), exist_ok=False)

    # test that directory created if it doesn't exist
    shutil.rmtree(str(subdir))
    job.dump_all_outputs(str(subdir), exist_ok=False, update_references=True)
    assert subdir.is_dir()
    _verify_output_dump(subdir, expected_files, job, outputs_updated=True)


def _verify_output_dump(dirpath, expected_files, job, outputs_updated):
    # test that output files were dumped
    found_files = set(str(p.relative_to(dirpath)) for p in dirpath.glob('**/*')
                      if not p.is_dir())
    assert found_files == expected_files

    # Make sure that references either are or are NOT pointing to the newly dumped outputs
    for ff in found_files:
        assert ff in job.get_output()
        ref = job.get_output(ff)
        if outputs_updated:
            assert (getattr(ref, 'localpath')
                    and os.path.normpath(ref.localpath) == os.path.normpath(str(dirpath/ff)))
        else:
            assert (not getattr(ref, 'localpath', None)
                    or os.path.normpath(ref.localpath) != os.path.normpath(str(dirpath/ff)))


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_output_dump_abspaths(fixture, request, tmpdir):
    from pathlib import Path
    engine = request.getfixturevalue(fixture)
    if not engine.ABSPATHS:
        pytest.skip("Engine %s does not support absolute paths" % str(fixture))

    p = Path(str(tmpdir))
    job = engine.launch('alpine',
                        'mkdir -p /opt/a && echo "hello world" > /opt/a/f')
    job.wait()

    # where we'll dump the outputs
    abstmp = p / 'absdump'
    reltmp = p / 'reldump'

    # only changed files are relative to root, so this directory should be empty
    job.dump_all_outputs(str(reltmp), update_references=False)
    assert len(list(reltmp.glob('**/*'))) == 0

    # the changed absolute-path files should be staged into the requests 'fsroot' directory
    job.dump_all_outputs(str(abstmp), abspaths='fsroot')
    outputs = list((abstmp/'fsroot').glob('**/*'))
    assert len(outputs) == 3
    optdir = abstmp / 'fsroot' / 'opt'
    assert optdir.is_dir()
    assert (optdir / 'a').is_dir()
    assert (optdir / 'a' / 'f').is_file()


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_input_ouput_files(fixture, request):
    engine = request.getfixturevalue(fixture)
    job = engine.launch(image='alpine',
                        command='cat a.txt b.txt > out.txt',
                        inputs={'a.txt': 'a',
                                'b.txt': pyccc.StringContainer('b')})
    print(job.rundata)
    job.wait()
    assert job.get_output('out.txt').read().strip() == 'ab'


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_sleep_raises_jobstillrunning(fixture, request):
    engine = request.getfixturevalue(fixture)
    job = engine.launch('alpine', 'sleep 5; echo done')
    print(job.rundata)
    with pytest.raises(pyccc.JobStillRunning):
        job.stdout
    job.wait()
    assert job.stdout.strip() == 'done'


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_python_function(fixture, request):
    engine = request.getfixturevalue(fixture)
    pycall = pyccc.PythonCall(function_tests.fn, 5)
    job = engine.launch(PYIMAGE, pycall, interpreter=PYVERSION)
    print(job.rundata)
    job.wait()
    assert job.result == 6


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_python_instance_method(fixture, request):
    engine = request.getfixturevalue(fixture)
    obj = function_tests.Cls()
    pycall = pyccc.PythonCall(obj.increment, by=2)
    job = engine.launch(PYIMAGE, pycall, interpreter=PYVERSION)
    print(job.rundata)
    job.wait()

    assert job.result == 2
    assert job.updated_object.x == 2


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_python_reraises_exception(fixture, request):
    engine = request.getfixturevalue(fixture)
    pycall = pyccc.PythonCall(_raise_valueerror, 'this is my message')
    job = engine.launch(PYIMAGE, pycall, interpreter=PYVERSION)
    print(job.rundata)
    job.wait()

    with pytest.raises(ValueError):
        job.result


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_builtin_imethod(fixture, request):
    engine = request.getfixturevalue(fixture)
    mylist = [3, 2, 1]
    fn = pyccc.PythonCall(mylist.sort)
    job = engine.launch(image=PYIMAGE, command=fn, interpreter=PYVERSION)
    print(job.rundata)
    job.wait()

    assert job.result is None  # since sort doesn't return anything
    assert job.updated_object == [1, 2, 3]


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_builtin_function(fixture, request):
    mylist = [3, 2, 1]
    result = _runcall(fixture, request, sorted, mylist)
    assert result == [1,2,3]


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_function_with_closure_var(fixture, request):
    result = _runcall(fixture, request, function_tests.fn_withvar, 5.0)
    assert result == 8.0


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_function_with_closure_func(fixture, request):
    result = _runcall(fixture, request, function_tests.fn_withfunc, [1, 2], [3, 4])
    assert result == [1,2,3,4]


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_function_with_closure_mod(fixture, request):
    od = _runcall(fixture, request, function_tests.fn_withmod, [('a', 'b'), ('c', 'd')])
    assert od.__class__.__name__ == 'OrderedDict'
    assert list(od.keys()) == ['a', 'c']
    assert list(od.values()) == ['b', 'd']


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_function_with_renamed_closure_mod(fixture, request):
    if sys.version_info.major == 3:
        pytest.xfail("This is either impossible or a bug with Python 3")

    result = _runcall(fixture, request, function_tests.fn_with_renamed_mod)
    assert len(result) == 10
    for x in result:
        assert 0.0 <= x <= 1.0


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_function_with_renamed_module_var(fixture, request):
    result = _runcall(fixture, request, function_tests.fn_with_renamed_attr, 'a')
    assert not result


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_bash_exitcode(fixture, request):
    engine = request.getfixturevalue(fixture)
    job = pyccc.Job(image='python:2.7-slim',
                    command='sleep 5 && exit 35',
                    engine=engine,
                    submit=True)
    print(job.rundata)
    with pytest.raises(pyccc.JobStillRunning):
        job.exitcode
    job.wait()
    assert job.wait() == 35
    assert job.exitcode == 35


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_python_exitcode(fixture, request):
    engine = request.getfixturevalue(fixture)
    fn = pyccc.PythonCall(function_tests.sleep_then_exit_38)
    job = engine.launch(image=PYIMAGE, command=fn, interpreter=PYVERSION)
    print(job.rundata)

    with pytest.raises(pyccc.JobStillRunning):
        job.exitcode

    job.wait()
    assert job.wait() == 38
    assert job.exitcode == 38


class MyRefObj(object):
    _PERSIST_REFERENCES = True

    def identity(self):
        return self

    def tagme(self):
        self.tag = 'mytag'
        return self


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_persistence_assumptions(fixture, request):
    # Object references are not persisted across function calls by default.
    # This is the control experiment prior to the following tests
    testobj = MyRefObj()
    testobj.o = MyRefObj()
    testobj.o.o = testobj

    engine = request.getfixturevalue(fixture)
    pycall = pyccc.PythonCall(testobj.identity)

    # First the control experiment - references are NOT persisted
    job = engine.launch(PYIMAGE, pycall, interpreter=PYVERSION)
    print(job.rundata)
    job.wait()
    result = job.result
    assert result is not testobj
    assert result.o is not testobj.o
    assert result.o.o is result


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_persist_references_flag(fixture, request):
    testobj = MyRefObj()
    testobj.o = MyRefObj()
    testobj.o.o = testobj

    engine = request.getfixturevalue(fixture)
    pycall = pyccc.PythonCall(testobj.identity)

    # With the right flag, references ARE now persisted
    job = engine.launch(PYIMAGE, pycall, interpreter=PYVERSION, persist_references=True)
    print(job.rundata)
    job.wait()
    result = job.result
    assert result is testobj
    assert result.o is testobj.o
    assert result.o.o is result


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_persistent_and_nonpersistent_mixture(fixture, request):
    # References only persisted in objects that request it
    testobj = MyRefObj()
    testobj.o = MyRefObj()
    testobj.o.o = testobj
    testobj.should_persist = MyRefObj()
    testobj._PERSIST_REFERENCES = False
    testobj.o._PERSIST_REFERENCES = False

    engine = request.getfixturevalue(fixture)
    pycall = pyccc.PythonCall(testobj.identity)

    job = engine.launch(PYIMAGE, pycall, interpreter=PYVERSION, persist_references=True)
    print(job.rundata)
    job.wait()
    result = job.result
    assert result is not testobj
    assert result.o is not testobj.o
    assert result.o.o is result
    assert result.should_persist is testobj.should_persist


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_callback(fixture, request):
    def _callback(job):
        return job.get_output('out.txt').read().strip()

    engine = request.getfixturevalue(fixture)
    job = engine.launch(image=PYIMAGE,
                        command='echo hello world > out.txt',
                        when_finished=_callback)
    print(job.rundata)
    job.wait()

    assert job.result == 'hello world'


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_unicode_stdout_and_return(fixture, request):
    engine = request.getfixturevalue(fixture)
    fn = pyccc.PythonCall(function_tests.fn_prints_unicode)
    job = engine.launch(image=PYIMAGE, command=fn, interpreter=PYVERSION)
    print(job.rundata)
    job.wait()
    assert job.result == u'¶'
    assert job.stdout.strip() == u'Å'
    assert job.stderr.strip() == u'µ'


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_callback_after_python_job(fixture, request):
    def _callback(job):
        return job.function_result - 1

    fn = pyccc.PythonCall(function_tests.fn, 3.0)
    engine = request.getfixturevalue(fixture)
    job = engine.launch(image=PYIMAGE, command=fn, interpreter=PYVERSION, when_finished=_callback)
    print(job.rundata)
    job.wait()

    assert job.function_result == 4.0
    assert job.result == 3.0


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_job_with_callback_and_references(fixture, request):
    def _callback(job):
        return job.function_result.obj

    testobj = MyRefObj()
    testobj.obj = MyRefObj()

    fn = pyccc.PythonCall(testobj.tagme)
    engine = request.getfixturevalue(fixture)
    job = engine.launch(image=PYIMAGE, command=fn,
                        interpreter=PYVERSION, when_finished=_callback, persist_references=True)
    print(job.rundata)
    job.wait()

    assert job.function_result is testobj
    assert job.result is testobj.obj
    assert job.function_result.obj is testobj.obj

    # A surprising result but correct behavior - because we replace the object with its reference,
    # it is unchanged.
    assert not hasattr(job.result, 'tag')
    assert not hasattr(testobj, 'tag')
    assert hasattr(job.updated_object, 'tag')


def _runcall(fixture, request, function, *args, **kwargs):
    engine = request.getfixturevalue(fixture)
    fn = pyccc.PythonCall(function, *args, **kwargs)
    job = engine.launch(image=PYIMAGE, command=fn, interpreter=PYVERSION)
    print(job.rundata)
    job.wait()
    return job.result


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_clean_working_dir(fixture, request):
    """ Because of some weird results that seemed to indicate the wrong run dir
    """
    engine = request.getfixturevalue(fixture)
    job = engine.launch(image='alpine', command='ls')
    print(job.rundata)
    job.wait()
    assert job.stdout.strip() == ''


class no_context(): 
    """context manager that does nothing -- useful if we need to conditionally apply a context
    """
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        return False


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_abspath_input_files(fixture, request):
    engine = request.getfixturevalue(fixture)
    with no_context() if engine.ABSPATHS else pytest.raises(pyccc.PathError):
        job = engine.launch(image='alpine', command='cat /opt/a',
                            inputs={'/opt/a': pyccc.LocalFile(os.path.join(THISDIR, 'data', 'a'))})
    if engine.ABSPATHS:
        print(job.rundata)
        job.wait()
        assert job.exitcode == 0
        assert job.stdout.strip() == 'a'


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_directory_input(fixture, request):
    engine = request.getfixturevalue(fixture)

    job = engine.launch(image='alpine', command='cat data/a data/b',
                        inputs={'data':
                                    pyccc.LocalDirectoryReference(os.path.join(THISDIR, 'data'))})
    print(job.rundata)
    job.wait()
    assert job.exitcode == 0
    assert job.stdout.strip() == 'a\nb'


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_deleted_file_is_not_returned(fixture, request):
    engine = request.getfixturevalue(fixture)
    job = engine.launch(image='alpine', command='mv a b',
                        inputs={'a': pyccc.LocalFile(os.path.join(THISDIR, 'data', 'a'))})
    job.wait()
    outputs = job.get_output()
    assert 'a' not in outputs
    assert 'b' in outputs


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_passing_files_between_jobs(fixture, request):
    engine = request.getfixturevalue(fixture)

    job1 = engine.launch(image='alpine', command='echo hello > world')
    print('job1:', job1.rundata)
    job1.wait()
    assert job1.exitcode == 0

    job2 = engine.launch(image='alpine', command='cat helloworld',
                         inputs={'helloworld': job1.get_output('world')})
    print('job2:', job2.rundata)
    job2.wait()
    assert job2.exitcode == 0
    assert job2.stdout.strip() == 'hello'


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_job_env_vars(fixture, request):
    engine = request.getfixturevalue(fixture)

    job = engine.launch(image='alpine',
                        command='echo ${AA} ${BB}',
                        env={'AA': 'hello', 'BB':'world'})
    print(job.rundata)
    job.wait()
    assert job.exitcode == 0
    assert job.stdout.strip() == 'hello world'


@pytest.mark.parametrize('fixture', fixture_types['engine'])
def test_get_job(fixture, request):
    engine = request.getfixturevalue(fixture)
    job = engine.launch(image='alpine',
                        command='sleep 1 && echo nice nap')

    try:
        newjob = engine.get_job(job.jobid)
    except NotImplementedError:
        pytest.skip('get_job raised NotImplementedError for %s' % fixture)

    assert job.jobid == newjob.jobid
    job.wait()
    assert newjob.status == job.status

    assert newjob.stdout == job.stdout
    assert newjob.stderr == job.stderr

