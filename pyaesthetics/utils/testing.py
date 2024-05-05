import pathlib


class PyaestheticsTestCase(object):
    PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
    MODULE_ROOT = PROJECT_ROOT / "pyaesthetics"
    TEST_ROOT = PROJECT_ROOT / "tests"
    FIXTURES_ROOT = PROJECT_ROOT / "test_fixtures"
