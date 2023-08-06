# pyhamcrest_metamatchers

[![Documentation Status](https://readthedocs.org/projects/pyhamcrest-metamatchers/badge/?version=latest)](https://pyhamcrest-metamatchers.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.com/ibolit/pyhamcrest_metamatchers.svg?branch=master)](https://travis-ci.com/ibolit/pyhamcrest_metamatchers)

Some matchers for testing pyhamcrest-style matchers.

For now, we have only one of them. More to come.

This is a short example of the usage (with pytest):

```python
    def test_wrong_status_with_wrong_headers(self, response_200):
        assert_that(
            status(300).with_headers({"Hello-Dude": "application/json"}),
            doesnt_match(response_200)
                .with_description(
                    "An HttpResponse object with status_code <300>, "
                    "with headers: \"Hello-Dude: 'application/json'\".")
                .with_mismatch_description(
                    "Status code was: <200>. Does not contain header <Hello-Dude>.")
        )
```

It might, in fact, be a good idea to write a test for these matchers using these matchers.
