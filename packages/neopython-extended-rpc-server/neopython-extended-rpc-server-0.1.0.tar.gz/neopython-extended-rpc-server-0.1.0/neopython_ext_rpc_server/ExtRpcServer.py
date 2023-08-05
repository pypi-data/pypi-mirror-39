import pkg_resources
import inspect
from neo.api.JSONRPC.JsonRpcApi import JsonRpcApi
from .ExtRpcCommand import ExtendedRpcCommand

pip_plugins = {
    entry_point.name: entry_point.load()
    for entry_point
    in pkg_resources.iter_entry_points('neopython.extrpc.plugins')
}

plugins = []
for module in pip_plugins.values():
    for i in dir(module):
        attribute = getattr(module, i)
        # to find a class that extends ExtendedRpcCommand
        if inspect.isclass(attribute) and issubclass(attribute, ExtendedRpcCommand):
            plugins.append(attribute)


class ExtendedJsonRpcApi(JsonRpcApi):
    """
    Extended JSON-RPC API Methods
    """

    def __init__(self, port, wallet=None):
        super(ExtendedJsonRpcApi, self).__init__(port, wallet)
        self.commands = {}
        for plugin in plugins:
            for command in plugin.commands():
                self.commands.update({command: plugin})

    @classmethod
    def options_response(cls):
        return {'supported HTTP methods': ("GET", "POST"),
                'JSON-RPC server type': "extended-rpc"}

    def json_rpc_method_handler(self, method, params):
        plugin = self.commands.get(method)
        if plugin:
            return plugin.execute(self, method, params)
        else:
            return super(ExtendedJsonRpcApi, self).json_rpc_method_handler(method, params)
