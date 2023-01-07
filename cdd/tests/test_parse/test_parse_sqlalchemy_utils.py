"""
Tests for the utils that is used by the SQLalchemy parsers
"""

from copy import deepcopy
from unittest import TestCase

from cdd.parse.utils.sqlalchemy_utils import (
    column_call_name_manipulator,
    column_call_to_param,
)
from cdd.tests.mocks.json_schema import config_schema
from cdd.tests.mocks.sqlalchemy import (
    dataset_primary_key_column_assign,
    node_fk_call,
    node_fk_name_param,
)
from cdd.tests.utils_for_tests import unittest_main


class TestParseSqlAlchemyUtils(TestCase):
    """
    Tests the SQLalchemy parser utilities
    """

    def test_column_call_to_param_pk(self) -> None:
        """
        Tests that `parse.sqlalchemy.utils.column_call_to_param` works with PK
        """

        gold_name, gold_param = (
            lambda _name: (
                _name,
                {
                    "default": config_schema["properties"][_name]["default"],
                    "typ": "str",
                    "doc": config_schema["properties"][_name]["description"],
                },
            )
        )("dataset_name")
        gen_name, gen_param = column_call_to_param(
            column_call_name_manipulator(
                deepcopy(dataset_primary_key_column_assign.value), "add", gold_name
            )
        )
        self.assertEqual(gold_name, gen_name)
        self.assertDictEqual(gold_param, gen_param)

    def test_column_call_to_param_fk(self) -> None:
        """
        Tests that `parse.sqlalchemy.utils.column_call_to_param` works with FK
        """
        gen_name, gen_param = column_call_to_param(deepcopy(node_fk_call))
        gold_name, gold_param = node_fk_name_param
        self.assertEqual(gold_name, gen_name)
        self.assertDictEqual(gold_param, gen_param)

    def test_column_call_to_param_not_implemented(self) -> None:
        """
        Tests that `parse.sqlalchemy.utils.column_call_to_param` raises `NotImplementedError`
        """
        call = deepcopy(node_fk_call)
        call.args[2].func.id = "NotFound"
        self.assertRaises(NotImplementedError, column_call_to_param, call)


unittest_main()