import sqlalchemy as sa
import databases


DATABASE_URL = 'sqlite:///blog.db'

metadata = sa.MetaData()
database = databases.Database(DATABASE_URL)
engine = sa.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
