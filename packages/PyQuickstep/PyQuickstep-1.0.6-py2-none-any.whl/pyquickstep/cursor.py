
# import the generated classes
import NetworkCli_pb2
from quickstepresult import QuickstepResult
from pyquickstep.error import databaseerror


class Cursor(object):

    def __init__(self, connection):

        self.connection = connection
        self.rownumber = 0
        self.rowcount = -1
        self._result = None
        self._executed = None
        self._rows = None

    def close(self):

        if self.connection is None:
            return

        self.clear_result()
        self.connection = None

    def clear_result(self):

        self.rownumber = 0
        self._result = None
        self._executed = None
        self._rows = None
        self.rowcount = 0
    def _check_executed(self):
        if not self._executed:
            raise databaseerror.ProgrammingError("execute() first")

    def execute(self, query, args=None):
        """
        Makes a request using GRPC with the query string and get the response parses it and returns it
        :param query:
        :param args:
        :return: Parsed query result
        """
        #have to implement getting arguments for the query
        conn = self.connection
        request = NetworkCli_pb2.QueryRequest(query=query)
        response = conn.stub.SendQuery(request)
        self._executed = query
        result = QuickstepResult(conn)
        result.parse_response(response)
        self.get_result(result)
        return result.affected_rows

    def get_result(self, result):

        self._rows = result.rows
        self.rowcount = result.affected_rows
        self._result = result

    def fetchone(self):
        """
        fetches the row pointed by cursor and moves the cursor to next row
        :return: returns row in the cursor
        """
        self._check_executed()
        if self._rows is None or self.rownumber >= self.rowcount:
            return None
        result = self._rows[self.rownumber]
        self.rownumber = self.rownumber + 1
        return result

    def fetchmany(self, size=None):
        """
        fetches the size number of rows in cursor and moves the cursor to size+1 row
        :param size:
        :return: size number of rows in the cursor
        """
        self._check_executed()
        if self._rows is None:
            return ()
        if size is None:
            size = 1
        last_row_index = self.rownumber + size
        result = self._rows[self.rownumber:last_row_index]
        self.rownumber = min(last_row_index, self.rowcount)
        return result

    def fetchall(self):
        """
        fetches all the rows available in cursor and moves the cursor position to the end
        :return: all the rows available in the cursor
        """
        self._check_executed()
        if self._rows is None:
            return ()
        result = self._rows[self.rownumber:]
        self.rownumber = self.rowcount
        return result

    def scroll(self, value, mode="relative"):

        self._check_executed()
        if mode is "relative":
            row_number = self.rownumber + value
        elif mode is "absolute":
            row_number = value
        else:
            raise databaseerror.ProgrammingError("Scroll mode %s is invalid" % mode)

        if not (0 <= row_number < len(self._rows)):
            raise IndexError("Index out of range")

        self.rownumber = row_number
    def setinputsizes(self, *args):
        """Following DB API guidelines. Does nothing."""

    def setoutputsizes(self, *args):
        """Following DB API guidelines. Does nothin."""