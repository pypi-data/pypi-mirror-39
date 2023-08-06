
from constants import COMMON

class QuickstepResult(object):

    def __init__(self, connection):

        self.connection = connection
        self.affected_rows = None
        self.rows = None



    def check_error_response(self, error_result):
        '''

        Have to check error result and throw excpetion
        :param error_result:
        :return:
        '''

    def parse_response(self, response):

        self.check_error_response(response.error_result)
        result_string = str(response.query_result)
        result_string_list = result_string.split(COMMON.NEWLINE)

        rows = []
        for item in result_string_list:
            item_list = item.split(COMMON.RESULTSPLIT)
            row = []
            for item_item in item_list:
                ii = "".join(item_item.split())
                row.append(ii)
            row = row[1:]
            row = row[:-1]
            if len(row) > 0:
                rows.append(tuple(row))

        rows = rows[1:]
        self.affected_rows = len(rows)
        self.rows = tuple(rows)

