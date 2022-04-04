#!/usr/local/bin/python3

from eth_account import Account
from getopt import getopt, GetoptError
import json
import sys
import os
from web3 import Web3
import time
from delegations import delegations
import getpass

def main(argv):
  '''Reset ftso delegates for a list of wallets defined within delegations.py.

  See delegations.template.py for an example layout.

  A keys directory is required that contains the encrypted private key of each wallet to be reset.

  The keys can be encrypted with the encryptkey.py utility.
  The key directory can be set with the commandline switch -k.
  The key directory will default to keys.

  Running this utility will prompt for the passphrase to unencrypt
  each key. The utility assumes you used the same passphrase to encrypt
  each key.
  '''

  keydir = './keys'
  rpcurl = "https://songbird.towolabs.com/rpc"

  # Set up access to wrapped Songbird contract (wNAT)
  wNATAddress = '0x02f0826ef6aD107Cfc861152B32B52fD11BaB9ED'
  wNATABI = '[{"type":"constructor","stateMutability":"nonpayable","inputs":[{"type":"address","name":"_governance","internalType":"address"},{"type":"string","name":"_name","internalType":"string"},{"type":"string","name":"_symbol","internalType":"string"}]},{"type":"event","name":"Approval","inputs":[{"type":"address","name":"owner","internalType":"address","indexed":true},{"type":"address","name":"spender","internalType":"address","indexed":true},{"type":"uint256","name":"value","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"CreatedTotalSupplyCache","inputs":[{"type":"uint256","name":"_blockNumber","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"Deposit","inputs":[{"type":"address","name":"dst","internalType":"address","indexed":true},{"type":"uint256","name":"amount","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"GovernanceProposed","inputs":[{"type":"address","name":"proposedGovernance","internalType":"address","indexed":false}],"anonymous":false},{"type":"event","name":"GovernanceUpdated","inputs":[{"type":"address","name":"oldGovernance","internalType":"address","indexed":false},{"type":"address","name":"newGoveranance","internalType":"address","indexed":false}],"anonymous":false},{"type":"event","name":"Transfer","inputs":[{"type":"address","name":"from","internalType":"address","indexed":true},{"type":"address","name":"to","internalType":"address","indexed":true},{"type":"uint256","name":"value","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"VotePowerContractChanged","inputs":[{"type":"uint256","name":"_contractType","internalType":"uint256","indexed":false},{"type":"address","name":"_oldContractAddress","internalType":"address","indexed":false},{"type":"address","name":"_newContractAddress","internalType":"address","indexed":false}],"anonymous":false},{"type":"event","name":"Withdrawal","inputs":[{"type":"address","name":"src","internalType":"address","indexed":true},{"type":"uint256","name":"amount","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"allowance","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"address","name":"spender","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"approve","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceHistoryCleanup","inputs":[{"type":"address","name":"_owner","internalType":"address"},{"type":"uint256","name":"_count","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOfAt","inputs":[{"type":"address","name":"_owner","internalType":"address"},{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256[]","name":"","internalType":"uint256[]"}],"name":"batchVotePowerOfAt","inputs":[{"type":"address[]","name":"_owners","internalType":"address[]"},{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"claimGovernance","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"cleanupBlockNumber","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"decreaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"subtractedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"delegate","inputs":[{"type":"address","name":"_to","internalType":"address"},{"type":"uint256","name":"_bips","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"delegateExplicit","inputs":[{"type":"address","name":"_to","internalType":"address"},{"type":"uint256","name":"_amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address[]","name":"_delegateAddresses","internalType":"address[]"},{"type":"uint256[]","name":"_bips","internalType":"uint256[]"},{"type":"uint256","name":"_count","internalType":"uint256"},{"type":"uint256","name":"_delegationMode","internalType":"uint256"}],"name":"delegatesOf","inputs":[{"type":"address","name":"_owner","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address[]","name":"_delegateAddresses","internalType":"address[]"},{"type":"uint256[]","name":"_bips","internalType":"uint256[]"},{"type":"uint256","name":"_count","internalType":"uint256"},{"type":"uint256","name":"_delegationMode","internalType":"uint256"}],"name":"delegatesOfAt","inputs":[{"type":"address","name":"_owner","internalType":"address"},{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"delegationModeOf","inputs":[{"type":"address","name":"_who","internalType":"address"}]},{"type":"function","stateMutability":"payable","outputs":[],"name":"deposit","inputs":[]},{"type":"function","stateMutability":"payable","outputs":[],"name":"depositTo","inputs":[{"type":"address","name":"recipient","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"governance","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IGovernanceVotePower"}],"name":"governanceVotePower","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"increaseAllowance","inputs":[{"type":"address","name":"spender","internalType":"address"},{"type":"uint256","name":"addedValue","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"initialise","inputs":[{"type":"address","name":"_governance","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"name","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"needsReplacementVPContract","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"proposeGovernance","inputs":[{"type":"address","name":"_governance","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"proposedGovernance","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IVPContractEvents"}],"name":"readVotePowerContract","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"revokeDelegationAt","inputs":[{"type":"address","name":"_who","internalType":"address"},{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setCleanerContract","inputs":[{"type":"address","name":"_cleanerContract","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setCleanupBlockNumber","inputs":[{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setCleanupBlockNumberManager","inputs":[{"type":"address","name":"_cleanupBlockNumberManager","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setGovernanceVotePower","inputs":[{"type":"address","name":"_governanceVotePower","internalType":"contract IIGovernanceVotePower"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setReadVpContract","inputs":[{"type":"address","name":"_vpContract","internalType":"contract IIVPContract"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setWriteVpContract","inputs":[{"type":"address","name":"_vpContract","internalType":"contract IIVPContract"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"symbol","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupplyAt","inputs":[{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupplyCacheCleanup","inputs":[{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupplyHistoryCleanup","inputs":[{"type":"uint256","name":"_count","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalVotePower","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalVotePowerAt","inputs":[{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalVotePowerAtCached","inputs":[{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transfer","inputs":[{"type":"address","name":"recipient","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"transferFrom","inputs":[{"type":"address","name":"sender","internalType":"address"},{"type":"address","name":"recipient","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"transferGovernance","inputs":[{"type":"address","name":"_governance","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"undelegateAll","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"_remainingDelegation","internalType":"uint256"}],"name":"undelegateAllExplicit","inputs":[{"type":"address[]","name":"_delegateAddresses","internalType":"address[]"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"undelegatedVotePowerOf","inputs":[{"type":"address","name":"_owner","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"undelegatedVotePowerOfAt","inputs":[{"type":"address","name":"_owner","internalType":"address"},{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"votePowerFromTo","inputs":[{"type":"address","name":"_from","internalType":"address"},{"type":"address","name":"_to","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"votePowerFromToAt","inputs":[{"type":"address","name":"_from","internalType":"address"},{"type":"address","name":"_to","internalType":"address"},{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"votePowerOf","inputs":[{"type":"address","name":"_owner","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"votePowerOfAt","inputs":[{"type":"address","name":"_owner","internalType":"address"},{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"votePowerOfAtCached","inputs":[{"type":"address","name":"_owner","internalType":"address"},{"type":"uint256","name":"_blockNumber","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"withdraw","inputs":[{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"withdrawFrom","inputs":[{"type":"address","name":"owner","internalType":"address"},{"type":"uint256","name":"amount","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IVPContractEvents"}],"name":"writeVotePowerContract","inputs":[]},{"type":"receive","stateMutability":"payable"}]'

  # Get command line args  
  try:
    opts, args = getopt(argv, "hk:", ["keydir="])
  except GetoptError:
    printinvoke()
    exit(2)

  for opt, arg in opts:
    if opt == "-h":
      printinvoke()
      exit()
    elif opt in ("-k", "--keydir"):
      keydir = arg

  # Get the password to unencrypt keys...they should all be set to the
  # same password for convenience.
  # password = input("Password: ")
  password = getpass.getpass()

  # Init web3
  web3 = Web3(Web3.HTTPProvider(rpcurl))

  # Initialize access to wNAT contract
  wNATContract = web3.eth.contract(address=wNATAddress, abi=wNATABI)

  # Setup default web3 transaction parameters. Note chain id 19 is the
  # Songbird chain.
  tx_parms = {
    'chainId': 19,
    'gas': 500000,
    'gasPrice': web3.toWei('50', 'gwei'),
    'nonce': 0
  }

  # Iterate over all private key files in the keys directory
  keyfiles = os.listdir(keydir)
  for keyfile in keyfiles:
      if os.path.isfile(os.path.join(keydir, keyfile)):
        with open(os.path.join(keydir, keyfile), 'r') as f:
          # Set up account to work with by decrypting the private key.
          encrypted = json.loads(f.read())
          privatekey = Account.decrypt(encrypted, password)
          account = Account.from_key(privatekey)
          web3.eth.default_account = account.address
          print("************************************************")
          print(f'Keyfile: {keyfile}')
          print(f'Address: {account.address}')
          # Get the delegation for the wallet address
          delegation = {}
          try:
            delegation = delegations[account.address]
          except:
            print("No delegations.")
            continue
          # Undelegate all delegates
          tx_parms["nonce"] = web3.eth.getTransactionCount(account.address)
          tx = wNATContract.functions.undelegateAll().buildTransaction(tx_parms)
          tx_receipt = transact(web3, account, tx)
          print(f'Undelegated with tx_hash {tx_receipt["transactionHash"].hex()}')
          # Iterate over all delegates
          for delegate in delegation:
            # Delegate vote power percentage defined for each delegate
            tx_parms["nonce"] = web3.eth.getTransactionCount(account.address)
            tx = wNATContract.functions.delegate(web3.toChecksumAddress(delegate["provider"]), delegate["bips"]).buildTransaction(tx_parms)
            tx_receipt = transact(web3, account, tx)
            print(f'Delegate to {delegate["provider"]} bips of {delegate["bips"]} with tx_hash {tx_receipt["transactionHash"].hex()}')

def transact(web3, account, tx):
  '''Helper function to sign and send transactions.

  Args:
    web3: An instantiated Web3 provider.
    account: An instantiated eth_account.Account that will sign the tx.
    tx: The transaction to sign, generated by the smart contract ABI helper functions.

  Returns:
    The transaction receipt.
  '''
  signed_tx = account.sign_transaction(tx)
  # Towo has rate limiters.
  time.sleep(1)
  tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
  time.sleep(1)
  tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
  return tx_receipt

def printinvoke():
  print("usage:")
  print("  delegate.py -k <keysdirectory>")
  print("  -k is optional. Default is ./keys")

if __name__ == "__main__":
  main(sys.argv[1:])