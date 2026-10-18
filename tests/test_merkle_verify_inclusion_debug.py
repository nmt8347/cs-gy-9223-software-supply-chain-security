import merkle_reference as ref
from merkle_proof import DefaultHasher, verify_inclusion


def test_verify_inclusion_debug_prints_calculated_and_given_roots(capsys):
    leaves = ref.make_leaves(5)
    tree_root = ref.root(leaves).hex()
    proof = ref.hexlist(ref.inclusion_proof(4, leaves))
    leaf = ref.leaf_hash(leaves[4]).hex()

    verify_inclusion(DefaultHasher, 4, 5, leaf, proof, tree_root, debug=True)

    out = capsys.readouterr().out
    assert f"Calculated root hash {tree_root}" in out
    assert f"Given root hash {tree_root}" in out


def test_verify_inclusion_without_debug_prints_nothing(capsys):
    leaves = ref.make_leaves(5)
    verify_inclusion(
        DefaultHasher,
        4,
        5,
        ref.leaf_hash(leaves[4]).hex(),
        ref.hexlist(ref.inclusion_proof(4, leaves)),
        ref.root(leaves).hex(),
    )

    assert capsys.readouterr().out == ""
