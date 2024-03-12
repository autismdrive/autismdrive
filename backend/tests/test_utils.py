from unittest import TestCase

from math import floor

from app.utils import snake_case_it, pascal_case_it, get_random_integer


class TestUtils(TestCase):
    def test_should_generate_unique_random_integers(self):
        num_ints = 1000000  # 1 million
        ints = [get_random_integer() for _ in range(num_ints)]
        for i in ints:
            self.assertIsNotNone(i)
            self.assertIsInstance(i, int)
            self.assertGreaterEqual(i, 100)
            self.assertLessEqual(i, 2147483647)

        # There should be no duplicates
        self.assertEqual(num_ints, len(set(ints)))

    def test_should_convert_string_to_pascal_case(self):
        test_cases = [
            ("", ""),
            ("a_bc", "ABc"),
            ("a_b123", "AB123"),
            ("some_variable_name", "SomeVariableName"),
            ("some_variable_name_abc", "SomeVariableNameAbc"),
            ("abc123_something_else", "Abc123SomethingElse"),
            ("ABC_123_SomethingElse", "Abc123SomethingElse"),
            ("ABC_123_SOMETHING_ELSE", "Abc123SomethingElse"),
        ]

        for input_str, expected_output_str in test_cases:
            with self.subTest(input_str=input_str, expected_output_str=expected_output_str):
                self.assertEqual(pascal_case_it(input_str), expected_output_str)

    def test_should_convert_string_to_snake_case(self):
        test_cases = [
            ("", ""),
            ("aBc", "a_bc"),
            ("aB123", "a_b123"),
            ("SomeVariableName", "some_variable_name"),
            ("SomeVariableNameABC", "some_variable_name_abc"),
            ("ABC123SomethingElse", "abc123_something_else"),
            ("ABC_123_SomethingElse", "abc_123_something_else"),
            ("ABC_123_SOMETHING_ELSE", "abc_123_something_else"),
            ("_WhatDoesThisDo_", "_what_does_this_do_"),
            ("____WhatDoesThisDo____", "____what_does_this_do____"),
        ]

        for input_str, expected_output_str in test_cases:
            with self.subTest(input_str=input_str, expected_output_str=expected_output_str):
                self.assertEqual(snake_case_it(input_str), expected_output_str)

    def test_raise_exception_when_converting_nonstring_to_snake_case(self):
        test_cases = [
            None,
            True,
            1,
            1.0,
            [],
            (),
        ]

        for input in test_cases:
            with self.subTest(input=input):
                with self.assertRaises(TypeError):
                    snake_case_it(input)
