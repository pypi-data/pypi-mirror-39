
import pytest
import os


def pytest_addoption(parser):
    parser.addoption(
        "--show_plots", action="store_true", default=False, help="Display plots"
    )


@pytest.fixture
def show_plots(request):
    return request.config.getoption("--show_plots")


@pytest.fixture
def datadir(tmpdir, request):
    """
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    """
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    return test_dir
