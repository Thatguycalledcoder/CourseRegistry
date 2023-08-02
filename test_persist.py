import unittest
import psycopg2
from processor import persist


class PersistDataTest(unittest.TestCase):
    def test_read_from_pg(self):
        db_object = persist.PersistData()
        courses = db_object.read_from_pg("futurexschema.futurex_course_catalog")
        self.assertTrue(type(courses[0][1]) == type("test"))

    def test_read_from_pg_2(self):
        db_object = persist.PersistData()

        with self.assertRaises(psycopg2.errors.UndefinedTable):
            db_object.read_from_pg("futurexschema.nice_table")


if __name__ == '__main__':
    unittest.main()
