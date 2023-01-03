import shutil

DB_PATH = "./testdb"


def delete_db_dir():
    shutil.rmtree(DB_PATH)
