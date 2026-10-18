import pytest

import merkle_reference as ref
from merkle_proof import DefaultHasher, RootMismatchError, verify_consistency

SIZE1, SIZE2 = 3, 7


@pytest.fixture
def case():
    leaves = ref.make_leaves(SIZE2)
    return {
        "root1": ref.root(leaves[:SIZE1]),
        "root2": ref.root(leaves),
        "proof": ref.consistency_proof(SIZE1, leaves),
    }


def test_verify_consistency_rejects_wrong_old_root(case):
    with pytest.raises(RootMismatchError):
        verify_consistency(
            DefaultHasher,
            SIZE1,
            SIZE2,
            ref.hexlist(case["proof"]),
            bytes(32).hex(),
            case["root2"].hex(),
        )


def test_verify_consistency_rejects_wrong_new_root(case):
    with pytest.raises(RootMismatchError):
        verify_consistency(
            DefaultHasher,
            SIZE1,
            SIZE2,
            ref.hexlist(case["proof"]),
            case["root1"].hex(),
            bytes(32).hex(),
        )


def test_verify_consistency_rejects_every_tampered_proof_element(case):
    for i in range(len(case["proof"])):
        tampered = list(case["proof"])
        tampered[i] = bytes(32)

        with pytest.raises(RootMismatchError):
            verify_consistency(
                DefaultHasher,
                SIZE1,
                SIZE2,
                ref.hexlist(tampered),
                case["root1"].hex(),
                case["root2"].hex(),
            )


def test_verify_consistency_rejects_fork_with_different_history():
    original = ref.make_leaves(7)
    forked = original[:2] + [b"rewritten"] + original[3:]

    with pytest.raises(RootMismatchError):
        verify_consistency(
            DefaultHasher,
            3,
            7,
            ref.hexlist(ref.consistency_proof(3, forked)),
            ref.root(original[:3]).hex(),
            ref.root(forked).hex(),
        )


def test_verify_consistency_equal_sizes_with_different_roots_mismatch():
    with pytest.raises(RootMismatchError):
        verify_consistency(DefaultHasher, 5, 5, [], bytes(32).hex(), (b"\x01" * 32).hex())
