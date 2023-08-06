import pytest

from shuttlis.time import MilitaryTime, TimeDelta, WeekDay


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


@pytest.mark.parametrize('mta,mtr', [
    (MilitaryTime(1320) + TimeDelta(1, 20), MilitaryTime(1440)),
    (MilitaryTime(1320) + TimeDelta(0, 40), MilitaryTime(1400)),
])
def test_military_time_add(mta, mtr):
    assert mtr == mta


@pytest.mark.parametrize('mts,mtr', [
    (MilitaryTime(1320) - TimeDelta(1, 20), MilitaryTime(1200)),
    (MilitaryTime(1320) - TimeDelta(0, 40), MilitaryTime(1240)),
])
def test_military_time_sub(mts, mtr):
    assert mtr == mts


def test_military_time_inequality():
    assert MilitaryTime(1000) != MilitaryTime(900)


def test_weekday_eq():
    assert WeekDay.MONDAY == WeekDay.MONDAY


@pytest.mark.parametrize('first,snd', [
    (WeekDay.MONDAY, WeekDay.TUESDAY),
    (WeekDay.MONDAY, WeekDay.SUNDAY),
])
def test_weekday_lt(first, snd):
    assert first < snd


def test_weekday_str_conversion():
    assert str(WeekDay.SUNDAY) == 'SUNDAY'


def test_time_delta_with_only_minutes():
    assert MilitaryTime(1359) == MilitaryTime(1300) + TimeDelta(min=59)


def test_hash_of_military_times():
    assert 2 == len({MilitaryTime(900), MilitaryTime(1000)})


def test_hash_of_same_military_time():
    assert 1 == len({MilitaryTime(900), MilitaryTime(900)})


def test_mt_in_list():
    assert MilitaryTime(900) in [MilitaryTime(900), MilitaryTime(1000)]

def test_mt_not_in_list():
    assert MilitaryTime(910) not in [MilitaryTime(900), MilitaryTime(1000)]
