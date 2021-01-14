import pytest
from helper_functions.cdk_synth_helper import (
    find_type, get_type, get_cdk_construct_template
)


def test_lambda_functions():
    template = get_cdk_construct_template(
        dict(
            key="value"
        )
    )

    assert find_type(template, "AWS::Lambda::Function") == True
    assert len(get_type(template, "AWS::Lambda::Function")) == 2