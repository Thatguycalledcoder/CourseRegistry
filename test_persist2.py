
import pytest
from processor import persist
import psycopg2


def test_read_from_pg():
    db_object = persist.PersistData()
    courses = db_object.read_from_pg("futurexschema.futurex_course_catalog")
    assert isinstance(courses[0][1], str)


def test_read_from_pg_2():
    db_object = persist.PersistData()

    with pytest.raises(psycopg2.errors.UndefinedTable):
        db_object.read_from_pg("futurexschema.nice_table")