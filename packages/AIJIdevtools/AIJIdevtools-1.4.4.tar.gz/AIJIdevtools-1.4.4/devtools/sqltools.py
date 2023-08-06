from sqlparse import parse
from sqlparse.tokens import Keyword, DML
from sqlparse.sql import Identifier, Where


__all__ = [
  'is_dml',
]


def is_dml(sql):
    parsed_list = parse(sql)
    for parsed in parsed_list:
        if parsed.token_first(skip_cm=True).ttype is not DML:
            return False
    return True


def update_or_delete_to_select(statement):
    return 'SELECT * FROM ' + \
           str(list(filter(
               lambda x: isinstance(x, Identifier),
               statement))[0])\
           + ' ' + \
           str(list(filter(
               lambda x: isinstance(x, Where),
               statement))[-1])


def find_tables(sql):
    parsed_list = parse(sql)
    tables = set()
    for parsed in parsed_list:
        found_key = -1
        for index, item in enumerate(parsed):
            if item.value.upper() in ['INTO', 'FROM', 'UPDATE']:
                found_key = index
            elif found_key != -1:
                if item.ttype is Identifier or item.ttype is None:
                    tables.add(item.get_name())
                elif item.ttype is Keyword:
                    found_key = -1
    return list(filter(None, tables))


# Input a sql
# Return a select only SQL list
def selectify(sentence: str):
    for statement in parse(sentence):
        if statement.get_type() in ['UPDATE', 'DELETE']:
            yield update_or_delete_to_select(statement)
