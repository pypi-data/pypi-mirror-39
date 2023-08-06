import os.path as op
import os
import tempfile
import pandas as pd


def visuallize_df(df):
    """For development purpose, displays df under Libreoffice
    :param df: a Pandas dataframe
    :return: None
    """
    tmp_fpath = op.join(tempfile.mkdtemp(), "tmp.xlsx")
    df.to_excel(tmp_fpath)
    cmd = 'soffice "{}"'.format(tmp_fpath)
    print(cmd)
    os.system(cmd)
