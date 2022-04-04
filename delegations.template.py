'''Set delegations to a list of wallet addresses mapped to ftso provider addresses and a delegation percentage in bips.
'''
delegations = {
  # wallet 1
  '0x...1': [
    { 'provider': '0x...a', 'bips': 10000 } # Provider a
  ],
  # wallet 2
  '0x...2': [
    { 'provider': '0x...b', 'bips': 5000 }, # Provider b
    { 'provider': '0x...c', 'bips': 5000 }  # Provider c
  ],
}