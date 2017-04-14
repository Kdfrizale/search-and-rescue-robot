#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.subscriber_state import SubscriberState
from cpsc495_flexbe_flexbe_states.kyle_twist_state import KyleTwistState
from cpsc495_flexbe_flexbe_states.timed_twist_state import TimedTwistState
from cpsc495_flexbe_flexbe_states.kyle_count_state import KyleCountState
from cpsc495_flexbe_flexbe_states.kyle_verify_state import KyleVerifyState
from flexbe_states.wait_state import WaitState
from flexbe_states.operator_decision_state import OperatorDecisionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Mar 29 2017
@author: Kyle Frizzell
'''
class Lab5_State_MachineSM(Behavior):
	'''
	Main State Machine for Lab 5
	'''


	def __init__(self):
		super(Lab5_State_MachineSM, self).__init__()
		self.name = 'Lab5_State_Machine'

		# parameters of this behavior

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
			# x:92 y:82
			OperatableStateMachine.add('GetVelocity',
										SubscriberState(topic="/makethisupvel", blocking=True, clear=False),
										transitions={'received': 'getang', 'unavailable': 'checkCount'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'velocitymy'})

			# x:721 y:137
			OperatableStateMachine.add('move',
										KyleTwistState(cmd_topic='/turtlebot/stamped_cmd_vel_mux/input/navi'),
										transitions={'done': 'Should_Robot_Finish', 'getNewMove': 'GetVelocity'},
										autonomy={'done': Autonomy.Off, 'getNewMove': Autonomy.Off},
										remapping={'input_velocity': 'velocitymy', 'input_rotation_rate': 'angularmy'})

			# x:277 y:51
			OperatableStateMachine.add('getang',
										SubscriberState(topic="/makethisupang", blocking=True, clear=False),
										transitions={'received': 'Ball_NOT_in_image', 'unavailable': 'checkCount'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'angularmy'})

			# x:97 y:394
			OperatableStateMachine.add('Rotate',
										TimedTwistState(target_time=.1, velocity=0, rotation_rate=.5, cmd_topic='/turtlebot/stamped_cmd_vel_mux/input/navi'),
										transitions={'done': 'GetVelocity'},
										autonomy={'done': Autonomy.Off})

			# x:286 y:434
			OperatableStateMachine.add('checkCount',
										KyleCountState(MaxCount=45),
										transitions={'done': 'failed', 'notDone': 'Rotate'},
										autonomy={'done': Autonomy.Off, 'notDone': Autonomy.Off})

			# x:496 y:22
			OperatableStateMachine.add('Ball_NOT_in_image',
										KyleVerifyState(ValueToMeasureAgainst=7777.0),
										transitions={'verified': 'checkCount', 'notVerified': 'move'},
										autonomy={'verified': Autonomy.Off, 'notVerified': Autonomy.Off},
										remapping={'inputValueVel': 'velocitymy', 'inputValueAng': 'angularmy'})

			# x:991 y:264
			OperatableStateMachine.add('simpleWait',
										WaitState(wait_time=.01),
										transitions={'done': 'GetVelocity'},
										autonomy={'done': Autonomy.Off})

			# x:983 y:151
			OperatableStateMachine.add('Should_Robot_Finish',
										OperatorDecisionState(outcomes=["yes", "no"], hint="Should the Robot Stop?", suggestion=None),
										transitions={'yes': 'finished', 'no': 'simpleWait'},
										autonomy={'yes': Autonomy.Off, 'no': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
