import pytest

import merkle_reference as ref
from merkle_proof import DefaultHasher, verify_inclusion


@pytest.mark.parametrize("size", range(1, 18))
def test_verify_inclusion_accepts_valid_proofs_for_every_index(size):
    leaves = ref.make_leaves(size)
    tree_root = ref.root(leaves).hex()

    for index in range(size):
        proof = ref.hexlist(ref.inclusion_proof(index, leaves))
        leaf = ref.leaf_hash(leaves[index]).hex()

        # Returns None and does not raise.
        assert verify_inclusion(DefaultHasher, index, size, leaf, proof, tree_root) is None
