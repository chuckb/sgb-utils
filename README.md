# Delegate and Claim Utilities for Songbird FTSO

## Background

This is a set of utilities, written in Python, to delegate wrapped SGB and make reward claims.

If you have one wallet to manage, the Towo Labs mobile wallet is a good choice. But if you have multiple accounts, it is a bit cumbersome. Since claiming needs to be done every week, these utilities can make it much easier. It also demonstrates how to call Flare smart contracts using Python on the Songbird network.

Note that the Towo API endpoint is used. It is rate limited and these utilities try to respect that. Please do not abuse their endpoint.

## Requirements
- Python 3
- Web3 python lib

## Keys
You should encrypt each private key for each wallet to be managed and put them in a common directory. Use the same passphrase for each key.

## Utilities
See documentation within each utility for usage.

### Encrypt Key
`encryptkey.py` will take a private key and encrypt it using a passphrase. It will then store the encrypted key in a specified file on the command line.

### Claim and Wrap
`claimnwrap.py` will iterate over the private keys and for each key will claim SGB FTSO rewards and wrap the rewards for compounded earning.

### Delegate
`delegate.py` will iterate over the private keys and for each key will un-delegate all and re-delegate to delegates specified in `delegations.py`. Copy `delegations.template.py`, fill in the public key for each wallet, and fill in the delegate public key and the percentage of the delegation in bips.
