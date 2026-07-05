import qsat


def test_version_is_string():
    #__version__ must exist and be a non-empty string
    assert isinstance(qsat.__version__, str)
    assert len(qsat.__version__) > 0