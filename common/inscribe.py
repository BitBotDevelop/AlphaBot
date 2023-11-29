from bitcoinutils.keys import P2trAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.utils import ControlBlock
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
from bitcoinutils.setup import setup
import codecs
import binascii
import json


def set_network(network: str = "testnet"):
  """
  设置网络，testnet 或者 mainnet
  """
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



def generate_brc20_mint_inscribe_content(tick: str, amt: int):
  content = {
    "p": "brc-20",
    "op": "mint",
    "tick": tick,
    "amt": str(amt),
  }
  return json.dumps(content)



def generate_brc20_deploy_inscribe_content(tick: str, max_supply: int, limit: int):
  content = {
    "p": "brc-20",
    "op": "deploy",
    "tick": tick,
    "max": str(max_supply),
    "lim": str(limit),
  }
  return json.dumps(content)



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

def get_text_script_pub_key(private: str, content: str):
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
    coonvert_string_to_hex(content),
    "OP_ENDIF",
  ])
  return tr_script_p2pk

def get_inscription_address(private: str, tr_script_p2pk: Script):
  """
  生成铭文的转入地址
  """
  privkey_tr_script = PrivateKey.from_bytes(bytes.fromhex(private))
  pubkey_tr_script = privkey_tr_script.get_public_key()

  # taproot script path address
  from_address = pubkey_tr_script.get_taproot_address([[tr_script_p2pk]])
  return from_address.to_string()

def get_brc20_mint_inscription_address(private: str, tick: str, amt: int):
  """
  生成brc20 mint铭文的转入地址
  """
  content = generate_brc20_mint_inscribe_content(tick, amt)
  script = get_text_script_pub_key(private, content)
  return get_inscription_address(private, script)

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
  """
  铭刻交易
  """
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
  return [tx.serialize(), tx.get_vsize(), tx.get_txid()]



def inscribe_and_send_after_tx(
    txid: str,
    vout: int,
    amount: int,
    fee: int,
    private: str,
    block_nummber: int,
    receive_address: str,
    send_address: str,
  ):
  """
  
  """
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
  refundAddress = P2trAddress(send_address)

  base = 546
  tx_out_list = []
  if amount - base > 0:
    tx_out_inscription = TxOutput(base, toAddress.to_script_pub_key())
    tx_out_list.append(tx_out_inscription)
  else:
    tx_out_inscription = TxOutput(amount, toAddress.to_script_pub_key())
    tx_out_list.append(tx_out_inscription)
  if amount - base - fee > 0:
    tx_out_refund = TxOutput(amount - fee - base, refundAddress.to_script_pub_key())
    tx_out_list.append(tx_out_refund)

  print(tx_out_list)
  
  tx = Transaction([tx_in], tx_out_list, has_segwit=True)
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
  return [tx.serialize(), tx.get_vsize(), tx.get_txid()]

def refund_from_inscription_tx(
    txid: str,
    vout: int,
    amount: int,
    fee: int,
    private: str,
    block_nummber: int,
    receive_address: str,
):
  privkey_tr_script = PrivateKey.from_bytes(bytes.fromhex(private))
  pubkey_tr_script = privkey_tr_script.get_public_key()
  tr_script_p2pk = get_bitmap_script_pub_key(private, block_nummber)

  # taproot script path address
  from_address = pubkey_tr_script.get_taproot_address([[tr_script_p2pk]])

  # create transaction input from tx id of UTXO
  tx_in = TxInput(txid, vout)

  amounts = [amount]

  scriptPubkey = from_address.to_script_pub_key()
  utxos_scriptPubkeys = [scriptPubkey]
  toAddress = P2trAddress(receive_address)

  tx_out_list = []
  tx_out_inscription = TxOutput(amount - fee, toAddress.to_script_pub_key())
  tx_out_list.append(tx_out_inscription)

  print(tx_out_list)
  
  tx = Transaction([tx_in], tx_out_list, has_segwit=True)


  sig = privkey_tr_script.sign_taproot_input(
        tx,
        0,
        utxos_scriptPubkeys,
        amounts,
        script_path=False,
        tapleaf_scripts=[tr_script_p2pk],
    )

  tx.witnesses.append(TxWitnessInput([sig]))
  # print raw signed transaction ready to be broadcasted
  return [tx.serialize(), tx.get_vsize(), tx.get_txid()]


def inscribe_from_tr_script(txid: str, vout: int, amount: int, private: str, tr_script_p2pk: Script, receive_address: str):
  """
  铭刻交易
  """
  # taproot script is a simple P2PK with the following keys
  privkey_tr_script = PrivateKey.from_bytes(bytes.fromhex(private))
  pubkey_tr_script = privkey_tr_script.get_public_key()

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
  return [tx.serialize(), tx.get_vsize(), tx.get_txid()]