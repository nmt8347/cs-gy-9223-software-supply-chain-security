"""Independent RFC 6962 reference implementation used to generate valid proofs.

Deliberately does not import merkle_proof, so the tests cross-check the
implementation under test against the RFC definitions (section 2.1).
"""
import hashlib


def leaf_hash(data):
    return hashlib.sha256(b"\x00" + data).digest()


def node_hash(left, right):
    return hashlib.sha256(b"\x01" + left + right).digest()


def make_leaves(n):
    return [f"leaf-{i}".encode() for i in range(n)]


def _split(n):
    """Largest power of two strictly less than n (n >= 2)."""
    k = 1
    while k * 2 < n:
        k *= 2
    return k


def root(leaves):
    n = len(leaves)
    if n == 0:
        return hashlib.sha256(b"").digest()
    if n == 1:
        return leaf_hash(leaves[0])
    k = _split(n)
    return node_hash(root(leaves[:k]), root(leaves[k:]))


def inclusion_proof(index, leaves):
    n = len(leaves)
    if n == 1:
        return []
    k = _split(n)
    if index < k:
        return inclusion_proof(index, leaves[:k]) + [root(leaves[k:])]
    return inclusion_proof(index - k, leaves[k:]) + [root(leaves[:k])]


def consistency_proof(m, leaves):
    return _subproof(m, leaves, True)


def _subproof(m, leaves, complete):
    n = len(leaves)
    if m == n:
        return [] if complete else [root(leaves)]
    k = _split(n)
    if m <= k:
        return _subproof(m, leaves[:k], complete) + [root(leaves[k:])]
    return _subproof(m - k, leaves[k:], False) + [root(leaves[:k])]


def hexlist(items):
    return [i.hex() for i in items]
