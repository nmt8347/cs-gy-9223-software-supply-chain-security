import pytest

import merkle_reference as ref
from merkle_proof import DefaultHasher, verify_consistency

ROOT = bytes(32).hex()


def test_verify_consistency_rejects_size2_smaller_than_size1():
    with pytest.raises(ValueError, match="size2"):
        verify_consistency(DefaultHasher, 5, 4, [], ROOT, ROOT)


def test_verify_consistency_rejects_proof_when_sizes_equal():
    with pytest.raises(ValueError, match="not empty"):
        verify_consistency(DefaultHasher, 5, 5, [ROOT], ROOT, ROOT)


def test_verify_consistency_size1_zero_requires_empty_proof():
    assert verify_consistency(DefaultHasher, 0, 5, [], ROOT, ROOT) is None

    with pytest.raises(ValueError, match="expected empty"):
        verify_consistency(DefaultHasher, 0, 5, [ROOT], ROOT, ROOT)


def test_verify_consistency_rejects_empty_proof_for_different_sizes():
    with pytest.raises(ValueError, match="empty bytearray_proof"):
        verify_consistency(DefaultHasher, 3, 7, [], ROOT, ROOT)


def test_verify_consistency_rejects_wrong_proof_length():
    leaves = ref.make_leaves(7)
    proof = ref.hexlist(ref.consistency_proof(3, leaves))
    root1 = ref.root(leaves[:3]).hex()
    root2 = ref.root(leaves).hex()

    with pytest.raises(ValueError, match="wrong bytearray_proof size"):
        verify_consistency(DefaultHasher, 3, 7, proof[:-1], root1, root2)
    with pytest.raises(ValueError, match="wrong bytearray_proof size"):
        verify_consistency(DefaultHasher, 3, 7, proof + [ROOT], root1, root2)


@pytest.mark.parametrize("bad", ["zz", "abc", "not hex"])
def test_verify_consistency_rejects_non_hex_roots(bad):
    with pytest.raises(ValueError):
        verify_consistency(DefaultHasher, 5, 5, [], bad, ROOT)
