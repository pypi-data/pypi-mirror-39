'''Defines the ScopedStep class.
'''
from .. import StepResult

kDefaultStepName = "Unnamed step"

class ScopedStep(object):
	'''Similar to Step, but is used as a context.
	Upon entering the ScopedStep's context, the step is marked as running,
	and upon exiting it is marked as finished.

	If an unhandled exception occurs,
	the step fails with its reason specified as the unhandled exception.
	'''
	def __init__(self, stepName, basis):
		'''Instance initializer.

		:param str stepName: The name of the step. If not provided, defaults to 'Unnamed step'.
		:param basis.Basis basis: The Basis instance to use this step on. 
		
		:raises RuntimeError: If basis is None.
		'''
		self.stepName = kDefaultStepName
		if stepName:
			self.stepName = stepName
		else:
			basis.logger.warning("Step has Name field but it was empty; was this intended?")

		if not basis:
			raise RuntimeError("ScopedStep needs context object to operate!")
		self.basis = basis
		self.step_status = StepResult.NotDone

	def __enter__(self):
		'''Context entry method.
		'''
		self.basis.logger.info("Performing step: " + self.stepName + "...")
		self.basis.step_status = StepResult.InProgress

	def __exit__(self, exc_type, exc_value, traceback):
		'''Context exit method.

		:param exc_type:	The exception type if an exception occured
							within the yield section, None otherwise.
		:param exc_value:	The exception object itself if an exception occured
							within the yield section, None otherwise.
		:param traceback:	The traceback to the function generating
							the unhandeled exception if an exception occured
							within the yield section, None otherwise.
		'''
		#Check: did this step have any exception?
		if not exc_value:
			#If not, mark this step as successful.
			self.step_status = StepResult.Success
			self.basis.logger.success("Step succeeded: " + self.stepName)
		else:
			#If an unhandled exception occurs,
			#mark this step as failed with
			#the unhandled exception specified as the reason.
			self.step_status = StepResult.Fail
			self.basis.logger.error("Step {0} failed install with an error: {1}".format(self.stepName, exc_value))
			self.basis.addFailedStep(self.stepName)