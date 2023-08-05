import os
from neo.Settings import settings
from .ExtRpcServer import ExtendedJsonRpcApi
from neo.Utils.BlockchainFixtureTestCase import BlockchainFixtureTestCase
from klein.test.test_resource import requestMock
from twisted.web import server
from twisted.web.test.test_web import DummyChannel


def mock_post_request(body):
    return requestMock(path=b'/', method=b"POST", body=body)


def mock_get_request(path, method=b"GET"):
    request = server.Request(DummyChannel(), False)
    request.uri = path
    request.method = method
    request.clientproto = b'HTTP/1.1'
    return request


class ExtendedJsonRpcApiTestCase(BlockchainFixtureTestCase):
    app = None  # type:JsonRpcApi

    @classmethod
    def leveldb_testpath(cls):
        return os.path.join(settings.DATA_DIR_PATH, 'fixtures/test_chain')

    def setUp(self):
        self.app = ExtendedJsonRpcApi(20332)

    def _gen_post_rpc_req(self, method, params=None, request_id="2"):
        ret = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method
        }
        if params:
            ret["params"] = params
        return ret

    def _gen_get_rpc_req(self, method, params=None, request="2"):
        ret = "/?jsonrpc=2.0&method=%s&params=[]&id=%s" % (method, request)
        if params:
            ret = "/?jsonrpc=2.0&method=%s&params=%s&id=%s" % (method, params, request)
        return ret.encode('utf-8')
