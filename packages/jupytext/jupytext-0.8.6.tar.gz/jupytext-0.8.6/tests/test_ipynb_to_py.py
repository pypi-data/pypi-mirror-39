import nbformat
import pytest
import jupytext
from jupytext.compare import compare_notebooks
from .utils import list_notebooks

jupytext.header.INSERT_AND_CHECK_VERSION_NUMBER = False


@pytest.mark.parametrize('nb_file', list_notebooks('ipynb_py'))
def test_identity_source_write_read(nb_file):
    """
    Test that writing the notebook with jupytext, and read again,
    is the same as removing outputs
    :param file:
    :return:
    """

    with open(nb_file) as fp:
        nb1 = nbformat.read(fp, as_version=4)

    py = jupytext.writes(nb1, ext='.py')
    nb2 = jupytext.reads(py, ext='.py')

    compare_notebooks(nb1, nb2)
