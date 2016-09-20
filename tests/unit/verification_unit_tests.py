import pytest

from pock.verification import VerificationBuilder


class FakeMock(object):
    def __init__(self):
        self._property_expectations = []


@pytest.fixture
def verification_builder():
    return VerificationBuilder(mock=FakeMock())


@pytest.fixture
def match_criteria_ready_verification_builder(verification_builder):
    """ :type verification_builder: VerificationBuilder """
    getattr(verification_builder, 'somethingsomething')
    return verification_builder


def test_getattribute_for_the_first_time_sets_name(verification_builder):
    """ :type verification_builder: VerificationBuilder """
    name = 'some_name'
    getattr(verification_builder, name)
    assert verification_builder.name == name


def test_get_attribute_for_the_second_time_reverts_to_typical_usage(match_criteria_ready_verification_builder):
    """ :type match_criteria_ready_verification_builder: VerificationBuilder """
    with pytest.raises(AttributeError):
        getattr(match_criteria_ready_verification_builder, 'there_is_no_way_this_exists')


