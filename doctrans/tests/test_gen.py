""" Tests for gen """

import os
import sys
from ast import (
    ImportFrom,
    alias,
    ClassDef,
    Load,
    Name,
    Expr,
    Assign,
    Store,
    FunctionDef,
    arguments,
    arg,
    Attribute,
)
from copy import deepcopy
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase

from doctrans.ast_utils import set_value
from doctrans.gen import gen
from doctrans.pure_utils import tab
from doctrans.source_transformer import to_code
from doctrans.tests.utils_for_tests import unittest_main


def populate_files(tempdir, input_str=None):
    """
    Populate files in the tempdir

    :param tempdir: Temporary directory
    :type tempdir: ```str```

    :param input_str: Input string to write to the input_filename
    :type input_str: ```Optional[str]```

    :return: input filename, input str, expected_output
    :rtype: ```Tuple[str, str, str]```
    """
    input_filename = os.path.join(tempdir, "input.py")

    input_str = input_str or (
        "class Foo(object):\n"
        '{tab}"""\n{tab}The amazing Foo\n\n'
        "{tab}:cvar a: An a\n"
        "{tab}:cvar b: A b\n"
        '{tab}"""\n'
        "{tab}a = 5\n"
        "{tab}b = 16\n\n\n"
        "input_map = {{'Foo': Foo}}\n".format(tab=tab)
    )
    # expected_output_class_str = (
    #     "class FooConfig(object):\n"
    #     '    """\n'
    #     "    The amazing Foo\n\n"
    #     "    :cvar a: An a. Defaults to 5\n"
    #     '    :cvar b: A b. Defaults to 16"""\n'
    #     "    a = 5\n"
    #     "    b = 16\n\n"
    #     "    def __call__(self):\n"
    #     "        self.a = 5\n"
    #     "        self.b = 16\n"
    # )
    expected_class_ast = ClassDef(
        name="FooConfig",
        bases=[Name("object", Load())],
        keywords=[],
        body=[
            Expr(
                set_value(
                    "\n    The amazing Foo\n\n"
                    "    :cvar a: An a. Defaults to 5\n"
                    "    :cvar b: A b. Defaults to 16"
                )
            ),
            Assign(
                targets=[Name("a", Store())],
                value=set_value(value=5),
                expr=None,
                lineno=None,
            ),
            Assign(
                targets=[Name("b", Store())],
                value=set_value(value=16),
                expr=None,
                lineno=None,
            ),
            FunctionDef(
                name="__call__",
                args=arguments(
                    posonlyargs=[],
                    args=[
                        arg(arg="self", expr=None, identifier_arg=None, annotation=None)
                    ],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[],
                    arg=None,
                    vararg=None,
                    kwarg=None,
                ),
                body=[
                    Assign(
                        targets=[Attribute(Name("self", Load()), "a", Store())],
                        value=set_value(value=5),
                        expr=None,
                        lineno=None,
                    ),
                    Assign(
                        targets=[Attribute(Name("self", Load()), "b", Store())],
                        value=set_value(value=16),
                        expr=None,
                        lineno=None,
                    ),
                ],
                decorator_list=[],
                arguments_args=None,
                identifier_name=None,
                stmt=None,
                lineno=None,
            ),
        ],
        decorator_list=[],
        expr=None,
        identifier_name=None,
    )
    expected_output = "PREPENDED\n{}".format(to_code(expected_class_ast))

    with open(input_filename, "wt") as f:
        f.write(input_str)
    return input_filename, input_str, expected_output


class TestGen(TestCase):
    """ Test class for gen.py """

    sys_path = deepcopy(sys.path)
    tempdir = None

    @classmethod
    def setUpClass(cls) -> None:
        """ Construct temporary module for use by tests """
        cls.tempdir = mkdtemp()
        temp_module_dir = os.path.join(cls.tempdir, "gen_test_module")
        os.mkdir(temp_module_dir)
        (cls.input_filename, cls.input_str, cls.expected_output) = populate_files(
            temp_module_dir
        )
        with open(os.path.join(temp_module_dir, "__init__.py"), "w") as f:
            f.write(
                to_code(
                    ImportFrom(
                        module="input",
                        names=[
                            alias(
                                name="*",
                                asname=None,
                                identifier=None,
                                identifier_name=None,
                            )
                        ],
                        level=1,
                        identifier=None,
                    )
                )
            )

        sys.path.append(cls.tempdir)

    @classmethod
    def tearDownClass(cls) -> None:
        """ Drop the new module from the path and delete the temporary directory """
        sys.path = cls.sys_path
        rmtree(cls.tempdir)

    def test_gen(self) -> None:
        """ Tests `gen` """

        output_filename = os.path.join(self.tempdir, "test_gen_output.py")
        self.assertIsNone(
            gen(
                name_tpl="{name}Config",
                input_mapping="gen_test_module.input_map",
                type_="class",
                output_filename=output_filename,
                prepend="PREPENDED\n",
            )
        )
        with open(output_filename, "rt") as f:
            self.assertEqual(f.read(), self.expected_output)

    def test_gen_with_imports_from_file(self) -> None:
        """ Tests `gen` with `imports_from_file` """

        output_filename = os.path.join(
            self.tempdir, "test_gen_with_imports_from_file_output.py"
        )
        self.assertIsNone(
            gen(
                name_tpl="{name}Config",
                input_mapping="gen_test_module.input_map",
                imports_from_file="gen_test_module",
                type_="class",
                output_filename=output_filename,
            )
        )
        with open(output_filename, "rt") as f:
            self.assertEqual(
                f.read(),
                self.expected_output.replace(
                    "PREPENDED\n",
                    to_code(
                        ImportFrom(
                            module="input",
                            names=[
                                alias(
                                    name="*",
                                    asname=None,
                                    identifier=None,
                                    identifier_name=None,
                                )
                            ],
                            level=1,
                            identifier=None,
                        )
                    ),
                ),
            )


unittest_main()