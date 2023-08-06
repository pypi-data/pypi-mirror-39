
import grpc
# import the generated classes
import NetworkCli_pb2_grpc

from cursor import Cursor

class Connection():

    def __init__(self, host=None, port=None, cursorclass=Cursor):

        self.host = host
        self.port = port
        self.channel = None
        self.stub = None
        self.cursorclass = cursorclass

        #create channel and stub
        self.connect()

    def close(self):
        """
        grpc channel is closed which closes the connection between this interface
        and Quickstep DB.
        :return:
        """
        if self.channel is None:
            return
        self.channel.close()

    def connect(self):
        """
        grpc insecure channel is created and the client is created.
        :return:
        """
        insecure_channel = self.host+":"+self.port
        self.channel = grpc.insecure_channel(insecure_channel)
        self.stub = NetworkCli_pb2_grpc.NetworkCliStub(self.channel)

    def cursor(self, cursor=None):
        """

        :param cursor:
        :return: Cursor
        """
        if cursor:
            return cursor(self)
        return self.cursorclass(self)

