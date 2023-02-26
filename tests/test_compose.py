from issuetruck.compose import compose


def test_compose_add_mul():
    add3 = lambda x: x + 3
    mul5 = lambda x: x * 5

    add3mul5 = compose(add3, mul5)
    assert add3mul5(0) == 15
    assert add3mul5(1) == 20
    assert add3mul5(2) == 25
    assert add3mul5(-1) == 10

    mul5add3 = compose(mul5, add3)
    assert mul5add3(0) == 3
    assert mul5add3(1) == 8
    assert mul5add3(2) == 13
    assert mul5add3(-1) == -2
