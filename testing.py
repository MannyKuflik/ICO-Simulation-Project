import sha3
from ecdsa import SigningKey, SECP256k1

keccak = sha3.keccak_256()
sk_string = '8c70afd6be9a772cd1fe852c411cc67b829f402c733a45d27b9b8eb6b9710dc4'
private = SigningKey.from_string(bytes().fromhex(sk_string), curve=SECP256k1)
print('PRIVATE: ',private.to_string())
public = private.get_verifying_key().to_string()
print('PUBLIC: ',public)
keccak.update(public)
address = "0x{}".format(keccak.hexdigest()[24:])
print('ADDRESS: ',address)
