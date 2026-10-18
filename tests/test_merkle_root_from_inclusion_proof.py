import pytest

import merkle_reference as ref
from merkle_proof import DefaultHasher, root_from_inclusion_proof


def test_root_from_inclusion_proof_returns_reference_root():
    leaves = ref.make_leaves(11)
    index = 6

    result = root_from_inclusion_proof(
        DefaultHasher,
        index,
        11,
        ref.leaf_hash(leaves[index]),
        ref.inclusion_proof(index, leaves),
    )

    assert result == ref.root(leaves)


def test_root_from_inclusion_proof_rejects_index_beyond_size():
    with pytest.raises(ValueError, match="index is beyond size"):
        root_from_inclusion_proof(DefaultHasher, 8, 8, bytes(32), [])


@pytest.mark.parametrize("bad_length", [0, 31, 33])
def test_root_from_inclusion_proof_rejects_wrong_leaf_hash_length(bad_length):
    with pytest.raises(ValueError, match="unexpected size"):
        root_from_inclusion_proof(DefaultHasher, 0, 1, bytes(bad_length), [])


def test_root_from_inclusion_proof_rejects_wrong_proof_length():
    leaves = ref.make_leaves(8)
    leaf = ref.leaf_hash(leaves[3])
    proof = ref.inclusion_proof(3, leaves)

    with pytest.raises(ValueError, match="wrong proof size"):
        root_from_inclusion_proof(DefaultHasher, 3, 8, leaf, proof[:-1])
    with pytest.raises(ValueError, match="wrong proof size"):
        root_from_inclusion_proof(DefaultHasher, 3, 8, leaf, proof + [bytes(32)])
