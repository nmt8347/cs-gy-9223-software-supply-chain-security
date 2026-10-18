import pytest

from merkle_proof import (
    DefaultHasher,
    RootMismatchError,
    chain_border_right,
    chain_inner,
    chain_inner_right,
    decomp_incl_proof,
    inner_proof_size,
    verify_match,
)

H = DefaultHasher.hash_children
SEED, A, B = b"S" * 32, b"A" * 32, b"B" * 32


@pytest.mark.parametrize(
    "index, size, expected",
    [(0, 1, 0), (0, 8, 3), (2, 8, 3), (5, 6, 0), (7, 8, 0)],
)
def test_inner_proof_size(index, size, expected):
    assert inner_proof_size(index, size) == expected


@pytest.mark.parametrize(
    "index, size, expected",
    [(0, 1, (0, 0)), (2, 8, (3, 0)), (5, 6, (0, 2)), (7, 8, (0, 3))],
)
def test_decomp_incl_proof(index, size, expected):
    assert decomp_incl_proof(index, size) == expected


def test_chain_inner_orders_hash_by_index_bits():
    # index bits (LSB first): 1, 0 -> proof element on the left, then on the right.
    assert chain_inner(DefaultHasher, SEED, [A, B], 0b01) == H(H(A, SEED), B)
    # index bits: 0, 1
    assert chain_inner(DefaultHasher, SEED, [A, B], 0b10) == H(B, H(SEED, A))
    assert chain_inner(DefaultHasher, SEED, [], 0) == SEED


def test_chain_inner_right_only_applies_set_bits():
    assert chain_inner_right(DefaultHasher, SEED, [A, B], 0b00) == SEED
    assert chain_inner_right(DefaultHasher, SEED, [A, B], 0b01) == H(A, SEED)
    assert chain_inner_right(DefaultHasher, SEED, [A, B], 0b10) == H(B, SEED)
    assert chain_inner_right(DefaultHasher, SEED, [A, B], 0b11) == H(B, H(A, SEED))


def test_chain_border_right_always_places_proof_on_left():
    assert chain_border_right(DefaultHasher, SEED, []) == SEED
    assert chain_border_right(DefaultHasher, SEED, [A, B]) == H(B, H(A, SEED))


def test_verify_match_accepts_equal_and_rejects_different():
    assert verify_match(b"x" * 32, b"x" * 32) is None

    with pytest.raises(RootMismatchError):
        verify_match(b"x" * 32, b"y" * 32)
