import pytest

from app.calc import Calculator


class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_adding(self):
        assert self.calc.adding(self, 30, 10) == 40

    def test_subtraction(self):
        assert self.calc.subtraction(self, 30, 10) == 20

    def test_multiply(self):
        assert self.calc.multiply(self, 30, 10) == 300

    def test_division(self):
        assert self.calc.division(self, 30, 10) == 3

    def teardown(self):
        print('Выполнение метода Teardown')
