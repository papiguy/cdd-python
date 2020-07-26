"""
Tests for the Intermediate Representation
"""
from ast import FunctionDef, Expr, Constant
from unittest import TestCase, main as unittest_main

from doctrans import docstring_struct
from doctrans.docstring_struct import to_docstring
from doctrans.tests.mocks.argparse import argparse_func_ast
from doctrans.tests.mocks.classes import class_ast
from doctrans.tests.mocks.docstrings import docstring_structure, docstring_str, docstring_structure_no_default_doc
from doctrans.tests.mocks.methods import class_with_method_ast


class TestIntermediateRepresentation(TestCase):
    """
    Tests whether the intermediate representation is consistent when parsed from different inputs.

    IR is a dictionary of form:
              {
                  'short_description': ...,
                  'long_description': ...,
                  'params': [{'name': ..., 'typ': ..., 'doc': ..., 'default': ..., 'required': ... }, ...],
                  "returns': {'name': ..., 'typ': ..., 'doc': ..., 'default': ..., 'required': ... }
              }
    """

    def test_from_argparse_ast(self) -> None:
        """
        Tests whether `from_argparse_ast` produces `docstring_structure_no_default_doc`
              from `argparse_func_ast` """
        self.assertDictEqual(docstring_struct.from_argparse_ast(argparse_func_ast, emit_default_doc=False),
                             docstring_structure_no_default_doc)

    def test_from_argparse_ast_fails(self) -> None:
        """
        Tests whether `argparse_ast2docstring_structure` produces `docstring_structure_no_default_doc`
              from `argparse_func_ast` """
        self.assertRaises(NotImplementedError,
                          lambda: docstring_struct.from_argparse_ast(FunctionDef(body=[
                              Expr(value=Constant(value='wow', kind='choco'))])),
                          )

    def test_from_class(self) -> None:
        """
        Tests whether `from_class` produces `docstring_structure`
              from `class_ast` """
        self.assertDictEqual(docstring_struct.from_class(class_ast),
                             docstring_structure)

    def test_from_class_with_method(self) -> None:
        """
        Tests whether `from_class_with_method` produces `docstring_structure`
              from `class_with_method_ast` """
        self.assertDictEqual(
            docstring_struct.from_class_with_method(class_with_method_ast, 'method_name',
                                                    emit_default_doc=False),
            docstring_structure_no_default_doc
        )

    # Commented out as `ast.parse` isn't extracting the return type in the `def f() -> bool` form.
    '''
    def test_class_with_method2docstring_structure_inline_types(self) -> None:
        """
        Tests whether `class_with_method2docstring_structure` produces `docstring_structure`
              from `class_with_method_types_ast` """
        self.assertDictEqual(
            docstring_struct.from_class_with_method(class_with_method_types_ast, 'method_name',
                                                    emit_default_doc=False),
            docstring_structure
        )
    '''

    def test_from_docstring(self) -> None:
        """
        Tests whether `from_docstring` produces `docstring_structure`
              from `docstring_str` """
        _docstring_structure, returns = docstring_struct.from_docstring(docstring_str, return_tuple=True)
        self.assertTrue(returns)
        self.assertDictEqual(_docstring_structure,
                             docstring_structure)

    def test_to_docstring_fails(self) -> None:
        """
        Tests to_docstring failure conditions
        """
        self.assertRaises(NotImplementedError,
                          lambda: to_docstring(docstring_str,
                                               docstring_format='numpy'))


if __name__ == '__main__':
    unittest_main()
