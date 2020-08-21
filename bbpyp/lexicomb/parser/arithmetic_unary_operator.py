from bbpyp.lexicomb.parser.unary_operator import UnaryOperator
from bbpyp.lexicomb.parser.model.operator_enum import OperatorEnum


class ArithmeticUnaryOperator(UnaryOperator):

    def __repr__(self):
        return f"({self.operator} {self.operand})"

    def _eval(self, frame):
        operand_value = self.operand.eval(frame)

        value = None
        if self.operator is OperatorEnum.ARITHMETIC_NEGATIVE:
            value = -operand_value

        return value
