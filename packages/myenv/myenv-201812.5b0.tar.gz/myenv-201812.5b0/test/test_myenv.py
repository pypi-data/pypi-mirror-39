import os
import myenv
import pathlib as pl
import typing as typ


# dbenv_cls and testenv_cls are declared to avoid PytestWarning:
#   cannot collect test class 'TestEnv' because it has a __init__ constructor


def dbenv_cls():
    class DBEnv(myenv.BaseEnv):

        _environ_prefix = "MYAPP_DB_"

        host     : str = "127.0.0.1"
        port     : int = 5432
        name     : str = "app_db_v1"
        user     : str = "app_user"
        password : str
        read_only: bool    = True
        ddl      : pl.Path = (pl.Path(".") / "create_tables.sql")

        @property
        def url(self) -> str:
            db = self
            return f"postgres://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}"

    return DBEnv


def testenv_cls():
    class TestEnv(myenv.BaseEnv):

        str_val_wo_default  : str
        str_val             : str = "foo"
        int_val_wo_default  : int
        int_val             : int = 123
        bool_val_wo_default : bool
        bool_val            : bool = True
        float_val_wo_default: float
        float_val           : float = 12.34
        strs_val_wo_default : typ.List[str]
        strs_val            : typ.List[str] = ['bar']
        path_val_wo_default : pl.Path
        path_val            : pl.Path = pl.Path("file.txt")
        paths_val_wo_default: typ.List[pl.Path]
        paths_val           : typ.List[pl.Path] = [
            pl.Path("file1.txt"),
            pl.Path("file2.txt"),
            pl.Path("file3.txt"),
        ]

    return TestEnv


def test_parse():
    environ = {
        'MYAPP_DB_HOST'     : "1.2.3.4",
        'MYAPP_DB_PORT'     : "1234",
        'MYAPP_DB_NAME'     : "app_db_v2",
        'MYAPP_DB_USER'     : "new_user",
        'MYAPP_DB_PASSWORD' : "secret",
        'MYAPP_DB_READ_ONLY': "0",
        'MYAPP_DB_DDL'      : "~/mkdb.sql",
    }
    environ_before = str(os.environ)

    dbenv = dbenv_cls()(environ=environ)

    environ_after = str(os.environ)
    assert environ_before == environ_after

    assert set(dbenv._varnames()) == set(environ.keys())

    assert dbenv.host     == "1.2.3.4"
    assert dbenv.port     == 1234
    assert dbenv.name     == "app_db_v2"
    assert dbenv.user     == "new_user"
    assert dbenv.password == "secret"
    assert dbenv.read_only is False
    assert isinstance(dbenv.ddl, pl.Path)
    assert str(dbenv.ddl).endswith("mkdb.sql")

    assert dbenv.url == "postgres://new_user:secret@1.2.3.4:1234/app_db_v2"

    attrnames = [attrname for attrname in dbenv.__annotations__ if not attrname.startswith("_")]
    assert len(attrnames) == 7


def test_defaults():
    environ_before = str(os.environ)

    dbenv = dbenv_cls()(environ={'MYAPP_DB_PASSWORD': "secret"})

    environ_after = str(os.environ)
    assert environ_before == environ_after

    assert dbenv.host     == "127.0.0.1"
    assert dbenv.port     == 5432
    assert dbenv.name     == "app_db_v1"
    assert dbenv.user     == "app_user"
    assert dbenv.password == "secret"
    assert dbenv.read_only is True

    assert isinstance(dbenv.ddl, pl.Path)
    assert str(dbenv.ddl).endswith("create_tables.sql")

    attrnames = [attrname for attrname in dbenv.__annotations__ if not attrname.startswith("_")]
    assert len(attrnames) == 7


def test_errors():
    try:
        dbenv = testenv_cls()(environ={})
        assert False
    except KeyError as err:
        assert "STR_VAL_WO_DEFAULT" in str(err)

    try:
        dbenv = testenv_cls()(environ={'STR_VAL_WO_DEFAULT': "bar"})
        assert False
    except KeyError as err:
        assert "INT_VAL_WO_DEFAULT" in str(err)

    good_environ = {
        'STR_VAL_WO_DEFAULT'  : "bar",
        'INT_VAL_WO_DEFAULT'  : "123",
        'BOOL_VAL_WO_DEFAULT' : "TRUE",
        'FLOAT_VAL_WO_DEFAULT': "123.456",
        'STRS_VAL_WO_DEFAULT' : "baz:buz",
        'PATH_VAL_WO_DEFAULT' : "fileA.txt",
        'PATHS_VAL_WO_DEFAULT': "fileA.txt:fileB.txt:fileC.txt",
    }
    dbenv = testenv_cls()(environ=good_environ)

    assert dbenv.str_val             == "foo"
    assert dbenv.str_val_wo_default  == "bar"
    assert dbenv.strs_val            == ['bar']
    assert dbenv.strs_val_wo_default == ["baz", 'buz']

    try:
        bad_environ = good_environ.copy()
        bad_environ['INT_VAL'] = "abc"
        dbenv = testenv_cls()(environ=bad_environ)
        assert False
    except ValueError as err:
        assert 'INT_VAL' in str(err)
        assert 'abc' in str(err)
        assert "TestEnv.int_val" in str(err)

    try:
        bad_environ = good_environ.copy()
        bad_environ['INT_VAL'] = "123af"
        dbenv = testenv_cls()(environ=bad_environ)
        assert False
    except ValueError as err:
        assert 'INT_VAL' in str(err)
        assert '123af' in str(err)
        assert "TestEnv.int_val" in str(err)

    try:
        bad_environ = good_environ.copy()
        bad_environ['BOOL_VAL'] = "yes"
        dbenv = testenv_cls()(environ=bad_environ)
        assert False
    except ValueError as err:
        assert 'BOOL_VAL' in str(err)
        assert 'yes' in str(err)
        assert "TestEnv.bool_val" in str(err)

    try:
        bad_environ = good_environ.copy()
        bad_environ['FLOAT_VAL'] = "abc.23"
        dbenv = testenv_cls()(environ=bad_environ)
        assert False
    except ValueError as err:
        assert 'FLOAT_VAL' in str(err)
        assert "abc.23" in str(err)
        assert "TestEnv.float_val" in str(err)
