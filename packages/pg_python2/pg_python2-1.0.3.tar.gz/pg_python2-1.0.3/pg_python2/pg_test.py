import pg_python, pg_validate
import unittest

COL_1 = "col1"
COL_2 = "col2"
COL_3 = "col3"
COL_4 = "col4"
COL_5 = "int_value"
UPDATE = "update"
test_table = "pg_python_test"


class TestTests(unittest.TestCase):

    def test_update(self):
        pg_python.pg_server("test_db", "postgres", "@pgtest", "localhost", False)
        create_rows()
        dict_lst =[
            {COL_1:'title1', UPDATE:'updated_name1'},
            {COL_1: 'title2', UPDATE: "update'd_name2"}
        ]
        pg_python.update_multiple(test_table,COL_4,[COL_1],dict_lst)
        title1 = pg_python.read(test_table,[COL_4],{COL_1:'title1'})
        title2 = pg_python.read(test_table, [COL_4], {COL_1: 'title2'})
        self.assertEqual(title1[0][COL_4],'updated_name1')
        self.assertEqual(title2[0][COL_4], "update'd_name2")

        clear_table()

    def test_single_update(self):
        pg_python.pg_server("test_db", "postgres", "@pgtest", "localhost", False)
        create_rows()
        pg_python.update(test_table,{COL_4:'updated_name1'},{COL_1:'title1%'},clause='ilike')
        title1 = pg_python.read(test_table,[COL_4],{COL_1:'title15'})
        self.assertEqual(title1[0][COL_4],'updated_name1')
        clear_table()

    def test_multiple_insert(self):
        pg_python.pg_server("test_db", "postgres", "@pgtest", "localhost", False)
        column_to_insert = [COL_1, COL_3]
        insert_dict_list = [
            {COL_1: "insert1", COL_3: 1},
            {COL_3: 2, COL_1: "insert2"},
            {COL_1: "insert3", COL_3: 3}
        ]
        pg_python.insert_multiple(test_table,column_to_insert,insert_dict_list)
        val1 = pg_python.read(test_table,[COL_1],{COL_3:1})
        val2 = pg_python.read(test_table, [COL_1], {COL_3: 2})
        val3 = pg_python.read(test_table, [COL_1], {COL_3: 3})
        values = [val1[0][COL_1],val2[0][COL_1],val3[0][COL_1] ]
        self.assertEqual(values,["insert1","insert2","insert3"])
        clear_table()

    def test_update_raw(self):
        pg_python.pg_server("test_db", "postgres", "@pgtest", "localhost", False)
        create_rows()
        updates = pg_python.update_raw("update "+ test_table + " set " + COL_4 + "= 'updated_name1' where " + COL_1 + " ilike 'title1%'" )
        title1 = pg_python.read(test_table, [COL_4], {COL_1: 'title15'})
        self.assertEqual(title1[0][COL_4], 'updated_name1')
        self.assertEqual(updates, 2)
        print("UPdate raw done")
        clear_table()

    def test_read_in(self):
        pg_python.pg_server("test_db", "postgres", "@pgtest", "localhost", False)
        create_rows()
        values = ['title15','title1','title2','title3']
        rows = pg_python.read(test_table, [COL_1], {COL_1: values}, clause=" in ")
        read_values = []
        for row in rows:
            read_values.append(row.get(COL_1))
        self.assertEqual(sorted(read_values), sorted(values))
        print("Read IN done")
        clear_table()

    def test_read_simple(self):
        pg_python.pg_server("test_db", "postgres", "@pgtest", "localhost", False)
        create_rows()
        rows = pg_python.read(test_table, [COL_1], {COL_2: 'read'})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][COL_1], 'title1')
        print("Read simple done")
        clear_table()

    def test_read_greater_than(self):
        pg_python.pg_server("test_db", "postgres", "@pgtest", "localhost", False)
        create_rows()
        rows = pg_python.read(test_table, [COL_1], {COL_5 + " >": 10})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][COL_1], 'title6')
        print("Read greater than done")
        clear_table()

    def phone_validation_test(self):
        self.assertEqual(pg_validate.is_phone_no_valid("+91 7349250104"), (True, "correct number"))
        self.assertEqual(pg_validate.is_phone_no_valid("+91 9090909090"), (False, "phone number appears wrong"))
        self.assertEqual(pg_validate.is_phone_no_valid("+91 7891237890"), (False, "phone number appears wrong"))

    def name_validation_test(self):
        self.assertEqual(pg_validate.is_name_valid("gaurav"), True)
        self.assertEqual(pg_validate.is_name_valid("a"), False)
        self.assertEqual(pg_validate.is_name_valid("aaaaabbbbb"), False)

def create_rows():
    pg_python.write(test_table, {COL_1: "title1", COL_2: "read", COL_3: 76, COL_4: "reeer"})
    pg_python.write(test_table, {COL_1: "title2", COL_2: "read2", COL_3: 77, COL_4: "reeer"})
    pg_python.write(test_table, {COL_1: "title3", COL_2: "read3", COL_3: 77, COL_4: "reeer"})
    pg_python.write(test_table, {COL_1: "title4", COL_2: "read4", COL_3: 77, COL_4: "reeer"})
    pg_python.write(test_table, {COL_1: "title15", COL_2: "read5", COL_3: 77, COL_4: "reeer"})
    pg_python.write(test_table, {COL_1: "title6", COL_2: "read6", COL_3: 77, COL_4: "reeer", COL_5: 20})

def clear_table():
    pg_python.write_raw("Delete from %s"%(test_table), None)

