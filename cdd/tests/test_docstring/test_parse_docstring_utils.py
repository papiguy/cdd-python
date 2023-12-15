"""
Tests for cdd.docstring.utils.parse_utils
"""

from unittest import TestCase

from cdd.docstring.utils.parse_utils import parse_adhoc_doc_for_typ
from cdd.tests.utils_for_tests import unittest_main


class TestParseDocstringUtils(TestCase):
    """
    Tests whether the intermediate representation is consistent when parsed from different inputs.

    IR is a dictionary consistent with `IntermediateRepr`, defined as:
        ParamVal = TypedDict("ParamVal", {"typ": str, "doc": Optional[str], "default": Any})
        IntermediateRepr = TypedDict("IntermediateRepr", {
            "name": Optional[str],
            "type": Optional[str],
            "doc": Optional[str],
            "params": OrderedDict[str, ParamVal],
            "returns": Optional[OrderedDict[Literal["return_type"], ParamVal]],
        })
    """

    def test_parse_adhoc_doc_for_typ(self) -> None:
        """
        Test that `parse_adhoc_doc_for_typ` works for various found-in-wild Keras variants
        """
        # deque(
        #     map(
        #         lambda output_input: self.assertEqual(
        #             output_input[0], parse_adhoc_doc_for_typ(output_input[1], name="")
        #         ),
        #         (
        #             (
        #                 "str",
        #                 class_google_keras_tensorboard_ir["params"]["log_dir"]["doc"],
        #             ),
        #             (
        #                 "int",
        #                 class_google_keras_tensorboard_ir["params"]["histogram_freq"][
        #                     "doc"
        #                 ],
        #             ),
        #             ("Union[list,tuple]", "A list/tuple"),
        #             (
        #                 "Union[Literal['batch', 'epoch'], int]",
        #                 class_google_keras_tensorboard_ir["params"]["update_freq"][
        #                     "doc"
        #                 ],
        #             ),
        #             (
        #                 "int",
        #                 "Explicit `int64`-castable monotonic step value for this summary.",
        #             ),
        #             (
        #                 "bool",
        #                 cdd.shared.docstring_parsers.parse_docstring(
        #                     docstring_google_keras_tensorboard_return_str
        #                 )["returns"]["return_type"]["typ"],
        #             ),
        #             (
        #                 "Literal['auto', 'max', 'min']",
        #                 "String. One of `{'auto', 'min', 'max'}`. In `'min'` mode,",
        #             ),
        #             (
        #                 'Union[Literal["epoch"], bool, int]',
        #                 '`"epoch"`, integer, or `False`.'
        #                 'When set to `"epoch" the callback saves the checkpoint at the end of each epoch.',
        #             ),
        #         ),
        #     ),
        #     maxlen=0,
        # )

        self.assertEqual(
            ("Optional[int]", "Int or None, defaults to None."),
            parse_adhoc_doc_for_typ("Int or None, defaults to None.", name=""),
        )


unittest_main()
