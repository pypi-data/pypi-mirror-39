import sqlite3

from models import Base

class User(Base):
    __tablename__ = 'users'

    id = ('INTEGER', 'not null')
    username = ('INTEGER', '')


class Posts(Base):
    __tablename__ = 'posts'

    id = ('INTEGER', 'not null')
    postname = ('INTEGER', 'PRIMARY KEY AUTOINCREMENT')
    user_id = ('INTEGER', 'not null')

    __relationships__ = (('user_id', 'users', 'id'),)


if __name__ == '__main__':
    conn = sqlite3.connect('db')


    print(Base(conn=conn).create_table(User))
    print(Base(conn=conn).create_table(Posts))

    print(Posts(conn=conn, lazy=True, id=1).select())
    print((User(username=1, conn=conn).update(
        id=123, username=1)))
    #print(Base(conn=conn).drop_table())
    print(User(conn=conn).update(id=123, username=123))
    print(User(conn=conn).insert(id=1, username=123))
    print(User(conn=conn).select('id'))
