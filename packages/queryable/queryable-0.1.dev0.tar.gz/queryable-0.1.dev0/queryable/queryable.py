import keyword
import sqlite3
import textwrap


_MISSING = object()


class MemDB(object):
    def __init__(self, schema):
        self.db = sqlite3.connect(':memory:')
        for statement in schema.split(';'):
            statement = statement.strip()
            if statement:
                self.db.execute(statement)

    def execute(self, sql):
        '''pass-through'''
        return self.db.execute(sql)

    def sql(self, sql, args=None):
        '''run sql against underlying DB, fetch and returns results'''
        if args is None:
            return self.db.execute(sql).fetchall()
        return self.db.execute(sql, args).fetchall()

    def sql_val(self, sql, args=None, default=_MISSING):
        '''run SELECT sql that returns single value'''
        result = self.sql(sql, args)
        if not result:
            if default is not _MISSING:
                return default
            raise ValueError("sql returned no rows", sql)
        return result[0][0]

    def sql_list(self, sql, args=None):
        '''run SELECT and return [a, b, c] instead of [(a,), (b,), (c,)]'''
        return list(sum(self.sql(sql, args), ()))

    def __getattr__(self, queryname):
        if queryname in self.named_queries:
            return self.named_queries[queryname]
        raise AttributeError(queryname)


def make_db_class(name, schema, named_queries):
    namespace = {}
    for query in named_queries:
        query._build_func(namespace)
    return type(name, (MemDB,), namespace)


class NamedQuery(object):
    '''
    name -- logical name to refer to it as, must be a valid python identifier
    query -- sql query to execute
    args -- iterable of argument names (default no arguments)
    arity -- table / list / value (default table);
             does it return a 2-D table, a 1-D list, or a single value
    help_ -- a help string (default the query)
    '''
    def __init__(self, name, query, args=(), arity='table', help_=None):
        assert not keyword.iskeyword(name)  # TODO: more complete identifier check
        help_ = help_ or query
        self.name, self.query, self.args, self.arity, self.help = name, query, args, arity, help_

    def _build_func(self, namespace):
        callthru = {'table': 'sql', 'list': 'sql_list', 'value': 'sql_val'}[self.arity]
        code = textwrap.dedent(
        '''
        def {name}({args}):
            return {callthru}({query}, ({args},))
        '''.format(
            name=self.name,
            args=", ".join(self.args)),
            callthru=callthru,
            query=repr(self.query),
            )
        exec code in namespace
