import pytest

import merkle_reference as ref
from merkle_proof import DefaultHasher, verify_consistency

MAX_SIZE = 17


@pytest.mark.parametrize("size2", range(1, MAX_SIZE + 1))
def test_verify_consistency_accepts_valid_proofs_for_every_prefix(size2):
    leaves = ref.make_leaves(size2)
    root2 = ref.root(leaves).hex()

    for size1 in range(1, size2 + 1):
        root1 = ref.root(leaves[:size1]).hex()
        proof = ref.hexlist(ref.consistency_proof(size1, leaves))

        # Returns None and does not raise.
        assert (
            verify_consistency(DefaultHasher, size1, size2, proof, root1, root2) is None
        )


def test_verify_consistency_equal_sizes_use_empty_proof():
    leaves = ref.make_leaves(9)
    tree_root = ref.root(leaves).hex()

    verify_consistency(DefaultHasher, 9, 9, [], tree_root, tree_root)
