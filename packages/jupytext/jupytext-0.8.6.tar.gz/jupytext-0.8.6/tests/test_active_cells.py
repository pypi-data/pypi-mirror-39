import pytest
from testfixtures import compare
import jupytext
from .utils import skip_if_dict_is_not_ordered

jupytext.header.INSERT_AND_CHECK_VERSION_NUMBER = False

ACTIVE_ALL = {'.py': """# + {"active": "ipynb,py,R,Rmd"}
# This cell is active in all extensions
""",
              '.Rmd': """```{python active="ipynb,py,R,Rmd"}
# This cell is active in all extensions
```
""",
              '.R': """#+ active="ipynb,py,R,Rmd"
# This cell is active in all extensions
""",
              '.ipynb': {'cell_type': 'code',
                         'source': '# This cell is active in all extensions',
                         'metadata': {'active': 'ipynb,py,R,Rmd'},
                         'execution_count': None,
                         'outputs': []}}


@pytest.mark.parametrize('ext', ['.Rmd', '.py', '.R'])
def test_active_all(ext):
    nb = jupytext.reads(ACTIVE_ALL[ext], ext=ext)
    assert len(nb.cells) == 1
    compare(nb.cells[0], ACTIVE_ALL['.ipynb'])
    compare(ACTIVE_ALL[ext], jupytext.writes(nb, ext=ext))


ACTIVE_IPYNB = {'.py': """# + {"active": "ipynb"}
# # This cell is active only in ipynb
# %matplotlib inline
""",
                '.Rmd': """```{python active="ipynb", eval=FALSE}
# This cell is active only in ipynb
%matplotlib inline
```
""",
                '.R': """#+ language="python", active="ipynb", eval=FALSE
# # This cell is active only in ipynb
# %matplotlib inline
""",
                '.ipynb': {'cell_type': 'code',
                           'source': '# This cell is active only in ipynb\n'
                                     '%matplotlib inline',
                           'metadata': {'active': 'ipynb'},
                           'execution_count': None,
                           'outputs': []}}


@skip_if_dict_is_not_ordered
@pytest.mark.parametrize('ext', ['.Rmd', '.py', '.R'])
def test_active_ipynb(ext):
    nb = jupytext.reads(ACTIVE_IPYNB[ext], ext=ext)
    assert len(nb.cells) == 1
    compare(nb.cells[0], ACTIVE_IPYNB['.ipynb'])
    if ext != '.R':
        compare(ACTIVE_IPYNB[ext], jupytext.writes(nb, ext=ext))


ACTIVE_PY_IPYNB = {'.py': """# + {"active": "ipynb,py"}
# This cell is active in py and ipynb extensions
""",
                   '.Rmd': """```{python active="ipynb,py", eval=FALSE}
# This cell is active in py and ipynb extensions
```
""",
                   '.R': """#+ language="python", active="ipynb,py", eval=FALSE
# # This cell is active in py and ipynb extensions
""",
                   '.ipynb': {'cell_type': 'code',
                              'source': '# This cell is active in py and '
                                        'ipynb extensions',
                              'metadata': {'active': 'ipynb,py'},
                              'execution_count': None,
                              'outputs': []}}


@skip_if_dict_is_not_ordered
@pytest.mark.parametrize('ext', ['.Rmd', '.py', '.R'])
def test_active_py_ipynb(ext):
    nb = jupytext.reads(ACTIVE_PY_IPYNB[ext], ext=ext)
    assert len(nb.cells) == 1
    compare(nb.cells[0], ACTIVE_PY_IPYNB['.ipynb'])
    if ext != '.R':
        compare(ACTIVE_PY_IPYNB[ext], jupytext.writes(nb, ext=ext))


ACTIVE_PY_R_IPYNB = {'.py': """# + {"active": "ipynb,py,R"}
# This cell is active in py, R and ipynb extensions
""",
                     '.Rmd': """```{python active="ipynb,py,R", eval=FALSE}
# This cell is active in py, R and ipynb extensions
```
""",
                     '.R': """#+ language="python", active="ipynb,py,R", eval=FALSE
# This cell is active in py, R and ipynb extensions
""",
                     '.ipynb': {'cell_type': 'code',
                                'source': '# This cell is active in py, R and '
                                          'ipynb extensions',
                                'metadata': {'active': 'ipynb,py,R'},
                                'execution_count': None,
                                'outputs': []}}


@skip_if_dict_is_not_ordered
@pytest.mark.parametrize('ext', ['.Rmd', '.py', '.R'])
def test_active_py_r_ipynb(ext):
    nb = jupytext.reads(ACTIVE_PY_R_IPYNB[ext], ext=ext)
    assert len(nb.cells) == 1
    compare(nb.cells[0], ACTIVE_PY_R_IPYNB['.ipynb'])
    if ext != '.R':
        compare(ACTIVE_PY_R_IPYNB[ext], jupytext.writes(nb, ext=ext))


ACTIVE_RMD = {'.py': """# + {"active": "Rmd"}
# # This cell is active in Rmd only
""",
              '.Rmd': """```{python active="Rmd"}
# This cell is active in Rmd only
```
""",
              '.R': """#+ language="python", active="Rmd", eval=FALSE
# # This cell is active in Rmd only
""",
              '.ipynb': {'cell_type': 'raw',
                         'source': '# This cell is active in Rmd only',
                         'metadata': {'active': 'Rmd'}}}


@skip_if_dict_is_not_ordered
@pytest.mark.parametrize('ext', ['.Rmd', '.py', '.R'])
def test_active_rmd(ext):
    nb = jupytext.reads(ACTIVE_RMD[ext], ext=ext)
    assert len(nb.cells) == 1
    compare(nb.cells[0], ACTIVE_RMD['.ipynb'])
    if ext != '.R':
        compare(ACTIVE_RMD[ext], jupytext.writes(nb, ext=ext))


ACTIVE_NOT_INCLUDE_RMD = {'.py': """# + {"hide_output": true, "active": "Rmd"}
# # This cell is active in Rmd only
""",
                          '.Rmd': """```{python include=FALSE, active="Rmd"}
# This cell is active in Rmd only
```
""",
                          '.R': """#+ include=FALSE, active="Rmd", eval=FALSE
# # This cell is active in Rmd only
""",
                          '.ipynb':
                              {'cell_type': 'raw',
                               'source': '# This cell is active in Rmd only',
                               'metadata': {'active': 'Rmd',
                                            'hide_output': True}}}


@skip_if_dict_is_not_ordered
@pytest.mark.parametrize('ext', ['.Rmd', '.py', '.R'])
def test_active_not_include_rmd(ext):
    nb = jupytext.reads(ACTIVE_NOT_INCLUDE_RMD[ext], ext=ext)
    assert len(nb.cells) == 1
    compare(nb.cells[0], ACTIVE_NOT_INCLUDE_RMD['.ipynb'])
    compare(ACTIVE_NOT_INCLUDE_RMD[ext], jupytext.writes(nb, ext=ext))
