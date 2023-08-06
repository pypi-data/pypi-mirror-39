import pytest

from shuttlis.time import MilitaryTime, TimeDelta


@pytest.mark.parametrize('hr,min', [(1, 20), (23, 59), (0, 0)])
def test_military_time_constructor(hr, min):
    mt = MilitaryTime.from_hr_min(hr, min)
    assert 4 == len(str(mt))
    assert hr == mt.hr
    assert min == mt.min


@pytest.mark.parametrize('hr,min', [(24, 00), (12, 61)])
def test_military_time_constructor_fails_when_hr_or_min_are_out_of_range(hr, min):
    with pytest.raises(AssertionError) as e:
        MilitaryTime.from_hr_min(hr, min)


@pytest.mark.parametrize('mt,td,mtr', [
    (MilitaryTime(1320), TimeDelta(1, 20), MilitaryTime(1440)),
    (MilitaryTime(1320), TimeDelta(0, 40), MilitaryTime(1400)),
])
def test_military_time_add(mt, td, mtr):
    assert mtr == mt + td


@pytest.mark.parametrize('mt,td,mtr', [
    (MilitaryTime(1320), TimeDelta(1, 20), MilitaryTime(1200)),
    (MilitaryTime(1320), TimeDelta(0, 40), MilitaryTime(1240)),
])
def test_military_time_sub(mt, td, mtr):
    assert mtr == mt + td
