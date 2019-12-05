import pytest
from orlanguage import OR
from orofxorlanguage import ORofXOR
from xorlanguage import XOR
from xoroforlanguage import XORofOR


def test_OR():
    bid1 = (["A", "B", "C"], 10)
    bid2 = (["D", "C"], 15)

    orbid = OR([bid1, bid2])
    assert str(orbid) == "(['A', 'B', 'C'], 10) OR (['D', 'C'], 15)"
    assert orbid.size == 2
    assert sorted(orbid.items) == ['A', 'B', 'C', 'D']

    with pytest.raises(TypeError):
        assert OR(0)
    with pytest.raises(TypeError):
        assert OR([0])
    with pytest.raises(TypeError):
        assert OR([(0, 0, 0)])
    with pytest.raises(TypeError):
        assert OR([([], "hello")])
    with pytest.raises(TypeError):
        assert OR([("hello", 10)])

    # test WDP
    bid1 = (['A'], 2)
    bid2 = (['A', 'B', 'D'], 3)
    bid3 = (['B', 'C'], 2)
    bid4 = (['C', 'D'], 1)
    orbid = OR([bid1, bid2, bid3, bid4])
    assert sorted(orbid.WDP()) == [(0,['A'], 2), (2,['B', 'C'], 2)]

    bid1 = (['D'], 1)
    bid2 = (['A', 'B'], 3)
    bid3 = (['B', 'C'], 2.5)
    bid4 = (['A', 'C', 'D'], 3)
    bid5 = (['E', 'C', 'D'], 1.5)
    bid6 = (['E', 'F'], 4.5)
    bid7 = (['F'], 3.5)
    bid8 = (['B', 'D'], 1)
    orbid = OR([bid1, bid2, bid3, bid4, bid5, bid6, bid7, bid8])
    assert sorted(orbid.WDP()) == [(0, ['D'], 1), (1, ['A', 'B'], 3), (5, ['E', 'F'], 4.5)]

def test_XOR():
    bid1 = (["A", "B", "C"], 10)
    bid2 = (["D", "C"], 15)

    xorbid = XOR([bid1, bid2])
    assert str(xorbid) == "(['A', 'B', 'C'], 10) XOR (['D', 'C'], 15)"
    assert xorbid.size == 2
    assert sorted(xorbid.items) == ['A', 'B', 'C', 'D']

    orbid = xorbid.to_OR()
    assert str(orbid) == "(['A', 'B', 'C', 'd'], 10) OR (['D', 'C', 'd'], 15)"
    assert orbid.size == 2
    assert sorted(orbid.items) == ['A', 'B', 'C', 'D', 'd']

    bid3 = (["d", "C"], 15)

    xorbid2 = XOR([bid1, bid2, bid3])
    assert str(xorbid2) == "(['A', 'B', 'C'], 10) XOR (['D', 'C'], 15) XOR (['d', 'C'], 15)"
    assert xorbid2.size == 3
    assert sorted(xorbid2.items) == ['A', 'B', 'C', 'D', 'd']
    
    orbid2 = xorbid2.to_OR()
    assert str(orbid2) == "(['A', 'B', 'C', 'd0'], 10) OR (['D', 'C', 'd0'], 15) OR (['d', 'C', 'd0'], 15)"
    assert orbid2.size == 3
    assert sorted(orbid2.items) == ['A', 'B', 'C', 'D', 'd', 'd0']

def test_ORofXOR():
    bid1 = (["A", "B"], 10)
    bid2 = (["C"], 12)
    bid3 = (["D", "E"], 10)
    bid4 = (["F"], 12)

    xorbid1 = XOR([bid1, bid2])
    xorbid2 = XOR([bid3, bid4])
    orofxorbid = ORofXOR([xorbid1, xorbid2])

    assert str(orofxorbid) == "((['A', 'B'], 10) XOR (['C'], 12)) OR ((['D', 'E'], 10) XOR (['F'], 12))"
    assert orofxorbid.size == 4
    assert sorted(orofxorbid.items) == ['A', 'B', 'C', 'D', 'E', 'F']

    orbid = orofxorbid.to_OR()
    assert str(orbid) == "(['A', 'B', 'd'], 10) OR (['C', 'd'], 12) OR (['D', 'E', 'd0'], 10) OR (['F', 'd0'], 12)"
    assert orbid.size == 4
    assert sorted(orbid.items) == ['A', 'B', 'C', 'D', 'E', 'F', 'd', 'd0']

def test_XORofOR():
    bid1 = (["A", "B"], 10)
    bid2 = (["C"], 12)
    bid3 = (["D", "E"], 10)
    bid4 = (["F"], 12)

    orbid1 = OR([bid1, bid2])
    orbid2 = OR([bid3, bid4])
    xoroforbid = XORofOR([orbid1, orbid2])

    assert str(xoroforbid) == "((['A', 'B'], 10) OR (['C'], 12)) XOR ((['D', 'E'], 10) OR (['F'], 12))"
    assert xoroforbid.size == 4
    assert sorted(xoroforbid.items) == ['A', 'B', 'C', 'D', 'E', 'F']

    orbid = xoroforbid.to_OR()
    assert str(orbid) == "(['A', 'B', 'd', 'd0'], 10) OR (['C', 'd1', 'd2'], 12) OR (['D', 'E', 'd', 'd1'], 10) OR (['F', 'd0', 'd2'], 12)"
    assert orbid.size == 4
    assert len(orbid.items) == 10
