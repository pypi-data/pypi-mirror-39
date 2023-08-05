#!/usr/bin/env python

import re
import sys
def is_legal_mysql_table_name(table_name):
    legal_mysql_table_name_regex_object = re.compile(r'[^a-zA-Z0-9_$.]')
    legal_mysql_table_name_regex_search_result = legal_mysql_table_name_regex_object.search(table_name)
    if bool(legal_mysql_table_name_regex_search_result):
        table_name_not_legal_message = 'The table name {} is not a MySql legal table name. Only the following characters are allowed [a-zA-Z0-9_$]'.format(table_name)
        print(table_name_not_legal_message)
        sys.exit(1)
    return True


print(is_legal_mysql_table_name('code42_sp_useast_1'))
