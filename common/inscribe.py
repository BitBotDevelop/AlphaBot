from bitcoinutils.keys import P2trAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.utils import ControlBlock
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
from bitcoinutils.setup import setup
import codecs
import binascii


def set_network(network: str = "testnet"):
  setup(network)

def coonvert_string_to_hex(content: str):
  """
  将字符串转化为hex
  """
  bt = codecs.encode(content, 'utf-8')
  hex_string = binascii.hexlify(bt).decode('utf-8')
  return hex_string

def generate_random_private_key():
  """
  生成随机私钥
  """
  priv = PrivateKey()
  return priv.to_bytes().hex()

def get_bitmap_script_pub_key(private: str, block_nummber: int):
  """
  生成铭文的scriptPubKey
  """
  # 重复但为了解耦
  privkey_tr_script = PrivateKey.from_bytes(bytes.fromhex(private))
  pubkey_tr_script = privkey_tr_script.get_public_key()
  tr_script_p2pk = Script([
    pubkey_tr_script.to_x_only_hex(),
    "OP_CHECKSIG",
    "OP_0",
    "OP_IF",
    coonvert_string_to_hex("ord"),
    "01",
    coonvert_string_to_hex("text/plain;charset=utf-8"),
    "OP_0",
    coonvert_string_to_hex(str(block_nummber) + ".bitmap"),
    "OP_ENDIF",
  ])
  return tr_script_p2pk

def get_bitmap_inscription_address(private: str, block_nummber: int):
  """
  生成铭文的转入地址
  """
  privkey_tr_script = PrivateKey.from_bytes(bytes.fromhex(private))
  pubkey_tr_script = privkey_tr_script.get_public_key()
  tr_script_p2pk = get_bitmap_script_pub_key(private, block_nummber)

  # taproot script path address
  from_address = pubkey_tr_script.get_taproot_address([[tr_script_p2pk]])
  print("From Taproot script address", from_address.to_string())
  return from_address.to_string()

def inscribe_after_tx(txid: str, vout: int, amount: int, private: str, block_nummber: int, receive_address: str):
  # taproot script is a simple P2PK with the following keys
  privkey_tr_script = PrivateKey.from_bytes(bytes.fromhex(private))
  pubkey_tr_script = privkey_tr_script.get_public_key()
  tr_script_p2pk = get_bitmap_script_pub_key(private, block_nummber)

  # taproot script path address
  from_address = pubkey_tr_script.get_taproot_address([[tr_script_p2pk]])

  print("From Taproot script address", from_address.to_string())


  # create transaction input from tx id of UTXO
  tx_in = TxInput(txid, vout)

  amounts = [amount]

  scriptPubkey = from_address.to_script_pub_key()
  utxos_scriptPubkeys = [scriptPubkey]
  toAddress = P2trAddress(receive_address)


  tx_out = TxOutput(546, toAddress.to_script_pub_key())
  tx = Transaction([tx_in], [tx_out], has_segwit=True)

  print("\nRaw transaction:\n" + tx.serialize())

  print("\ntxid: " + tx.get_txid())
  print("\ntxwid: " + tx.get_wtxid())

  # sign taproot input
  # to create the digest message to sign in taproot we need to
  # pass all the utxos' scriptPubKeys, their amounts and taproot script
  # we sign with the private key corresponding to the script - no keys
  # tweaking required
  sig = privkey_tr_script.sign_taproot_input(
      tx,
      0,
      utxos_scriptPubkeys,
      amounts,
      script_path=True,
      tapleaf_script=tr_script_p2pk,
      tweak=False,
  )

  # we spend a single script - no merkle path is required
  control_block = ControlBlock(pubkey_tr_script)

  tx.witnesses.append(
      TxWitnessInput([sig, tr_script_p2pk.to_hex(), control_block.to_hex()])
  )
  # print raw signed transaction ready to be broadcasted
  print("\nRaw signed transaction:\n" + tx.serialize())

  print("\nTxId:", tx.get_txid())
  print("\nTxwId:", tx.get_wtxid())

  print("\nSize:", tx.get_size())
  print("\nvSize:", tx.get_vsize())
  return [tx.serialize(), tx.get_vsize()]


