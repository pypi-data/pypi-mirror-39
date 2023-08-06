'''Contains unit tests for basis.setup.step.scoped_step.
'''
import unittest
from ..... import Basis, ScopedStep

class ScopedStepTest(unittest.TestCase):
	def __init__(self):
		unittest.TestCase.__init__(self)
		self.basis = Basis()

	def testSuccessfulStep(self):
		'''Test that a step that runs without any exceptions
		is considered successful in the Basis instance.
		'''
		numFailedStepsBefore = len(self.basis.failedSteps())

		with ScopedStep("Test step", self.basis) as _step:
			pass

		numFailedStepsAfter = len(self.basis.failedSteps())
		self.assertEquals(numFailedStepsBefore, numFailedStepsAfter)

	def testFailedStep(self):
		'''Test that a step that has an unhandled exception
		is considered failed in the Basis instance.
		'''
		numFailedStepsBefore = len(self.basis.failedSteps())

		try:
			with ScopedStep("Test step", self.basis) as _step:
				raise Exception("Test exception")
		except:
			pass

		numFailedStepsAfter = len(self.basis.failedSteps())
		self.assertGreater(numFailedStepsAfter, numFailedStepsBefore)


def suite():
	'''Returns all cases that should be run
	to test this part of the application.
	'''

	all_cases = (ScopedStepTest,)
	all_suites = []

	for case in all_cases:
		all_suites.append(unittest.TestLoader().loadTestsFromTestCase(case))

	return unittest.TestSuite(all_suites)

if __name__ == "__main__":
	unittest.TextTestRunner(verbosity=2).run(suite())
