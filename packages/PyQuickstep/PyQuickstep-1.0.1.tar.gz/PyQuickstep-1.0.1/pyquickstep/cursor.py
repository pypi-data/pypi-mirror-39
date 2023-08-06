
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

    def _check_executed(self):
        if not self._executed:
            raise databaseerror.ProgrammingError("execute() first")

    def execute(self, query, args=None):

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
        self._check_executed()
        if self._rows is None or self.rownumber >= self.rowcount:
            return None
        result = self._rows[self.rownumber]
        self.rownumber = self.rownumber + 1
        return result

    def fetchmany(self, size=None):
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
        self._check_executed()
        if self._rows is None:
            return ()
        result = self._rows[self.rownumber:]
        self.rownumber = self.rowcount
        return result

    def setinputsizes(self, *args):
        """Following DB API guidelines. Does nothing."""

    def setoutputsizes(self, *args):
        """Following DB API guidelines. Does nothin."""