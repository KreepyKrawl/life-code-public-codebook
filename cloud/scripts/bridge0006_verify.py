#!/usr/bin/env python3

from itertools import product


def main():
    U = list(product([0, 1], repeat=2))
    p1 = lambda u: u[0]
    p2 = lambda u: u[1]
    p3 = lambda u: u[0] ^ u[1]

    for p in (p1, p2, p3):
        fibers = {v: [u for u in U if p(u) == v] for v in (0, 1)}
        assert all(len(xs) == 2 for xs in fibers.values())

    joint = {(p1(u), p2(u)): u for u in U}
    assert len(joint) == len(U)
    for u in U:
        assert joint[(p1(u), p2(u))] == u

    direct = [0]
    for _ in range(15):
        direct.append(1 - direct[-1])

    hidden_state = 0
    hosted = [hidden_state]
    for _ in range(15):
        hidden_state = 1 - hidden_state
        hosted.append(hidden_state)

    assert direct == hosted

    print('BRIDGE-0006 FINITE VERIFIER: PASS')
    print('Single observer projections are non-injective.')
    print('Two independent projections reconstruct the hidden state exactly.')
    print('Distinct hidden realizations can be observationally equivalent.')
    print('The substrate-necessity theorem itself is deductive, not computational.')


if __name__ == '__main__':
    main()
