from pyhamcrest_toolbox.multicomponent import (
    MatcherPlugin,
    MulticomponentMatcher
)
from pyhamcrest_toolbox.util import get_mismatch_description, get_description


class MatchesPlugin(MatcherPlugin):
    def __init__(self, value, must_match=True):
        super().__init__()
        self.value = value
        self.must_match = must_match
        self.actual_match_result = None


    def component_matches(self, matcher):
        self.actual_match_result = matcher._matches(self.value) == self.must_match
        return self.actual_match_result


    def describe_to(self, description):
        description.append_text("A matcher that {} the item".format(
            "matches" if self.must_match else "does not match"))


    def describe_component_mismatch(self, item, mismatch_description):
        mismatch_description.append_text("the matcher {}the item".format(
            "matched " if self.actual_match_result else "did not match "
        ))


class DescriptionPlugin(MatcherPlugin):
    def __init__(self, a_description):
        super().__init__()
        self.description = a_description
        self.wrong_description = None


    def component_matches(self, matcher):
        descr = get_description(matcher)
        descr_is_correct = descr == self.description
        if not descr_is_correct:
            self.wrong_description = descr
            return False
        return True


    def describe_to(self, description):
        description.append_text(
            "with the description: <{}>".format(self.description))


    def describe_component_mismatch(self, item, mismatch_description):
        mismatch_description.append_text("the description was <{}>".format(
            self.wrong_description))


class MismatchDescriptionPlugin(MatcherPlugin):
    def __init__(self, value, a_mismatch_description):
        super().__init__()
        self.value = value
        self.mismatch_description = a_mismatch_description
        self.wrong_mismatch_description = None


    def component_matches(self, matcher):
        descr = get_mismatch_description(matcher, self.value)
        descr_is_correct = descr == self.mismatch_description
        if not descr_is_correct:
            self.wrong_mismatch_description = descr
            return False
        return True


    def describe_to(self, description):
        description.append_text(
            "with the mismatch description: <{}>".format(
                self.mismatch_description))


    def describe_component_mismatch(self, item, mismatch_description):
        mismatch_description.append_text(
            "the mismatch description was <{}>".format(
                self.wrong_mismatch_description))


class MetaMatcher(MulticomponentMatcher):
    def __init__(self, value, must_match=True):
        super().__init__()
        self.value = value
        self.must_match = must_match
        self.register(MatchesPlugin(value, must_match))


    def with_description(self, a_description):
        self.register(DescriptionPlugin(a_description))
        return self


    def with_mismatch_description(self, a_mismatch_description):
        if self.must_match:
            raise RuntimeError("The matcher is expected to match, but a mismatch was specified.")
        self.register(MismatchDescriptionPlugin(self.value, a_mismatch_description))
        return self


def matches(a_value):
    """Checks that the matcher under test matches the value

    :param a_value: The value that needs to be checked.
    :return: :py:class:`pyhamcrest_metamatchers.metamatchers.MetaMatcher<MetaMatcher>`
    """
    return MetaMatcher(a_value, True)


def doesnt_match(a_value):
    """Checks that the matcher under test doesn't match the value

    :param a_value: The matcher that needs to be checked.
    :return: :py:class:`pyhamcrest_metamatchers.metamatchers.MetaMatcher<MetaMatcher>`
    """
    return MetaMatcher(a_value, False)
