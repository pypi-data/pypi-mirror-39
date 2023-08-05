An RPC server that extends the default ``neo-python`` RPC server with plugable commands.

Installation
------------
Install the package via ``pip``
::

    pip install neopython-extended-rpc-server

Next, open your `neo-python's <https://github.com/CityOfZion/neo-python/>`__ ``protocol.<network>.json``, find the ``RPCServer`` key and set it as follows

::

"RPCServer": "neopython_ext_rpc_server.ExtRpcServer.ExtendedJsonRpcApi"

Note that the default installation has not additional commands over ``neo-python``'s build-in RPC Server.

Extending with new commands
---------------------------
You can extend the RPC server with your own commands by creating a plugin. This has 2 requirements:

1. Your plugin must extend the ``ExtendedRpcCommand`` class and implement the required methods.
2. Your plugin must be installed using ``setuptools`` and register an entrypoint under ``neopython.extrpc.plugins``. See the ``entry_points`` key in `/extrpc-plugin-example/setup.py` for an example.

If your plugin does not adhere to the above 2 requirements it will not be picked up by the loader. The easiest approach is probably to copy the example plugin folder and adjust it to your needs.

Once your done you can either share your plugin via `PyPi <https://pypi.org/>`__ (`Instructions <https://packaging.python.org/tutorials/packaging-projects/>`__) to make it installable via ``pip`` or you can install it directly using ``python setup.py install``.

 Note: you have to restart the RPC server for new commands to be picked up.

