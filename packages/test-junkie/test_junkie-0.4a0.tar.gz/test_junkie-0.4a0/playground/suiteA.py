import time

from playground.SpecialDecorators import TestRules
from playground.suiteB import TestSuiteB
from test_junkie.decorators import Suite, test, beforeClass, beforeTest, afterTest, afterClass
from test_junkie.meta import meta, Meta
from tests.junkie_suites.TestListener import TestListener


def test_func():
    print("evaluating...")
    time.sleep(2)
    return [{"key": "value"}, {"key2": "value2"}]


@Suite(retry=2,
       listener=TestListener,
       meta=meta(name="Suite A",
                 known_bugs=[]),
       owner="Mike")
class TestSuiteA(TestRules):

    @test(dependencies=[])
    def a(self):

        print("Finished SUITE A / TEST A")

    # @test(priority=1, pr=[TestSuiteB.a])
    # def b(self):
    #     # time.sleep(15)
    #     print("Finished SUITE A / TEST B")
    #
    # @test(skip=True)
    # def c(self):
    #     # time.sleep(15)
    #     print("Finished SUITE A / TEST C")
