import binascii

import pytest

import merkle_reference as ref
from merkle_proof import DefaultHasher, RootMismatchError, verify_inclusion

SIZE = 8
INDEX = 2


@pytest.fixture
def case():
    leaves = ref.make_leaves(SIZE)
    return {
        "root": ref.root(leaves),
        "leaf": ref.leaf_hash(leaves[INDEX]),
        "proof": ref.inclusion_proof(INDEX, leaves),
    }


def test_verify_inclusion_rejects_wrong_root(case):
    bad_root = ref.root(ref.make_leaves(SIZE + 1)).hex()

    with pytest.raises(RootMismatchError):
        verify_inclusion(
            DefaultHasher, INDEX, SIZE, case["leaf"].hex(), ref.hexlist(case["proof"]), bad_root
        )


def test_verify_inclusion_rejects_wrong_leaf_hash(case):
    wrong_leaf = ref.leaf_hash(b"not in tree").hex()

    with pytest.raises(RootMismatchError):
        verify_inclusion(
            DefaultHasher, INDEX, SIZE, wrong_leaf, ref.hexlist(case["proof"]), case["root"].hex()
        )


def test_verify_inclusion_rejects_wrong_index(case):
    with pytest.raises(RootMismatchError):
        verify_inclusion(
            DefaultHasher,
            INDEX + 1,
            SIZE,
            case["leaf"].hex(),
            ref.hexlist(case["proof"]),
            case["root"].hex(),
        )


def test_verify_inclusion_rejects_every_tampered_proof_element(case):
    for i in range(len(case["proof"])):
        tampered = list(case["proof"])
        tampered[i] = bytes(32)

        with pytest.raises(RootMismatchError):
            verify_inclusion(
                DefaultHasher,
                INDEX,
                SIZE,
                case["leaf"].hex(),
                ref.hexlist(tampered),
                case["root"].hex(),
            )


def test_root_mismatch_error_reports_both_roots(case):
    bad_root = bytes(32)

    with pytest.raises(RootMismatchError) as exc:
        verify_inclusion(
            DefaultHasher,
            INDEX,
            SIZE,
            case["leaf"].hex(),
            ref.hexlist(case["proof"]),
            bad_root.hex(),
        )

    assert exc.value.expected_root == binascii.hexlify(bad_root)
    assert exc.value.calculated_root == binascii.hexlify(case["root"])
    message = str(exc.value)
    assert "does not match expected root" in message
    assert "calculated root" in message
