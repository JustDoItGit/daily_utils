import pymysql
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

user = ''
passwd = ''
host = ''
port = 3306
db_name = ''
engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(user, passwd, host, port, db_name))


class DataFrame2MysqlHistoryTable:
    def __init__(self, df, table_name, if_exists_, db_name_=db_name):
        self.df = df
        self.table_name = table_name
        self.db_name = db_name_
        self.if_exists = if_exists_

    def write_data(self):
        try:
            with engine.connect() as con, con.begin():
                self.df.to_sql(self.table_name, con, schema=self.db_name, if_exists=self.if_exists, index=False)
            con.close()
        except Exception as e:
            print(e)

    def delete_table_data(self):
        # db = pymysql.connect(host, user, passwd, db_name)
        # port must be int
        db = pymysql.connect(host=host, port=3306, user=user, password=passwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        # sql = 'DELETE FROM {0}'.format(self.table_name)
        sql = 'DELETE FROM %s' % self.table_name
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            str(e)
            db.rollback()
        db.close()


if __name__ == '__main__':
    df_ = pd.DataFrame({'A': [1, 2, 3, "中文", np.NaN],
                        'B': [1, np.NaN, 1, 1, np.NaN]
                        })
    df_.set_index(keys='A', inplace=True)
    DataFrame2MysqlHistoryTable(df_, 'test_df', 'append').write_data()
    # DataFrame2MysqlHistoryTable(df_, 'test_df', 'append').delete_table_data()
