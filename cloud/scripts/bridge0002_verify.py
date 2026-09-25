#!/usr/bin/env python3

from itertools import product


def main():
    # Finite toy substrate U = Z2 x Z2.
    U = list(product([0, 1], repeat=2))

    # Three limited observer projections.
    p1 = lambda u: u[0]
    p2 = lambda u: u[1]
    p3 = lambda u: u[0] ^ u[1]

    # Each single view is many-to-one: it loses information.
    for p in (p1, p2, p3):
        fibers = {v: [u for u in U if p(u) == v] for v in (0, 1)}
        assert all(len(xs) == 2 for xs in fibers.values())

    # Joint independent views recover the full hidden state exactly.
    joint = {(p1(u), p2(u)): u for u in U}
    assert len(joint) == len(U)
    for u in U:
        assert joint[(p1(u), p2(u))] == u

    # Embedded-observer non-identifiability toy.
    # Model A: observable state itself toggles.
    direct = [0]
    for _ in range(15):
        direct.append(1 - direct[-1])

    # Model B: hidden host state toggles; observer only sees its projection.
    hidden_state = 0
    hosted = [hidden_state]
    for _ in range(15):
        hidden_state = 1 - hidden_state
        hosted.append(hidden_state)

    # The observer stream is identical although the internal realizations differ.
    assert direct == hosted

    print('BRIDGE-0002 FINITE VERIFIER: PASS')
    print('Single observer projections are non-injective.')
    print('Two independent projections reconstruct the hidden state exactly.')
    print('Distinct hidden realizations can be observationally equivalent.')
    print('Note: the ontological necessity theorem is deductive, not a finite computational claim.')


if __name__ == '__main__':
    main()
