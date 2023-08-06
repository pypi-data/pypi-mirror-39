import time

from playground.suiteB import TestSuiteB
from test_junkie.decorators import Suite, test, beforeClass, beforeTest, afterTest, afterClass
from test_junkie.meta import meta, Meta
from tests.junkie_suites.TestListener import TestListener
from playground.SpecialDecorators import TestRules


@Suite(retry=2,
       listener=TestListener,
       meta=meta(name="Suite D",
                 known_bugs=[]),
       parameters=[1, 2, 3],
       priority=2, pr=[TestSuiteB], feature="Login", owner="Mike")
class TestSuiteD(TestRules):

    # @beforeClass()
    # def before_class1(self):
    #     pass
    #
    # @beforeTest()
    # def before_test2(self):
    #     # write your code here
    #     pass
    #
    # @afterTest()
    # def after_test3(self):
    #     # write your code here
    #     pass
    #
    # @afterClass()
    # def after_class4(self):
    #     # write your code here
    #     pass

    @test(tags=["tag a", "tag d"], owner="Artur")
    def a(self, suite_parameter):
        pass

    @test(component="OAuth", tags=["tag a", "tag d"])
    def b(self):
        pass
