from binascii import a2b_hex

VERSION_TRANSACTION = bytes([0])
VERSION_CONTRACT_ONT = bytes([0])
VERSION_CONTRACT_ONG = bytes([0])

NATIVE_TRANSFER = "transfer"
NATIVE_TRANSFER_FROM = "transferFrom"
NATIVE_APPROVE = "approve"
NATIVE_ALLOWANCE = "allowance"
DID_ONT = "did:ont:"

# NeoVM invokes a smart contract return type

NEOVM_TYPE_BOOL = 1
NEOVM_TYPE_INTEGER = 2
NEOVM_TYPE_BYTE_ARRAY = 3
NEOVM_TYPE_STRING = 4
UINT256_SIZE = 32

ZERO_ADDRESS = a2b_hex("0000000000000000000000000000000000000000".encode())
ONT_CONTRACT_ADDRESS = a2b_hex(("0000000000000000000000000000000000000001").encode())
ONG_CONTRACT_ADDRESS = a2b_hex(("0000000000000000000000000000000000000002").encode())
ONTID_CONTRACT_ADDRESS = a2b_hex(("0000000000000000000000000000000000000003").encode())
PARAM_CONTRACT_ADDRESS = a2b_hex(("0000000000000000000000000000000000000004").encode())
AUTH_CONTRACT_ADDRESS = a2b_hex(("0000000000000000000000000000000000000006").encode())
GOVERNANCE_CONTRACT_ADDRESS = a2b_hex(("0000000000000000000000000000000000000007").encode())


TX_MAX_SIG_SIZE = 16
MULTI_SIG_MAX_PUBKEY_SIZE = 16
