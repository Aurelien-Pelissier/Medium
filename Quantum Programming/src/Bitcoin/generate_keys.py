import bitcoin #pip install bitcoin
import ecdsa #pip install ecdsa
import os
from ecdsa.util import string_to_number, number_to_string


def main():
    key_with_bitcoin()
    key_with_edsca()
    
    
    
def discrete_logarithm(public_point, generator):
    #We need to recover secret such as public_point = secret * generator
    return 0
    


def key_with_edsca():
    
    # secp256k1, http://www.oid-info.com/get/1.3.132.0.10
    _p = "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2FL"
    _r = "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141L"
    _b = "0x0000000000000000000000000000000000000000000000000000000000000007L"
    _a = "0x0000000000000000000000000000000000000000000000000000000000000000L"
    _Gx = "0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798L"
    _Gy = "0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8L"
    curve_secp256k1 = ecdsa.ellipticcurve.CurveFp(_p, _a, _b)
    generator_secp256k1 = ecdsa.ellipticcurve.Point(curve_secp256k1, _Gx, _Gy, _r)
    oid_secp256k1 = (1, 3, 132, 0, 10)
    SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1, generator_secp256k1, oid_secp256k1)
    ec_order = _r
    
    curve = curve_secp256k1
    generator = generator_secp256k1
    
    def random_secret():
        convert_to_int = lambda array: int("".join(array).encode("hex"), 16)
    
        # Collect 256 bits of random data from the OS's cryptographically secure random generator
        byte_array = os.urandom(32)
    
        return convert_to_int(byte_array)
    
    def get_point_pubkey(point):
        if point.y() & 1:
            key = '03' + '%064x' % point.x()
        else:
            key = '02' + '%064x' % point.x()
        return key.decode('hex')
    
    def get_point_pubkey_uncompressed(point):
        key = '04' + \
              '%064x' % point.x() + \
              '%064x' % point.y()
        return key.decode('hex')
    
    
    # Generate a new private key.
    secret = random_secret()
    print("  Secret: ", secret)
    
    # Get the public key point.
    public_point = secret * generator
    print("  EC point:", public_point)
    
    print("  BTC public key:", get_point_pubkey(public_point).encode("hex"))
    
    
    #REVERSE Piblic key:
    secret = discrete_logarithm(public_point, generator)
    
    # Given the point (x, y) we can create the object using:
    point1 = ecdsa.ellipticcurve.Point(curve, public_point.x(), public_point.y(), ec_order)
    assert point1 == public_point


def key_with_bitcoin():
    # Generate a random private key
    valid_private_key = False
    while not valid_private_key:
        private_key = bitcoin.random_key()
        decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
        valid_private_key =  0 < decoded_private_key < bitcoin.N
    
    print("  Private Key (hex) is: ", private_key)
    print("  Private Key (decimal) is: ", decoded_private_key)
    
    # Convert private key to WIF format
    wif_encoded_private_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
    print("  Private Key (WIF) is: ", wif_encoded_private_key)
    
    # Add suffix "01" to indicate a compressed private key
    compressed_private_key = private_key + '01'
    print("  Private Key Compressed (hex) is: ", compressed_private_key)
    
    # Generate a WIF format from the compressed private key (WIF-compressed)
    wif_compressed_private_key = bitcoin.encode_privkey(
        bitcoin.decode_privkey(compressed_private_key, 'hex'), 'wif')
    print("  Private Key (WIF-Compressed) is: ", wif_compressed_private_key)
    
    # Multiply the EC generator point G with the private key to get a public key point
    public_key = bitcoin.fast_multiply(bitcoin.G, decoded_private_key)
    print("  Public Key (x,y) coordinates is:", public_key)
    
    # Encode as hex, prefix 04
    hex_encoded_public_key = bitcoin.encode_pubkey(public_key,'hex')
    print("  Public Key (hex) is:", hex_encoded_public_key)
    
    # Compress public key, adjust prefix depending on whether y is even or odd
    (public_key_x, public_key_y) = public_key
    if (public_key_y % 2) == 0:
        compressed_prefix = '02'
    else:
        compressed_prefix = '03'
    hex_compressed_public_key = compressed_prefix + bitcoin.encode(public_key_x, 16)
    print("  Compressed Public Key (hex) is:", hex_compressed_public_key)
    
    # Generate bitcoin address from public key
    print("  Bitcoin Address (b58check) is:", bitcoin.pubkey_to_address(public_key))
    
    # Generate compressed bitcoin address from compressed public key
    print("  Compressed Bitcoin Address (b58check) is:", bitcoin.pubkey_to_address(hex_compressed_public_key))
    
    
if __name__ == "__main__":
    main()