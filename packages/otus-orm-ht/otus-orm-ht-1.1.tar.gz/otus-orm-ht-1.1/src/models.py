import errors


class Meta(type):
    metadata = []
    
    def __new__(cls, name, bases, attr):
        if not attr.get('__tablename__'):
            attr['__tablename__'] = name

        obj = super(Meta, cls).__new__(cls, name, bases, attr)
        if name != 'Base':
            Meta.metadata.append(obj)
    
        return obj


class Base(metaclass=Meta):
    
    def __init__(self, conn, lazy=False, **args):
        self.__class__.__conn__ = conn
        self.__class__.__cur__ = conn.cursor()
        self.__class__.__lazy__ = lazy
        fields = [
            k for k in self.__class__.__dict__.keys()
            if not k.startswith('__')
        ]
        self.__class__.__filter__ = {}
        if args:
            if not set(fields).issuperset(set(args.keys())):
                raise errors.UknownColumn(self.__class__.__name__)
            self.__class__.__filter__ = args

    @classmethod
    def create_table(cls, *args):
        tables_lst = Base.metadata
        if args:
            if not set(Base.metadata).issuperset(set(args)):
                raise errors.UknownColumn(cls.__name__)
            tables_lst = args

        for table in tables_lst:
            create_fields = [
                '%s %s' % (key, ' '.join(value)) for key, value in
                table.__dict__.items() if not key.startswith('__')
            ]
            foreign_keys = []
            if table.__dict__.get('__relationships__'):
                foreign_keys = [
                    'FOREIGN KEY (%s) REFERENCES %s(%s)' % k for k
                    in table.__relationships__
                ]
            create_fields.extend(foreign_keys)
            cmd_line = 'CREATE TABLE IF NOT EXISTS %s ( %s );' % (
                table.__tablename__, ', '.join(create_fields))
            cls.__cur__.execute(cmd_line)
            cls.__conn__.commit()


    @classmethod
    def drop_table(cls, *args):
        if args:
            if not set(Base.metadata).issuperset(set(args)):
                raise errors.UknownColumn(cls.__name__)
            tables_lst = args
        else:
            tables_lst = Base.metadata
            
        for table in tables_lst:
            cmd_line = 'DROP TABLE IF EXISTS %s;' % table.__tablename__
            cls.__cur__.execute(cmd_line)
            cls.__conn__.commit()

    @classmethod
    def update(cls, **args):
        if args:
            fields = [k for k in cls.__dict__.keys() if not k.startswith('__')]
            if not set(fields).issuperset(set(args.keys())):
                raise errors.UknownColumn(cls.__name__)
            filter_str = ''
            if cls.__filter__:
                filter_lst = [
                    '%s = %s' % (key, value) for key, value
                    in cls.__filter__.items()
                ]
                filter_str = 'WHERE ' + ' and '.join(filter_lst)
            set_line = [
                '%s = %s' % (key, value) for key, value in args.items()]
            cmd_line = 'UPDATE %s SET %s %s;' % (
                cls.__tablename__, ', '.join(set_line), filter_str)
        else:
            raise errors.emptyArguments
        cls.__cur__.execute(cmd_line)
        cls.__conn__.commit()

    @classmethod
    def insert(cls, **args):
        if args:
            fields = [k for k in cls.__dict__.keys() if not k.startswith('__')]
            if not set(fields).issuperset(set(args.keys())):
                raise errors.UknownColumn(cls.__name__)
            
            insert_col = args.keys()
            insert_val = list(map(lambda x: str(args[x]), insert_col))
            insert_col_line = ', '.join(insert_col)
            insert_val_line = ', '.join(insert_val)
            filter_str = ''
            if cls.__filter__:
                filter_lst = [
                    '%s=%s' % (key, value) for key, value
                    in cls.__filter.items()
                ]
                filter_str = 'WHERE ' + ' and '.join(filter_lst)
            cmd_line = 'INSERT INTO %s (%s) VALUES (%s) %s;' % (
                cls.__tablename__, insert_col_line, insert_val_line, filter_str
            )
            cls.__cur__.execute(cmd_line)
            cls.__conn__.commit()

            
        else:
            raise errors.emptyArguments

    @classmethod
    def select(cls, *args):
        filter_str = ''
        if cls.__filter__:
            filter_lst = ['%s.%s = %s' %
                          (cls.__tablename__, key, value) for key, value
                          in cls.__filter__.items()
                          ]
            filter_str = 'WHERE ' + ' and '.join(filter_lst)
        join_str = ''
        if cls.__lazy__ and cls.__dict__.get('__relationships__'):
            join_lst = [
                'LEFT JOIN %s ON %s.%s = %s.%s' %
                (r[1], cls.__tablename__, r[0], r[1], r[2]) for r
                in cls.__relationships__
            ]
            join_str = ' '.join(join_lst)
        if args:
            fields = [k for k in cls.__dict__.keys() if not k.startswith('__')]
            if not set(fields).issuperset(set(args)):
                raise errors.UknownColumn(cls.__name__)
            cmd_line = 'SELECT %s FROM %s %s %s;' % (
                ', '.join(args), cls.__tablename__, join_str, filter_str)
        else:
            cmd_line = 'SELECT * FROM %s %s %s;' % (
                cls.__tablename__, join_str, filter_str)
            cls.__cur__.execute(cmd_line)
        return cls.__cur__.fetchall()
