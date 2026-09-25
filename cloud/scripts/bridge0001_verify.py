#!/usr/bin/env python3

BASES = {
    'A': (0, 0),
    'G': (0, 1),
    'C': (1, 0),
    'T': (1, 1),
}
INV = {v: k for k, v in BASES.items()}
COMP = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}


def add(u, v):
    return (u[0] ^ v[0], u[1] ^ v[1])


def f_ry(v):
    return v[0]


def f_mk(v):
    return v[1]


def f_ws(v):
    return v[0] ^ v[1]


def main():
    # Complement = translation by (1,1)
    for b, v in BASES.items():
        assert INV[add(v, (1, 1))] == COMP[b]
        assert INV[add(add(v, (1, 1)), (1, 1))] == b

    # Canonical quotient partitions
    expected = {
        'RY': {'A': 0, 'G': 0, 'C': 1, 'T': 1},
        'MK': {'A': 0, 'C': 0, 'G': 1, 'T': 1},
        'WS': {'A': 0, 'T': 0, 'G': 1, 'C': 1},
    }
    funcs = {'RY': f_ry, 'MK': f_mk, 'WS': f_ws}
    for name, fn in funcs.items():
        for b, v in BASES.items():
            assert fn(v) == expected[name][b]

    # Exhaust all nonzero linear functionals V -> Z2.
    # Any linear functional is f_ab(x,y)=a*x XOR b*y.
    observed = set()
    for a, b in [(1, 0), (0, 1), (1, 1)]:
        outputs = tuple((a & v[0]) ^ (b & v[1]) for v in BASES.values())
        observed.add(outputs)
    assert len(observed) == 3

    # Complement action on each quotient.
    assert f_ry((1, 1)) == 1
    assert f_mk((1, 1)) == 1
    assert f_ws((1, 1)) == 0

    print('BRIDGE-0001: PASS')
    print('DNA alphabet is Z2 x Z2 under the fixed encoding.')
    print('RY, MK, WS are exactly the three nonzero linear one-bit quotients.')
    print('Watson-Crick complement is translation by (1,1).')
    print('Projected complement action: RY flip, MK flip, WS preserve.')


if __name__ == '__main__':
    main()
