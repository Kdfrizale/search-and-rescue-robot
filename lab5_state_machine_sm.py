#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from cpsc495_flexbe_flexbe_states.kyle_pub_state import KylePubState
from flexbe_states.wait_state import WaitState
from flexbe_states.operator_decision_state import OperatorDecisionState
from cpsc495_flexbe_flexbe_states.kyle_twist_state import KyleTwistState
from flexbe_states.subscriber_state import SubscriberState
from cpsc495_flexbe_flexbe_states.timed_twist_state import TimedTwistState
from cpsc495_flexbe_flexbe_states.kyle_count_state import KyleCountState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jan 11 2017
@author: David Conner
'''
class Lab5_State_MachineSM(Behavior):
	'''
	This is a simple example for a behavior.
	'''


	def __init__(self):
		super(Lab5_State_MachineSM, self).__init__()
		self.name = 'Lab5_State_Machine'

		# parameters of this behavior
		self.add_parameter('waiting_time', 3)

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1162 y:100, x:318 y:599
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:84 y:36
			OperatableStateMachine.add('initialPub0',
										KylePubState(cmd_topic='/makethisupcount'),
										transitions={'done': 'GetTwistCommand'},
										autonomy={'done': Autonomy.Off})

			# x:471 y:488
			OperatableStateMachine.add('simpleWait',
										WaitState(wait_time=.01),
										transitions={'done': 'GetTwistCommand'},
										autonomy={'done': Autonomy.Off})

			# x:864 y:316
			OperatableStateMachine.add('Should_Robot_Finish',
										OperatorDecisionState(outcomes=["yes", "no"], hint="Should the Robot Stop?", suggestion=None),
										transitions={'yes': 'finished', 'no': 'simpleWait'},
										autonomy={'yes': Autonomy.Off, 'no': Autonomy.Off})

			# x:441 y:214
			OperatableStateMachine.add('move',
										KyleTwistState(cmd_topic='/turtlebot/stamped_cmd_vel_mux/input/navi'),
										transitions={'done': 'Should_Robot_Finish', 'getNewMove': 'GetTwistCommand'},
										autonomy={'done': Autonomy.Off, 'getNewMove': Autonomy.Off},
										remapping={'input_velocity': 'velocitymy', 'input_rotation_rate': 'angularmy'})

			# x:249 y:85
			OperatableStateMachine.add('getang',
										SubscriberState(topic="/makethisupang", blocking=True, clear=False),
										transitions={'received': 'move', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'angularmy'})

			# x:17 y:300
			OperatableStateMachine.add('Rotate',
										TimedTwistState(target_time=.1, velocity=0, rotation_rate=.1, cmd_topic='/turtlebot/stamped_cmd_vel_mux/input/navi'),
										transitions={'done': 'GetTwistCommand'},
										autonomy={'done': Autonomy.Off})

			# x:234 y:224
			OperatableStateMachine.add('getCount',
										SubscriberState(topic='/makethisupcount', blocking=True, clear=False),
										transitions={'received': 'checkCount', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'count'})

			# x:181 y:330
			OperatableStateMachine.add('checkCount',
										KyleCountState(cmd_topic='/makethisupcount'),
										transitions={'done': 'failed', 'notDone': 'Rotate'},
										autonomy={'done': Autonomy.Off, 'notDone': Autonomy.Off},
										remapping={'inputCount': 'count'})

			# x:102 y:130
			OperatableStateMachine.add('GetTwistCommand',
										SubscriberState(topic="/makethisupvel", blocking=False, clear=False),
										transitions={'received': 'getang', 'unavailable': 'getCount'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'velocitymy'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
