# coding:utf-8

# from .matrix import Matrix
# def p(x):
#     print('asdf')

import pandas as pd
import numpy as np


class Baumkuchen:

    # 100% nan のカラムを@で埋める
    def empty(self, df):

        # 100% nan のカラムをリストアップする
        c = df.loc[:, df.isnull().sum()==len(df)].columns

        # 100% nan のカラムを@で埋める
        df[c] = df[c].fillna('@')

        return df


    # カテゴリ型のカラムを上位thresholdカテゴリのみ残して @MINORITY で埋め、nanは @FILLED で埋める
    def categorical(self, df, mask=None, threshold=3):

        # カテゴリ型のカラムをリストアップする
        c = df.select_dtypes(include=[np.object, np.bool]).columns

        # マスクする
        c = c ^ (c & {mask})

        # カテゴリ型のカラムに関して上位thresholdカテゴリのみ残してそれ以外の値を@MINORにする
        df[c] = df[c].apply(lambda x: x.mask(~x.isnull() & ~x.isin(x.value_counts().index[:threshold]), '@.MINORITY'))

        # カテゴリ型のカラムを@で埋める
        df[c] = df[c].fillna('@.FILLED')

        return df

    # 数値型のカラムを平均値で埋め、埋めた場所がわかるように新たなカラムを追加する
    def numerical(self, df, mask=None):

        # 数値型のカラムをリストアップする
        c = df.select_dtypes(include=[np.number]).columns

        for v in c:
            # 列のソート（最後尾に）
            df = df[df.columns.drop(v).append(pd.Index([v]))]

            # 埋めた場所がわかるように新たなカラムを追加する。
            df['%s@'%v] = df[v].isnull()

        # 平均値で埋める
        df[c] = df[c].fillna(df[c].mean())

        return df


if __name__ == '__main__':
    b = Baumkuchen()

    df = pd.DataFrame([
        [np.nan,1,1,1,1,1,'D','D','D','A'],
        [np.nan,3,3,3,3,3,'E','D','E','B'],
        [np.nan,np.nan,3,3,3,3,'E','D','E','B'],
        [np.nan,2,3,3,3,3,'E','A','E','B'],
        [np.nan,3,3,3,3,3,'E','E','E','B'],
        [np.nan,3,3,np.nan,3,3,'E','C','E','B'],
        [np.nan,3,np.nan,3,3,3,'E','H','E','B'],
        [np.nan,5,np.nan,5,5,5,'E','E','E','B'],
        [np.nan,4,4,4,4,4,np.nan,'E','E','B'],
        [np.nan,7,7,7,7,7,'E','E','E',np.nan],
        ])
    df.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    print(df)
    print(b.empty(df))
    print(b.categorical(df, 'd'))
    print(b.numerical(df))
    exit()
