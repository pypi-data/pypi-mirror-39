import json
import shutil
from neo.Wallets.utils import to_aes_key
from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neopython_ext_rpc_server.ExtRpcTestCase import ExtendedJsonRpcApiTestCase, mock_post_request
from neo.Utils.WalletFixtureTestCase import WalletFixtureTestCase


class ExamplePluginTest(ExtendedJsonRpcApiTestCase):

    def test_example_plugin_command(self):
        req = self._gen_post_rpc_req("my_command")
        mock_req = mock_post_request(json.dumps(req).encode("utf-8"))
        res = json.loads(self.app.home(mock_req))
        self.assertEqual('first command success', res['result'])

        req = self._gen_post_rpc_req("my_command2")
        mock_req = mock_post_request(json.dumps(req).encode("utf-8"))
        res = json.loads(self.app.home(mock_req))
        self.assertEqual('second command success', res['result'])



    def test_example_plugin_command_fail(self):
        test_wallet_path = shutil.copyfile(
            WalletFixtureTestCase.wallet_1_path(),
            WalletFixtureTestCase.wallet_1_dest()
        )

        self.app.wallet = UserWallet.Open(
            test_wallet_path,
            to_aes_key(WalletFixtureTestCase.wallet_1_pass())
        )

        req = self._gen_post_rpc_req("my_command")
        mock_req = mock_post_request(json.dumps(req).encode("utf-8"))
        res = json.loads(self.app.home(mock_req))
        error = res.get('error', {})
        self.assertEqual(error.get('code', None), -1337)
        self.assertEqual(error.get('message', None), "Unsafe command with open wallet")
