from samson.utilities.math import mod_inv
from samson.utilities.bytes import Bytes
from samson.publickey.dsa import DSA

# https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm
class ECDSA(DSA):
    def __init__(self, G, hash_obj, d=None):
        self.G = G
        self.q = self.G.curve.q
        self.d = d or max(1, Bytes.random(self.q.bit_length() + 7 // 8).int() % self.q)
        self.Q = self.d * self.G
        self.H = hash_obj

    
    def __repr__(self):
        return f"<ECDSA: d={self.d}, G={self.G}, Q={self.Q}, H={self.H}>"


    def __str__(self):
        return self.__repr__()
    

    def sign(self, message, k=None):
        r = 0
        s = 0

        while s == 0 or r == 0:
            k = k or max(1, Bytes.random(self.q .bit_length() + 7 // 8).int() % self.q)
            inv_k = mod_inv(k, self.q)

            z = self.H.hash(message).int()
            z >>= max(self.H.digest_size * 8 - self.q.bit_length(), 0)

            r = (k * self.G).x % self.q
            s = (inv_k * (z + self.d * r)) % self.q

        return (r, s)
    
    
    def verify(self, message, sig):
        (r, s) = sig
        w = mod_inv(s, self.q)

        z = self.H.hash(message).int()
        z >>= max(self.H.digest_size * 8 - self.q.bit_length(), 0)

        u_1 = (z * w) % self.q
        u_2 = (r * w) % self.q
        v = u_1 * self.G + u_2 * self.Q
        return v.x == r