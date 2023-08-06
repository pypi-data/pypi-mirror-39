# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from shimbase.sqlite3impl import SQLite3Impl
from shimbase.dbimpl import DatabaseDataError, DatabaseIntegrityError

class TestSQLite3Impl(TestCase):
    """SQLite3Impl tests"""
    db = None

    @classmethod
    def setUpClass(cls):
        createName = './db/createdb.sql' 
        testDataName = './db/*_data.sql' 
        dbName = './db/test.db'
        os.system('cat {} | sqlite3 {}'.format(createName, dbName))
        os.system('cat {} | sqlite3 {}'.format(testDataName, dbName))
        cls.db = SQLite3Impl()
        cls.db.connect(dbName)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def setUp(self):
        TestSQLite3Impl.db.execute('pragma foreign_keys=0')

    def tearDown(self):
        pass

    def test_select(self):
        rows = TestSQLite3Impl.db.select('foo', {})    

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ( \
                'foo name TD', 'foo desc TD', 98))
        self.assertEqual(rows[1], ( \
                'foo name TD2', 'foo desc TD2', 99))

        rows = TestSQLite3Impl.db.select('bar', {'id' : 98})

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (98, 98, 2.3, 'X'))

        rows = TestSQLite3Impl.db.select(
                'foo', {'bar_id' : 98})

        self.assertEqual(len(rows), 1)
        self.assertEqual(
                rows[0], ('foo name TD', 'foo desc TD', 98))

    def test_select_Greater(self):
        rows = TestSQLite3Impl.db.select('foo', {'>bar_id' : 98})    

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ( \
                'foo name TD2', 'foo desc TD2', 99))

    def test_select_Less(self):
        rows = TestSQLite3Impl.db.select('foo', {'<bar_id' : 99})    

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ( \
                'foo name TD', 'foo desc TD', 98))

    def test_select_Between(self):
        rows = TestSQLite3Impl.db.select('foo', \
                {'>bar_id' : 97, '<bar_id' : 99})    

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ( \
                'foo name TD', 'foo desc TD', 98))

    def test_select_Not(self):
        rows = TestSQLite3Impl.db.select('foo', {'!bar_id' : 99})

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ( \
                'foo name TD', 'foo desc TD', 98))

    def test_select_Ordered(self):
        rows = TestSQLite3Impl.db.select('foo', {}, ('>bar_id',))    

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ( \
                'foo name TD2', 'foo desc TD2', 99))
        self.assertEqual(rows[1], ( \
                'foo name TD', 'foo desc TD', 98))

        TestSQLite3Impl.db.insert('bar', \
                {'id' : 1, 'heading' : 270, 'speed' : 33.3, 'signal' : 'A'})
        
        rows = TestSQLite3Impl.db.select('bar', {}, ('>id',))    
        print(rows)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], (99, 99, 2.4, 'Z'))
        self.assertEqual(rows[1], (98, 98, 2.3, 'X'))
        self.assertEqual(rows[2], (1, 270, 33.3, 'A'))

        rows = TestSQLite3Impl.db.select('bar', {}, ('heading',))    

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], (98, 98, 2.3, 'X'))
        self.assertEqual(rows[1], (99, 99, 2.4, 'Z'))
        self.assertEqual(rows[2], (1, 270, 33.3, 'A'))

        TestSQLite3Impl.db.insert('bar', \
                {'id' : 2, 'heading' : 270, 'speed' : 31.3, 'signal' : 'A'})

        rows = TestSQLite3Impl.db.select('bar', {}, ('<heading', 'speed'))    

        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0], (98, 98, 2.3, 'X'))
        self.assertEqual(rows[1], (99, 99, 2.4, 'Z'))
        self.assertEqual(rows[2], (2, 270, 31.3, 'A'))
        self.assertEqual(rows[3], (1, 270, 33.3, 'A'))

        rows = TestSQLite3Impl.db.select('bar', \
                {'heading' : 270, 'signal' : 'A'}, ('speed',))    
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (2, 270, 31.3, 'A'))
        self.assertEqual(rows[1], (1, 270, 33.3, 'A'))

        TestSQLite3Impl.db.rollback()

    def test_foreign_key(self):
        TestSQLite3Impl.db.execute('pragma foreign_keys=1')
        # bar id 100 should not exist
        with self.assertRaises(DatabaseIntegrityError) as cm:
            TestSQLite3Impl.db.insert('foo', {'name' : 'new foo', \
                    'desc' : 'what to do?', 'bar_id' : 100})
        TestSQLite3Impl.db.rollback()
        self.assertEqual(cm.exception.msg, 'FOREIGN KEY constraint failed')
 
    def test_select_NoRows(self):
        rows = TestSQLite3Impl.db.select('foo', {'name' : 'no foo'})
        self.assertEqual(len(rows), 0)

    def test_insert(self):
        TestSQLite3Impl.db.insert('foo', {'name' : 'my foo', \
                'desc' : 'and what a foo', 'bar_id' : 98})

        rows = TestSQLite3Impl.db.select('foo')

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[2], ('my foo', 'and what a foo', 98))

        TestSQLite3Impl.db.rollback()

    def test_transaction(self):
        TestSQLite3Impl.db.begin()

        TestSQLite3Impl.db.insert('foo', {'name' : 'my foo', \
                'desc' : 'super foo', 'bar_id' : 98})
        TestSQLite3Impl.db.insert('foo', {'name' : 'another foo', \
                'desc' : 'mega foo', 'bar_id' : 99})

        TestSQLite3Impl.db.commit()

        rows = TestSQLite3Impl.db.select('foo', {})    
        self.assertEqual(len(rows), 4)

        TestSQLite3Impl.db.insert('foo', {'name' : 'yet another foo', \
                'desc' : 'over the top foo', 'bar_id' : 99})

        rows = TestSQLite3Impl.db.select('foo', {})    
        self.assertEqual(len(rows), 5)

        TestSQLite3Impl.db.rollback()

        rows = TestSQLite3Impl.db.select('foo', {})    
        self.assertEqual(len(rows), 4)

    def test_transaction_Failure(self):
        TestSQLite3Impl.db.begin()

        TestSQLite3Impl.db.insert('foo', {'name' : 'really?', \
                'desc' : 'another one?', 'bar_id' : 98})
        try:
            TestSQLite3Impl.db.insert('foo', None)
        except:
            pass

        rows = TestSQLite3Impl.db.select('foo', {'name' : 'really?'})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ('really?', 'another one?', 98))

        TestSQLite3Impl.db.rollback()

        rows = TestSQLite3Impl.db.select('foo', {'name' : 'really?'})
        self.assertEqual(len(rows), 0)

    def test_insert_Error(self):
        with self.assertRaises(DatabaseDataError) as cm:
            TestSQLite3Impl.db.insert('foo', {})
        self.assertEqual(cm.exception.msg, 'No values provided for INSERT')

    def test_update(self):
        TestSQLite3Impl.db.update('bar', {'heading' : 180}, {'id' : 98})

        rows = TestSQLite3Impl.db.select('bar')

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (98, 180, 2.3, 'X'))

        TestSQLite3Impl.db.rollback()

    def test_update_Greater(self):
        TestSQLite3Impl.db.update('bar', {'heading' : 180}, {'>id' : 97})

        rows = TestSQLite3Impl.db.select('bar')

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (98, 180, 2.3, 'X'))
        self.assertEqual(rows[1], (99, 180, 2.4, 'Z'))

        TestSQLite3Impl.db.rollback()

    def test_update_Less(self):
        TestSQLite3Impl.db.update('bar', {'speed' : 22.2}, {'<heading' : 180})

        rows = TestSQLite3Impl.db.select('bar')

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (98, 98, 22.2, 'X'))
        self.assertEqual(rows[1], (99, 99, 22.2, 'Z'))

        TestSQLite3Impl.db.rollback()

    def test_update_Between(self):
        TestSQLite3Impl.db.update('bar', \
                {'signal' : 'C'}, {'>heading' : 97, '<heading' : 99})

        rows = TestSQLite3Impl.db.select('bar')

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (98, 98, 2.3, 'C'))
        self.assertEqual(rows[1], (99, 99, 2.4, 'Z'))

        TestSQLite3Impl.db.rollback()

    def test_update_Not(self):
        TestSQLite3Impl.db.update('bar', {'signal' : 'C'}, {'!id' : 99})

        rows = TestSQLite3Impl.db.select('bar')

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (98, 98, 2.3, 'C'))
        self.assertEqual(rows[1], (99, 99, 2.4, 'Z'))

        TestSQLite3Impl.db.rollback()

    def test_update_Error(self):
        with self.assertRaises(DatabaseDataError) as cm:
            TestSQLite3Impl.db.update('foo', {})
        self.assertEqual(
                cm.exception.msg, 'No values provided for UPDATE')

    def test_null_insert(self):
        TestSQLite3Impl.db.insert('bar', \
                {'id' : 100, 'heading' : 270, 'speed' : 33.3})

        rows = TestSQLite3Impl.db.select('bar', {'id' : 100})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (100, 270, 33.3, None))

        TestSQLite3Impl.db.rollback()

    def test_null_update(self):
        TestSQLite3Impl.db.insert('bar', \
                {'id' : 101, 'heading' : 90, 'speed' : 61.0, 'signal' : 'A'})

        TestSQLite3Impl.db.update('bar', {'speed' : None}, {'id' : 101})

        rows = TestSQLite3Impl.db.select('bar', {'id' : 101})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (101, 90, None, 'A'))

        TestSQLite3Impl.db.rollback()

    def test_delete(self):
        TestSQLite3Impl.db.insert('bar', \
                {'id' : 101, 'heading' : 180, 'speed' : 42.0, 'signal' : 'B'})
        TestSQLite3Impl.db.commit()

        rows = TestSQLite3Impl.db.select('bar')
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[2], (101, 180, 42.0, 'B'))

        TestSQLite3Impl.db.delete('bar', {'id' : 101})
        TestSQLite3Impl.db.commit()

        rows = TestSQLite3Impl.db.select('bar')
        self.assertEqual(len(rows), 2)

        rows = TestSQLite3Impl.db.select('bar', {'id' : 101})
        self.assertEqual(len(rows), 0)

    def test_delete_Greater(self):
        TestSQLite3Impl.db.insert('bar', \
                {'id' : 101, 'heading' : 180, 'speed' : 42.0, 'signal' : 'B'})

        TestSQLite3Impl.db.delete('bar', {'>heading' : 100})    
        rows = TestSQLite3Impl.db.select('bar')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (98, 98, 2.3, 'X'))
        self.assertEqual(rows[1], (99, 99, 2.4, 'Z'))
        TestSQLite3Impl.db.rollback()

    def test_delete_Less(self):
        TestSQLite3Impl.db.insert('bar', \
                {'id' : 101, 'heading' : 180, 'speed' : 42.0, 'signal' : 'B'})

        TestSQLite3Impl.db.delete('bar', {'<heading' : 99})    
        rows = TestSQLite3Impl.db.select('bar')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (99, 99, 2.4, 'Z'))
        self.assertEqual(rows[1], (101, 180, 42.0, 'B'))
        TestSQLite3Impl.db.rollback()

    def test_delete_Between(self):
        TestSQLite3Impl.db.insert('bar', \
                {'id' : 101, 'heading' : 180, 'speed' : 42.0, 'signal' : 'B'})

        TestSQLite3Impl.db.delete('bar', {'<heading' : 100, '>heading' : 97})
        rows = TestSQLite3Impl.db.select('bar')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (101, 180, 42.0, 'B'))
        TestSQLite3Impl.db.rollback()

    def test_delete_Not(self):
        TestSQLite3Impl.db.insert('bar', \
                {'id' : 101, 'heading' : 180, 'speed' : 42.0, 'signal' : 'B'})

        TestSQLite3Impl.db.delete('bar', {'!id' : 101})
        rows = TestSQLite3Impl.db.select('bar')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (101, 180, 42.0, 'B'))
        TestSQLite3Impl.db.rollback()

if __name__ == '__main__':
    import unittest
    unittest.main()
