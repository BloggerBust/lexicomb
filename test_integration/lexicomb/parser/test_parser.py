import unittest
from numbers import Number
from test_integration.helper import Helper
from enum import Enum
helper = Helper()


class Interpret(Enum):
    DO_NOT_INTERPRET = 0
    RETURN_EVAL = 1
    RETURN_RESULT = 2
    RETURN_FRAME = 3


class TestParser(unittest.TestCase):
    def setUp(self):
        self._helper = helper

    def test_parser_given_number_expect_real_number_artifact(self):
        cases = [
            ("0", self._helper.lexicomb_ioc.real_number_factory_provider("0")),
            ("9", self._helper.lexicomb_ioc.real_number_factory_provider("9")),
            ("42.42", self._helper.lexicomb_ioc.real_number_factory_provider("42.42")),
            ("00045.1000", self._helper.lexicomb_ioc.real_number_factory_provider("00045.1000")),
        ]

        self._evaluate(self._helper.lexicomb_parser.arethmatic_expression, cases)

    def test_parser_given_name_expect_variable_artifact(self):
        cases = [
            ("x", self._create_term("x")),
            ("my_var", self._create_term("my_var")),
            ("myVar", self._create_term("myVar")),
            ("MY_VAR", self._create_term("MY_VAR")),
            ("x0123456789", self._create_term("x0123456789")),
            ("MY_VAR_1", self._create_term("MY_VAR_1"))
        ]

        self._evaluate(self._helper.lexicomb_parser.arethmatic_expression, cases)

    def test_parser_given_arethmatic_expression_expect_matching_arethmatic_expression_ast(self):
        cases = [
            ("1 + 42", self._create_arethmatic_binary_operator("+", "1", "42")),
            ("1 - 42", self._create_arethmatic_binary_operator("-", "1", "42")),
            ("1 * 42", self._create_arethmatic_binary_operator("*", "1", "42")),
            ("1 / 42", self._create_arethmatic_binary_operator("/", "1", "42")),
            ("x + y", self._create_arethmatic_binary_operator("+", "x", "y")),
            ("x - y", self._create_arethmatic_binary_operator("-", "x", "y")),
            ("x * y", self._create_arethmatic_binary_operator("*", "x", "y")),
            ("x / y", self._create_arethmatic_binary_operator("/", "x", "y")),
        ]

        self._evaluate(self._helper.lexicomb_parser.arethmatic_expression, cases)

    def test_parser_given_arethmatic_expression_expect_arethmatic_expression_ast_with_correct_precedence(self):
        cases = [
            ("3 + 4 + 2", self._create_arethmatic_binary_operator(
                "+", self._create_arethmatic_binary_operator(
                    "+", "3", "4"), "2")),
            ("3 + 4 - 2", self._create_arethmatic_binary_operator(
                "-", self._create_arethmatic_binary_operator(
                    "+", "3", "4"), "2")),
            ("3 - 4 - 2", self._create_arethmatic_binary_operator(
                "-", self._create_arethmatic_binary_operator(
                    "-", "3", "4"), "2")),
            ("3 * 4 + 2", self._create_arethmatic_binary_operator(
                "+", self._create_arethmatic_binary_operator(
                    "*", "3", "4"), "2")),
            ("3 + 4 * 2", self._create_arethmatic_binary_operator(
                "+", "3", self._create_arethmatic_binary_operator(
                    "*", "4", "2"))),
            ("3 * 4 * 2", self._create_arethmatic_binary_operator(
                "*", self._create_arethmatic_binary_operator(
                    "*", "3", "4"), "2")),
            ("3 / 4 * 2", self._create_arethmatic_binary_operator(
                "*", self._create_arethmatic_binary_operator(
                    "/", "3", "4"), "2")),
            ("3 * 4 / 2", self._create_arethmatic_binary_operator(
                "/", self._create_arethmatic_binary_operator(
                    "*", "3", "4"), "2")),
            ("3 / 4 / 2", self._create_arethmatic_binary_operator(
                "/", self._create_arethmatic_binary_operator(
                    "/", "3", "4"), "2")),
            ("3 + 4 * 2 / 2", self._create_arethmatic_binary_operator(
                "+", "3", self._create_arethmatic_binary_operator(
                    "/", self._create_arethmatic_binary_operator(
                        "*", "4", "2"), "2")))
        ]

        self._evaluate(self._helper.lexicomb_parser.arethmatic_expression, cases)

    def test_parser_given_parenthesised_arethmatic_expression_expect_un_grouped_arethmatic_expression_ast_with_correct_prededence(self):
        cases = [
            ("(0)", self._helper.lexicomb_ioc.real_number_factory_provider("0")),
            ("((925.32))", self._helper.lexicomb_ioc.real_number_factory_provider("925.32")),
            ("(1 + 42)", self._create_arethmatic_binary_operator("+", "1", "42")),
            ("(1 + 42) * 3", self._create_arethmatic_binary_operator("*",
                                                                     self._create_arethmatic_binary_operator("+", "1", "42"), "3")),
            ("(1 / 42) - 3", self._create_arethmatic_binary_operator("-",
                                                                     self._create_arethmatic_binary_operator("/", "1", "42"), "3")),
            ("3 / (1 - 42)", self._create_arethmatic_binary_operator("/",
                                                                     "3", self._create_arethmatic_binary_operator("-", "1", "42"))),
            ("(3-42) * (1 + 42)", self._create_arethmatic_binary_operator(
                "*", self._create_arethmatic_binary_operator(
                    "-", "3", "42"), self._create_arethmatic_binary_operator(
                        "+", "1", "42"))),
            ("10 / (2 * (1 + 42)) * (3 + 9)", self._create_arethmatic_binary_operator(
                "*", self._create_arethmatic_binary_operator(
                    "/", "10", self._create_arethmatic_binary_operator(
                        "*", "2", self._create_arethmatic_binary_operator(
                            "+", "1", "42"))),
                self._create_arethmatic_binary_operator(
                    "+", "3", "9")))
        ]

        self._evaluate(self._helper.lexicomb_parser.arethmatic_expression, cases)

    def test_parser_gven_relational_expression_expect_relational_expression_ast(self):
        cases = [
            ("4 < 5", self._create_relational_binary_operator("<", "4", "5")),
            ("4 <= 5", self._create_relational_binary_operator("<=", "4", "5")),
            ("5 > 4", self._create_relational_binary_operator(">", "5", "4")),
            ("5 >= 4", self._create_relational_binary_operator(">=", "5", "4")),
            ("5 = 5", self._create_relational_binary_operator("=", "5", "5")),
            ("5 != 4", self._create_relational_binary_operator("!=", "5", "4"))
        ]

        self._evaluate(self._helper.lexicomb_parser.relational_expression, cases)

    def test_parser_gven_relational_expression_expect_relational_expression_ast_with_correct_precedence(self):
        cases = [
            ("4 < 5 < 6", self._create_relational_binary_operator(
                "<", self._create_relational_binary_operator("<", "4", "5"), "6")),
            ("4 < 5 <= 6", self._create_relational_binary_operator(
                "<=", self._create_relational_binary_operator("<", "4", "5"), "6")),
            ("4 < 5 = 6", self._create_relational_binary_operator(
                "=", self._create_relational_binary_operator("<", "4", "5"), "6")),
            ("4 < 5 >= 6", self._create_relational_binary_operator(
                ">=", self._create_relational_binary_operator("<", "4", "5"), "6")),
            ("4 < 5 > 6", self._create_relational_binary_operator(
                ">", self._create_relational_binary_operator("<", "4", "5"), "6")),

            ("4 <= 5 < 6", self._create_relational_binary_operator(
                "<", self._create_relational_binary_operator("<=", "4", "5"), "6")),
            ("4 <= 5 <= 6", self._create_relational_binary_operator(
                "<=", self._create_relational_binary_operator("<=", "4", "5"), "6")),
            ("4 <= 5 = 6", self._create_relational_binary_operator(
                "=", self._create_relational_binary_operator("<=", "4", "5"), "6")),
            ("4 <= 5 >= 6", self._create_relational_binary_operator(
                ">=", self._create_relational_binary_operator("<=", "4", "5"), "6")),
            ("4 <= 5 > 6", self._create_relational_binary_operator(
                ">", self._create_relational_binary_operator("<=", "4", "5"), "6")),

            ("4 = 5 < 6", self._create_relational_binary_operator(
                "<", self._create_relational_binary_operator("=", "4", "5"), "6")),
            ("4 = 5 <= 6", self._create_relational_binary_operator(
                "<=", self._create_relational_binary_operator("=", "4", "5"), "6")),
            ("4 = 5 = 6", self._create_relational_binary_operator(
                "=", self._create_relational_binary_operator("=", "4", "5"), "6")),
            ("4 = 5 >= 6", self._create_relational_binary_operator(
                ">=", self._create_relational_binary_operator("=", "4", "5"), "6")),
            ("4 = 5 > 6", self._create_relational_binary_operator(
                ">", self._create_relational_binary_operator("=", "4", "5"), "6")),

            ("4 >= 5 < 6", self._create_relational_binary_operator(
                "<", self._create_relational_binary_operator(">=", "4", "5"), "6")),
            ("4 >= 5 <= 6", self._create_relational_binary_operator(
                "<=", self._create_relational_binary_operator(">=", "4", "5"), "6")),
            ("4 >= 5 = 6", self._create_relational_binary_operator(
                "=", self._create_relational_binary_operator(">=", "4", "5"), "6")),
            ("4 >= 5 >= 6", self._create_relational_binary_operator(
                ">=", self._create_relational_binary_operator(">=", "4", "5"), "6")),
            ("4 >= 5 > 6", self._create_relational_binary_operator(
                ">", self._create_relational_binary_operator(">=", "4", "5"), "6")),

            ("4 > 5 < 6", self._create_relational_binary_operator(
                "<", self._create_relational_binary_operator(">", "4", "5"), "6")),
            ("4 > 5 <= 6", self._create_relational_binary_operator(
                "<=", self._create_relational_binary_operator(">", "4", "5"), "6")),
            ("4 > 5 = 6", self._create_relational_binary_operator(
                "=", self._create_relational_binary_operator(">", "4", "5"), "6")),
            ("4 > 5 >= 6", self._create_relational_binary_operator(
                ">=", self._create_relational_binary_operator(">", "4", "5"), "6")),
            ("4 > 5 > 6", self._create_relational_binary_operator(
                ">", self._create_relational_binary_operator(">", "4", "5"), "6")),

        ]

        self._evaluate(self._helper.lexicomb_parser.relational_expression, cases)

    def test_parser_gven_parenthesised_relational_expression_expect_parenthesised_relational_expression_ast(self):
        cases = [
            ("(4 < 5)", self._create_relational_binary_operator("<", "4", "5")),
            ("(4 < 5) > 6", self._create_relational_binary_operator(
                ">", self._create_relational_binary_operator("<", "4", "5"), "6")),
            ("4 < (5 > 6)", self._create_relational_binary_operator(
                "<", "4", self._create_relational_binary_operator(">", "5", "6"))),
            ("(4 < 5 > 6)", self._create_relational_binary_operator(
                ">", self._create_relational_binary_operator("<", "4", "5"), "6")),

        ]

        self._evaluate(self._helper.lexicomb_parser.relational_expression, cases)

    def test_parser_gven_unary_negation_relational_expression_expect_unary_negation_relational_expression_ast(self):
        cases = [
            ("!4 < 5", self._create_unary_operator(
                "!", self._create_relational_binary_operator("<", "4", "5"))),
            ("!(4 < 5)", self._create_unary_operator(
                "!", self._create_relational_binary_operator("<", "4", "5"))),
            ("(!4 < 5)", self._create_unary_operator(
                "!", self._create_relational_binary_operator("<", "4", "5"))),
            ("!(!4 < 5)", self._create_unary_operator("!", self._create_unary_operator(
                "!", self._create_relational_binary_operator("<", "4", "5")))),

            ("!4 < 5 > 6", self._create_unary_operator(
                "!", self._create_relational_binary_operator(">", self._create_relational_binary_operator("<", "4", "5"), "6"))),
            ("!(4 < 5 > 6)", self._create_unary_operator(
                "!", self._create_relational_binary_operator(">", self._create_relational_binary_operator("<", "4", "5"), "6"))),
            ("!(4 < 5) > 6", self._create_relational_binary_operator(
                ">", self._create_unary_operator("!", self._create_relational_binary_operator("<", "4", "5")), "6")),
            ("(!4 < 5) > 6", self._create_relational_binary_operator(
                ">", self._create_unary_operator("!", self._create_relational_binary_operator("<", "4", "5")), "6")),
            ("!4 < (5 > 6)", self._create_unary_operator("!", self._create_relational_binary_operator(
                "<", "4", self._create_relational_binary_operator(">", "5", "6")))),
            ("4 < !(5 > 6)", self._create_relational_binary_operator(
                "<", "4", self._create_unary_operator("!", self._create_relational_binary_operator(">", "5", "6")))),
            ("4 < (!5 > 6)", self._create_relational_binary_operator(
                "<", "4", self._create_unary_operator("!", self._create_relational_binary_operator(">", "5", "6")))),
        ]

        self._evaluate(self._helper.lexicomb_parser.relational_expression, cases)

    def test_parser_gven_logical_expression_expect_logical_expression_ast(self):
        cases = [
            ("5 && 6 ", self._create_logical_binary_operator("&&", "5", "6")),
            ("5 || 6 ", self._create_logical_binary_operator("||", "5", "6")),
        ]

        self._evaluate(self._helper.lexicomb_parser.logical_expression, cases)

    def test_parser_given_logical_expression_expect_logical_expression_ast_with_correct_precedence(self):
        cases = [
            ("5 && 6 && 7", self._create_logical_binary_operator(
                "&&", self._create_logical_binary_operator("&&", "5", "6"), "7")),
            ("5 && 6 || 7", self._create_logical_binary_operator(
                "||", self._create_logical_binary_operator("&&", "5", "6"), "7")),
            ("5 || 6 && 7", self._create_logical_binary_operator(
                "||", "5", self._create_logical_binary_operator("&&", "6", "7"))),
            ("5 || 6 || 7", self._create_logical_binary_operator(
                "||", self._create_logical_binary_operator("||", "5", "6"), "7")),
        ]

        self._evaluate(self._helper.lexicomb_parser.logical_expression, cases)

    def test_parser_given_unary_negation_logical_expression_expect_logical_expression_ast_with_correct_precedence(self):
        cases = [
            ("!5 && 6 && 7", self._create_logical_binary_operator(
                "&&", self._create_logical_binary_operator("&&", self._create_unary_operator("!", "5"), "6"), "7")),
            ("5 && !6 && 7", self._create_logical_binary_operator("&&", self._create_logical_binary_operator(
                "&&", "5", self._create_unary_operator("!", "6")), "7")),
            ("5 && 6 && !7", self._create_logical_binary_operator(
                "&&", self._create_logical_binary_operator("&&", "5", "6"), self._create_unary_operator("!", "7"))),

            ("!5 || 6 && 7", self._create_logical_binary_operator("||", self._create_unary_operator("!", "5"), self._create_logical_binary_operator(
                "&&", "6", "7"))),
            ("5 || !6 && 7", self._create_logical_binary_operator("||", "5", self._create_logical_binary_operator(
                "&&", self._create_unary_operator("!", "6"), "7"))),
            ("5 || 6 && !7", self._create_logical_binary_operator(
                "||", "5", self._create_logical_binary_operator("&&", "6", self._create_unary_operator("!", "7")))),

            ("!5 || 6 || 7", self._create_logical_binary_operator(
                "||", self._create_logical_binary_operator("||", self._create_unary_operator("!", "5"), "6"), "7")),
            ("5 || !6 || 7", self._create_logical_binary_operator(
                "||", self._create_logical_binary_operator("||", "5", self._create_unary_operator("!", "6")), "7")),
            ("5 || 6 || !7", self._create_logical_binary_operator(
                "||", self._create_logical_binary_operator("||", "5", "6"), self._create_unary_operator("!", "7"))),

            ("!5 && 6 || 7", self._create_logical_binary_operator("||", self._create_logical_binary_operator(
                "&&", self._create_unary_operator("!", "5"), "6"), "7")),
            ("5 && !6 || 7", self._create_logical_binary_operator("||", self._create_logical_binary_operator(
                "&&", "5", self._create_unary_operator("!", "6")), "7")),
            ("5 && 6 || !7", self._create_logical_binary_operator(
                "||", self._create_logical_binary_operator("&&", "5", "6"), self._create_unary_operator("!", "7"))),
        ]

        self._evaluate(self._helper.lexicomb_parser.logical_expression, cases)

    def test_parser_gven_parenthesised_logical_expression_expect_logical_expression_ast_with_correct_precendence(self):
        cases = [
            ("(4 || 5) && 6", self._create_logical_binary_operator(
                "&&", self._create_logical_binary_operator("||", "4", "5"), "6")),
            ("!(4 || 5) && 6", self._create_logical_binary_operator(
                "&&", self._create_unary_operator("!", self._create_logical_binary_operator("||", "4", "5")), "6")),
            ("(!4 || 5) && 6", self._create_logical_binary_operator(
                "&&", self._create_logical_binary_operator("||", self._create_unary_operator("!", "4"), "5"), "6")),
            ("(4 || !5) && 6", self._create_logical_binary_operator(
                "&&", self._create_logical_binary_operator("||", "4", self._create_unary_operator("!", "5")), "6")),
            ("(4 || 5) && !6", self._create_logical_binary_operator(
                "&&", self._create_logical_binary_operator("||", "4", "5"), self._create_unary_operator("!", "6"))),

            ("4 || (5 && 6)", self._create_logical_binary_operator(
                "||", "4", self._create_logical_binary_operator("&&", "5", "6"))),
            ("!4 || (5 && 6)", self._create_logical_binary_operator(
                "||", self._create_unary_operator("!", "4"), self._create_logical_binary_operator("&&", "5", "6"))),
            ("4 || !(5 && 6)", self._create_logical_binary_operator(
                "||", "4", self._create_unary_operator("!", self._create_logical_binary_operator("&&", "5", "6")))),
            ("4 || (!5 && 6)", self._create_logical_binary_operator(
                "||", "4", self._create_logical_binary_operator("&&", self._create_unary_operator("!", "5"), "6"))),
            ("4 || (5 && !6)", self._create_logical_binary_operator(
                "||", "4", self._create_logical_binary_operator("&&", "5", self._create_unary_operator("!", "6")))),
        ]

        self._evaluate(self._helper.lexicomb_parser.logical_expression, cases)

    def test_parser_gven_mixed_arethmatic_logical_expression_expect_expression_with_correct_precedence(self):
        cases = [
            ("2 + 4 > 4", self._create_relational_binary_operator(">",
                                                                  self._create_arethmatic_binary_operator("+", "2", "4"), "4")),
            ("4 > 4 - 2", self._create_relational_binary_operator(">", "4",
                                                                  self._create_arethmatic_binary_operator("-", "4", "2"))),
            ("4 > 5 / (4-2)", self._create_relational_binary_operator(
                ">", "4", self._create_arethmatic_binary_operator(
                    "/", "5", self._create_arethmatic_binary_operator(
                        "-", "4", "2")))),
            ("1 + 1 * 4 > 5", self._create_relational_binary_operator(
                ">", self._create_arethmatic_binary_operator(
                    "+", "1", self._create_arethmatic_binary_operator(
                        "*", "1", "4")),
                "5")),
            ("!(1 * 4 > (5+2) / 1) || !(2 / 3 + 1 <= 1)", self._create_logical_binary_operator(
                "||", self._create_unary_operator(
                    "!", self._create_relational_binary_operator(
                        ">", self._create_arethmatic_binary_operator(
                            "*", "1", "4"), self._create_arethmatic_binary_operator(
                                "/", self._create_arethmatic_binary_operator(
                                    "+", "5", "2"),
                                "1"))), self._create_unary_operator(
                                    "!", self._create_relational_binary_operator(
                                        "<=", self._create_arethmatic_binary_operator(
                                            "+", self._create_arethmatic_binary_operator(
                                                "/", "2", "3"),
                                            "1"),
                                        "1")))),

        ]

        self._evaluate(self._helper.lexicomb_parser.expression, cases)

    def test_assignment_statement(self):
        cases = [
            ("x := 5;", self._create_assignment_statement("x", self._create_real_number("5"))),
            ("x := y + 2;", self._create_assignment_statement("x",
                                                              self._create_arethmatic_binary_operator("+", self._create_term("y"), "2")))
        ]

        self._evaluate(self._helper.lexicomb_parser.assignment_statement, cases)

    def test_tag_expression(self):
        cases = [
            ("Athlete Trevor", self._create_tag_statement("Athlete", ["Trevor"])),
            ("ExerciseLog Trevor Pushups 3 sets 7 reps 5000 lbs", self._create_tag_statement(
                "ExerciseLog", ["Trevor", "Pushups", "3", "sets", "7", "reps", "5000", "lbs"]))
        ]

        self._evaluate(self._helper.lexicomb_parser._tag_expression, cases)

    def test_tag_statement(self):
        cases = [
            ("Athlete Trevor;", self._create_tag_statement("Athlete", ["Trevor"])),
            ("ExerciseLog Trevor Pushups 3 sets 7 reps 5000 lbs;", self._create_tag_statement(
                "ExerciseLog", ["Trevor", "Pushups", "3", "sets", "7", "reps", "5000", "lbs"]))
        ]

        self._evaluate(self._helper.lexicomb_parser._tag_statement, cases)

    def test_statement_sequence(self):
        cases = [
            ("x := 5; y := 2;", [self._create_assignment_statement("x", self._create_real_number(
                "5")), self._create_assignment_statement("y", self._create_real_number("2"))]),
            ("x := 5; y := 2; not_valid := 5", [self._create_assignment_statement("x", self._create_real_number(
                "5")), self._create_assignment_statement("y", self._create_real_number("2"))]),
            ("x := 1 + 2;", [self._create_assignment_statement("x", self._create_arethmatic_binary_operator(
                "+", self._create_real_number("1"), self._create_real_number("2")))]),
            ("x := 1 < 2;", [self._create_assignment_statement("x", self._create_relational_binary_operator(
                "<", self._create_real_number("1"), self._create_real_number("2")))]),
            ("""
            x := 5;
            y := 2;
            isTrue := x > y;
            """, [
                self._create_assignment_statement("x", self._create_real_number("5")),
                self._create_assignment_statement("y", self._create_real_number("2")),
                self._create_assignment_statement("isTrue", self._create_relational_binary_operator(
                    ">", self._create_term("x"), self._create_term("y")))])
        ]

        self._evaluate(self._helper.lexicomb_parser.statement_sequence, cases)

    def test_block(self):
        cases = [
            ("{ x:=5; }", self._create_statement_block(
                [self._create_assignment_statement("x", self._create_real_number("5"))])),
            ("{ x:=5; y:=2; }", self._create_statement_block([self._create_assignment_statement(
                "x", self._create_real_number("5")), self._create_assignment_statement("y", self._create_real_number("2"))])),
        ]

        self._evaluate(self._helper.lexicomb_parser.statement_block, cases)

    def test_conditional_block(self):
        cases = [
            ("? 1 < 2 { x := 1; }", self._create_conditional_block(self._create_relational_binary_operator(
                "<", "1", "2"), self._create_statement_block([self._create_assignment_statement("x", "1")]))),
            ("? 1 < 2 { x := 1; } { x := 2; }", self._create_conditional_block(self._create_relational_binary_operator("<", "1", "2"), self._create_statement_block(
                [self._create_assignment_statement("x", "1")]), self._create_statement_block([self._create_assignment_statement("x", "2")]))),
            ("? 1 < 2 { x := 1; }? 2 < 3 { y := 3; }", self._create_conditional_block(self._create_relational_binary_operator("<", "1", "2"), self._create_statement_block([self._create_assignment_statement(
                "x", "1")]), self._create_conditional_block(self._create_relational_binary_operator("<", "2", "3"), self._create_statement_block([self._create_assignment_statement("y", "3")])))),
            ("? 1 < 2 { x := 1; }? 2 < 3 { y := 3; }{ z := 5; }", self._create_conditional_block(self._create_relational_binary_operator(
                "<", "1", "2"), self._create_statement_block([
                    self._create_assignment_statement(
                        "x", "1")
                ]), self._create_conditional_block(self._create_relational_binary_operator(
                    "<", "2", "3"),
                self._create_statement_block([
                    self._create_assignment_statement("y", "3")
                ]),
                self._create_statement_block([
                    self._create_assignment_statement("z", "5")
                ]))))
        ]
        self._evaluate(self._helper.lexicomb_parser.conditional_block, cases)

    def test_conditional_repeat_block(self):
        cases = [
            ("@? x < 2 { x := x + 1; }", self._create_conditional_repeat_block(self._create_relational_binary_operator("<", "x", "2"),
                                                                               self._create_statement_block([self._create_assignment_statement("x", self._create_arethmatic_binary_operator("+", "x", "1"))]))),
            ("@? 1 < 2 { x := 1; } { x := 2; }", self._create_conditional_repeat_block(self._create_relational_binary_operator("<", "1", "2"), self._create_statement_block(
                [self._create_assignment_statement("x", "1")]), self._create_statement_block([self._create_assignment_statement("x", "2")]))),
            ("@? 1 < 2 { x := 1; }? 2 < 3 { y := 3; }", self._create_conditional_repeat_block(self._create_relational_binary_operator("<", "1", "2"), self._create_statement_block([self._create_assignment_statement(
                "x", "1")]), self._create_conditional_block(self._create_relational_binary_operator("<", "2", "3"), self._create_statement_block([self._create_assignment_statement("y", "3")])))),
            ("@? 1 < 2 { x := 1; }? 2 < 3 { y := 3; }{ z := 5; }", self._create_conditional_repeat_block(self._create_relational_binary_operator(
                "<", "1", "2"), self._create_statement_block([
                    self._create_assignment_statement("x", "1")
                ]), self._create_conditional_block(self._create_relational_binary_operator("<", "2", "3"),
                                                   self._create_statement_block([
                                                       self._create_assignment_statement("y", "3")
                                                   ]), self._create_statement_block([
                                                       self._create_assignment_statement("z", "5")
                                                   ])))),

        ]

        self._evaluate(self._helper.lexicomb_parser.conditional_repeat_block, cases)

    def test_parser_expect_correct_abstract_syntax_tree(self):
        cases = [
            ("""
            {
              # Comment in statement sequence
              x := 1; # Comment at the end of a line
              y
              # this is ugly, but valid
              := # ugly,
              # but
              x +
              # valid
              1
              ;
              # z := (x + y) / (2 * -1)
              ? y = x {
                # Comment in a statement block
                y := y * x;
              }{
                x := x / y;
              }
            }
            """, self._create_statement_block([
                self._create_assignment_statement("x", "1"),
                self._create_assignment_statement(
                    "y", self._create_arethmatic_binary_operator("+", "x", "1")),
                self._create_conditional_block(self._create_relational_binary_operator("=", "y", "x"),
                                               self._create_statement_block([
                                                   self._create_assignment_statement(
                                                       "y", self._create_arethmatic_binary_operator("*", "y", "x"))
                                               ]),
                                               self._create_statement_block([
                                                   self._create_assignment_statement(
                                                       "x", self._create_arethmatic_binary_operator("/", "x", "y"))
                                               ]))
            ])),
            ("""
            {
              x := 1;
              y := x + 1;
              @? y = x {
                y := y * x;
              }{
                x := x / y;
              }
            }
            """, self._create_statement_block([
                self._create_assignment_statement("x", "1"),
                self._create_assignment_statement(
                    "y", self._create_arethmatic_binary_operator("+", "x", "1")),
                self._create_conditional_repeat_block(self._create_relational_binary_operator("=", "y", "x"),
                                                      self._create_statement_block([
                                                          self._create_assignment_statement(
                                                              "y", self._create_arethmatic_binary_operator("*", "y", "x"))
                                                      ]),
                                                      self._create_statement_block([
                                                          self._create_assignment_statement(
                                                              "x", self._create_arethmatic_binary_operator("/", "x", "y"))
                                                      ]))
            ])),
            ("""
            {
              x := 1;
              y := x + 1;

              @ # the repeater and conditional are two operators that work together
              ? y = x {
                y := y * x;
              }{
                x := x / y;
              }

              ? y = x {
                y := y * x;
              }{
                x := x / y;
              }
            }
            """, self._create_statement_block([
                self._create_assignment_statement("x", "1"),
                self._create_assignment_statement(
                    "y", self._create_arethmatic_binary_operator("+", "x", "1")),
                self._create_conditional_repeat_block(self._create_relational_binary_operator("=", "y", "x"),
                                                      self._create_statement_block([
                                                          self._create_assignment_statement(
                                                              "y", self._create_arethmatic_binary_operator("*", "y", "x"))
                                                      ]),
                                                      self._create_statement_block([
                                                          self._create_assignment_statement(
                                                              "x", self._create_arethmatic_binary_operator("/", "x", "y"))
                                                      ])),
                self._create_conditional_block(self._create_relational_binary_operator("=", "y", "x"),
                                               self._create_statement_block([
                                                   self._create_assignment_statement(
                                                       "y", self._create_arethmatic_binary_operator("*", "y", "x"))
                                               ]),
                                               self._create_statement_block([
                                                   self._create_assignment_statement(
                                                       "x", self._create_arethmatic_binary_operator("/", "x", "y"))
                                               ]))
            ])),
            ("""
            {
              x := 1;
              y := x + 1;

              ? y = x {
                y := y * x;
              }{
                x := x / y;
              }

              @? y = x {
                y := y * x;
              }{
                x := x / y;
              }
            }
            """, self._create_statement_block([
                self._create_assignment_statement("x", "1"),
                self._create_assignment_statement(
                    "y", self._create_arethmatic_binary_operator("+", "x", "1")),
                self._create_conditional_block(self._create_relational_binary_operator("=", "y", "x"),
                                               self._create_statement_block([
                                                   self._create_assignment_statement(
                                                       "y", self._create_arethmatic_binary_operator("*", "y", "x"))
                                               ]),
                                               self._create_statement_block([
                                                   self._create_assignment_statement(
                                                       "x", self._create_arethmatic_binary_operator("/", "x", "y"))
                                               ])),
                self._create_conditional_repeat_block(self._create_relational_binary_operator("=", "y", "x"),
                                                      self._create_statement_block([
                                                          self._create_assignment_statement(
                                                              "y", self._create_arethmatic_binary_operator("*", "y", "x"))
                                                      ]),
                                                      self._create_statement_block([
                                                          self._create_assignment_statement(
                                                              "x", self._create_arethmatic_binary_operator("/", "x", "y"))
                                                      ]))
            ])),

            ("""
                Athlete Trevor
            """, self._create_tag_statement("Athlete", ["Trevor"])),

            ("""
            {
                Athlete Trevor;
            }
            """, self._create_statement_block([
                self._create_tag_statement("Athlete", ["Trevor"]),
            ])),

            ("""
            {
                x := 5;
                y := 10;
                Athlete Trevor;
                Excercise Log Trevor x pushups;
                ? y > 5 {
                  Excercise
                  Log Trevor
                  y
                  situps;
                }
            }
            """, self._create_statement_block([
                self._create_assignment_statement("x", "5"),
                self._create_assignment_statement("y", "10"),
                self._create_tag_statement("Athlete", ["Trevor"]),
                self._create_tag_statement("Excercise", ["Log",  "Trevor", "x", "pushups"]),
                self._create_conditional_block(self._create_relational_binary_operator(
                    ">", "y", "5"), self._create_statement_block([self._create_tag_statement("Excercise", ["Log",  "Trevor", "y", "situps"])]))
            ]))
        ]
        self._evaluate(self._helper.lexicomb_parser, cases)

    def test_interpreter_returning_result_object(self):
        cases = [
            ("""
            {
            a:=42;
            ?a=42{
              return a;
            };

            a:=5/0;
            return a;
            }""", self._create_result(42)),
            ("""
            {
              x := 1;
              step := 2;
              y := 10;

              @? x < y {
                x := x + step;
                ?x=(y-step+1){
                    return x;
                };
              }
              return y;
            }
            """, self._create_result(9)),

            ("""
            {
              return ReturnArgument foo;
            }

            """, self._create_result("foo")),

            ("""{
              Register Nichola Wilson;
              Excercise Nichola situps 10 07:15 07:45;
              Excercise Nichola situps 10 07:05 07:35;
              Excercise Nichola situps 10 07:00 07:15;
              Excercise Nichola pushups 20 07:00 07:15;
            }
            """, self._create_result({'Register': {'Nichola': {}}, 'Excercise': {'Nichola': {'situps': {'0': 3, '1': 30, '2': 1.25, '3': 0.4166666666666667}, 'pushups': {'0': 1, '1': 20, '2': 0.25, '3': 0.25}}}})),

        ]

        self._interpret(self._helper.lexicomb_parser, cases, Interpret.RETURN_RESULT)

    def test_interpreter_returning_frame(self):
        cases = [
            ("""
            {
              a := 42;
              b := (42);
              c := a;
              d := (c);
              f := 4.004200346534600034;
            }
            """, {"$is_unwinding": False, "a": 42, "b": 42, "c": 42, "d": 42, "f": 4.004200346534600034}),
            ("""
            {
              a := 1 < 2;
              b := 1 <= 2;
              c := 1 = 2;
              d := 1 >= 2;
              e := 1 > 2;
              f := 1 != 2;
              g := !1 != 2;
            }
            """, {"$is_unwinding": False, "a": True, "b": True, "c": False, "d": False, "e": False, "f": True, "g": False}),
            ("""
            {
              x := 42;
              y := 2;
              a := x / y;
              b := x * y;
              c := x + y;
              d := x - y;
              e := y - x;
              f := x / y + 3 * 2 - 3;
              g := x / (y + 3);
            }
            """, {"$is_unwinding": False, "x": 42, "y": 2, "a": 21, "b": 84, "c": 44, "d": 40, "e": -40, "f": 24, "g": 8.4}),
            ("""
            {
              x := 1;
              step := 2;
              y := 10;

              @? x < y {
                x := x + step;
              }
            }
            """, {"$is_unwinding": False, "x": 11, "step": 2, "y": 10}),
            ("""
            {
              x:=1;
              return;
            }
            """, {"$is_unwinding": True, "x": 1}),
            ("""
            {
              has_arg0 := [arg0];
              has_arg1 := [arg1];
              is_arg1_undefined := ![arg1];
              does_arg0_have_deep_property := [arg0[property][deep_property][2]];
            }
            """, {"$is_unwinding": False, "arg0": 0, "has_arg0": True, "has_arg1": False, "is_arg1_undefined": True, "does_arg0_have_deep_property": False}, {"arg0": 0}),
            ("""
            {
              ? [arg0] {
                x := arg0;
              }{
                x:=10;
              }
            }
            """, {"$is_unwinding": False, "arg0": 5, "x": 5}, {"arg0": 5}),

            ("""
            {
              ? [arg1]{
                x := arg1;
              }
              {
                x := 10;
              }
            }
            """, {"$is_unwinding": False, "arg0": 5, "x": 10}, {"arg0": 5}),
            ("""
            {
              x := 10;
              ? ![arg0]{
                x := 11;
              };
            }
            """, {"$is_unwinding": False, "arg0": 5, "x": 10}, {"arg0": 5}),
            ("""
            {
              return;
            }
            """, {"$is_unwinding": True}),
        ]

        self._interpret(self._helper.lexicomb_parser, cases, Interpret.RETURN_FRAME)

    def test_interpreter_returning_eval(self):
        cases = [
            ("""
            {
              ReturnNothing foo;
            }

             """, None),

            ("""
            {
              return ReturnNothing foo;
            }

             """, None),

            ("""
            {
              x := ReturnNothing foo;
              return x;
            }

             """, None),

            ("""
            {
              ReturnArgument foo;
            }

            """, None),

            ("""
            {
              return ReturnArgument foo;
            }

            """, "foo"),

            ("""
            {
              x := ReturnArgument foo;
              return x;
            }

            """, "foo"),

            ("""
            {
              ReturnArgument foo;
              x := ReturnArgument bar;
              ReturnArgument baz;
              return x;
            }

            """, "bar"),

            ("""{
              return Concat Trevor Wilson;
            }
            """, "TrevorWilson"),

            ("""{
              x:= Concat Trevor Wilson;
              return x;
            }
            """, "TrevorWilson"),

            ("""{
              return Concat Trevor Wilson 1 2 3;
            }
            """, "TrevorWilson123"),

            ("""{
              return Concat 1 2 3 Trevor Wilson;
            }
            """, "6TrevorWilson"),

            ("""{
              x:= 1 + 2 + 3;
              return Concat Trevor Wilson x;
            }
            """, "TrevorWilson6"),

            ("""{
              x:= 1+2+3;
              name:= Concat Trevor Wilson;
              return name + x;
            }
            """, "TrevorWilson6"),

            ("""{
              return Concat 1 2 3;
            }
            """, 6),

            ("""{
              CreateString 1 2 3 4 5 6 Trevor Wilson;
              return CreateString 1 2 3 Trevor Wilson;
            }
            """, "6Trevor Wilson"),

            ("""{
              return CreateString Trevor Wilson 1 2 3;
            }
            """, "Trevor Wilson 1 2 3"),

            ("""{
              Register Nichola Wilson;
              Excercise Nichola situps 10 07:15 07:45;
              Excercise Nichola situps 10 07:05 07:35;
              Excercise Nichola situps 10 07:00 07:15;
              Excercise Nichola pushups 20 07:00 07:15;
            }
            """, None),

            ##############################################
            # Testing the behavior of conditional blocks #
            ##############################################

            ("""
            {
              truthy := 1=1;
              falsey := !truthy;
              result := CreateString Initial Value;
              ? falsey {
                result := CreateString Set in truthy conditional block;
              }
              
              return result;
            } """, "Initial Value"),

            ("""
            { 
              truthy := 1=1;
              falsey := !truthy;
              result := CreateString Initial Value;
              ? truthy {
                result := CreateString Set in truthy conditional block;
              }
              
              return result;
            }

            """, "Set in True conditional block"),

            ("""
            { 
              truthy := 1=1;
              falsey := !truthy;
              result := CreateString Initial Value;
              ? truthy {
                result := CreateString Set in truthy conditional block;
              }
              
              result := CreateString Set after conditional block;
              
              return result;
            }

            """, "Set after conditional block"),

            ("""
            { 
              truthy := 1=1;
              falsey := !truthy;
              result := CreateString Initial Value;
              ? truthy {
                result := CreateString Set in truthy conditional block;
              } {
                result := CreateString Set in falsey conditional block;
              }
                            
              return result;
            } """, "Set in True conditional block"),

            ("""
            { 
              truthy := 1=1;
              falsey := !truthy;
              result := CreateString Initial Value;
              ? falsey {
                result := CreateString Set in truthy conditional block;
              } {
                result := CreateString Set in falsey conditional block;
              }
                            
              return result;
            } """, "Set in False conditional block"),

            ("""
            { 
              truthy := 1=1;
              falsey := !truthy;
              result := CreateString Initial Value;
              ? truthy {
                result := CreateString Set in first truthy conditional block;
              } ? truthy {
                result := CreateString Set in second truthy conditional block;
              }
                            
              return result;
            } """, "Set in first True conditional block"),

            ("""
            { 
              truthy := 1=1;
              falsey := !truthy;
              result := CreateString Initial Value;
              ? truthy {
                result := CreateString Set in first truthy conditional block;
              }; # statement separator allows subsequent short conditionals

              ? truthy {
                result := CreateString Set in second truthy conditional block;
              }
                            
              return result;
            } """, "Set in second True conditional block"),

            ("""
            { 
              truthy := 1=1;
              falsey := !truthy;
              result := CreateString Initial Value;
              ? truthy {
                result := CreateString Set in first True conditional block;
              }{
              }

              # empty statement block allows subsequent conditionals,
              # but statement terminator is preferred

              ? truthy {
                result := CreateString Set in second truthy conditional block;
              }
                            
              return result;
            } """, "Set in second True conditional block"),

            ("""
            { 
              truthy := 1=1;
              falsey := !truthy;
              result := CreateString Initial Value;
              ? falsey {
                result := CreateString Set in truthy conditional block;
              } ? falsey {
                result := CreateString Set in falsey conditional block;
              }
                            
              return result;
            } """, "Initial Value"),

            ("""
            { 
              truthy := 1=1;
              falsey := !truthy;
              result := CreateString Initial Value;
              ? falsey {
                result := CreateString Set in if conditional block;
              } ? falsey {
                result := CreateString Set in else if conditional block;
              } {
                result := CreateString Set in else conditional block;
              }
                            
              return result;
            } """, "Set in else conditional block"),

            ("""
            {
              x := 1;
              step := 2;
              y := 10;

              @? x < y {
                x := x + step;
              }
              return x;
            } """, 11),

            ("""
            {
              x := 1;
              step := 2;
              y := 10;

              @? x < y {
                x := x + step;
              }
              {
                x := x + step + 1;
              }
              return x;
            } """, 14),

            ("""
            {
              x := 1;
              step := 2;
              y := 10;
              
              @? x > y {
                x := x + step;
              }
              {
                x := x + step + 1;
              }
              return x;
            } """, 4),

            ("""
            {
              x := 1;
              step := 2;
              y := 10;
              
              @? x < 2 {
                x := x + step;
              }
              ? x < y {
                x := x + step + 1;
              }
              {
                x:= x - 2 * step;
              }
              return x;
            } """, 8),

            ("""
            {
              x := 1;
              step := 2;
              y := 10;
              
              ? x > 5 {
                x := x + step;
              }
              @? x < y {
                x := x + step + 1;
              }
              {               
                x:= x - 2 * step - 1;
              }
              return x;
            } """, 5),

            ("""
            {
              x := 1;
              step := 2;
              y := 10;
              
              ? x > 0 {
                x := 2;
              }
              # conditional repeat always begins a new conditional
              # statement.
              @? x < y {
                x := x + step + 1;
              }
              {               
                x:= x - 2 * step - 1;
              }
              return x;
            } """, 6),

            ("""{
              # F0 = 0, F1 = 1, Fn = Fn-1 + Fn-2
              return Fibernaci 10;
            }
            """, {'0': 0, '1': 1, '2': 1, '3': 2, '4': 3, '5': 5, '6': 8, '7': 13, '8': 21, '9': 34, '10': 55})
        ]

        self._interpret(self._helper.lexicomb_parser, cases, Interpret.RETURN_EVAL)

    def test_interpreter_error_handling(self):
        from bbpyp.abstract_parser.exception.parse_error import ParseError
        cases = [
            ("""
            {
              x := 10;
              ? ![arg0]
                x := 11;
              ;
            }
            """, ParseError)
        ]

        for case in cases:
            input_lines, expected_error = case
            tokens = self._helper.tokenize(input_lines)
            with self.assertRaises(expected_error):
                parser_result = self._helper.lexicomb_parser(tokens, 0)

    def _assert_parser(self, parser, input_line, expected_result, message=None, interpret_enum=Interpret.DO_NOT_INTERPRET, **kwargs):
        tokens = self._helper.tokenize(input_line)
        parser_result = parser(tokens, 0)

        self.assertIsNotNone(parser_result.value, message)
        interpreter = parser_result.value
        actual_result = parser_result.value

        def print_interpreter():
            print(f"parser = {interpreter}")

        def print_expected_and_actual():
            print(f"expected = {expected_result}")
            print(f"actual = {actual_result}")

        if interpret_enum != Interpret.DO_NOT_INTERPRET:
            frame = {name: value for name, value in kwargs.items()}
            try:
                if interpret_enum == Interpret.RETURN_EVAL:
                    actual_result = interpreter.eval(frame)
                elif interpret_enum == Interpret.RETURN_RESULT:
                    actual_result = interpreter.eval_and_return_result(frame)
                else:
                    interpreter.eval(frame)
                    actual_result = frame
            except Exception as e:
                print(f"An exception occurred during evaluation: {message}")
                raise e

        ################################################################################################
        # un-comment the call to print_interpreter to see the string representation of the interpreter #
        ################################################################################################
        # print_interpreter()

        try:
            self.assertEqual(actual_result, expected_result, message)
            if hasattr(actual_result, '__dict__'):
                self.assertEqual(actual_result.__dict__, expected_result.__dict__, message)
        except:
            print_expected_and_actual()

            ################################################################################################
            # un-comment the call to print_interpreter to see the string representation of the interpreter #
            ################################################################################################
            # print_interpreter()
            raise

    def _process_cases(self, parser, cases, interpret_enum=Interpret.DO_NOT_INTERPRET):
        case_number = 0
        for case in cases:
            kwargs = {}
            if len(case) == 2:
                provided, expected = case
            else:
                provided, expected, kwargs = case

            self._assert_parser(parser, provided, expected,
                                f"for case #{case_number}", interpret_enum, **kwargs)
            case_number += 1

    def _evaluate(self, parser, cases):
        self._process_cases(parser, cases)

    def _interpret(self, parser, cases, interpret_enum=Interpret.RETURN_EVAL):
        self._process_cases(parser, cases, interpret_enum)

    def _create_result(self, val):
        if type(val) is dict:
            return self._helper._result_factory(**val)
        return self._helper._result_factory(val)

    def _create_access(self, val, keys=None):
        if keys is None:
            keys = []
        variable = self._helper.lexicomb_ioc.variable_provider(val)
        return self._helper.lexicomb_ioc.access_provider(variable, keys)

    def _create_variable(self, val):
        return self._helper.lexicomb_ioc.variable_provider(val)

    def _create_real_number(self, val):
        return self._helper.lexicomb_ioc.real_number_factory_provider(val) if isinstance(val, str) else val

    def _create_hash(self):
        return self._helper.lexicomb_ioc.hash_provider()

    def _create_term(self, val):
        term = val
        if isinstance(val, str):
            term = self._create_real_number(val) if val.replace(
                ".", "").isdigit() else self._create_access(val)
        elif isinstance(val, dict):
            term = self._create_hash()

        return term

    def _create_arethmatic_binary_operator(self, operator, lhs, rhs):
        lhs = self._create_term(lhs)
        rhs = self._create_term(rhs)

        operator = self._helper.create_operator_enum(operator)

        return self._helper.lexicomb_ioc.arethmatic_binary_operator_provider(operator)(lhs, rhs)

    def _create_relational_binary_operator(self, operator, lhs, rhs):
        lhs = self._create_term(lhs)
        rhs = self._create_term(rhs)

        operator = self._helper.create_operator_enum(operator)

        return self._helper.lexicomb_ioc.relational_binary_operator_provider(operator)(lhs, rhs)

    def _create_logical_binary_operator(self, operator, lhs, rhs):
        lhs = self._create_term(lhs)
        rhs = self._create_term(rhs)

        operator = self._helper.create_operator_enum(operator)

        return self._helper.lexicomb_ioc.logical_binary_operator_provider(operator)(lhs, rhs)

    def _create_unary_operator(self, operator, operand):

        operator = self._helper.create_operator_enum(operator)
        return self._helper.lexicomb_ioc.logical_unary_operator_provider(operator)(self._create_term(operand))

    def _create_assignment_statement(self, lhs, rhs):
        lhs_variable = self._create_term(lhs)
        rhs_expression = self._create_term(rhs)
        return self._helper.lexicomb_ioc.assignment_provider(lhs_variable, rhs_expression)

    def _create_statement_block(self, statements):
        return self._helper.lexicomb_parser._block_factory(statements, self._helper.lexicomb_parser._statement_seperator.value)

    def _create_conditional_block(self, logical_expression_ast, if_block_ast, else_block_ast=None):

        return self._helper.lexicomb_parser._conditional_factory(logical_expression_ast, if_block_ast, else_block_ast)

    def _create_conditional_repeat_block(self, logical_expression_ast, if_block_ast, else_block_ast=None):
        conditional_block = self._create_conditional_block(
            logical_expression_ast, if_block_ast, else_block_ast)
        return self._helper.lexicomb_parser._conditional_repeat_factory(conditional_block)

    def _create_tag_statement(self, first, rest):
        tag = self._create_variable(first)
        tags = []
        for token in rest:
            term = self._create_term(token)
            tags.append(term)

        return self._helper.lexicomb_parser._tag_statement_factory(tag, tags) if len(tags) else None
