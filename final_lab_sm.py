#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flex_nav_flexbe_states.clear_costmaps_state import ClearCostmapsState
from flex_nav_flexbe_states.get_path_state import GetPathState
from flexbe_states.operator_decision_state import OperatorDecisionState
from flex_nav_flexbe_states.follow_path_state import FollowPathState
from cpsc495_flexbe_flexbe_states.turtlebot_status_state import TurtlebotStatusState
from flex_nav_turtlebot_flexbe_behaviors.turtlebot_simple_recovery_sm import TurtlebotSimpleRecoverySM
from flexbe_states.log_state import LogState
from flex_nav_flexbe_states.get_pose_state import GetPoseState
from cpsc495_flexbe_flexbe_states.timed_stop_state import TimedStopState
from cpsc495_flexbe_flexbe_states.kyle_pub_state import KylePubState
from flexbe_states.subscriber_state import SubscriberState
from cpsc495_flexbe_flexbe_states.kyle_verify_state import KyleVerifyState
from cpsc495_flexbe_flexbe_states.kyle_twist_state import KyleTwistState
from cpsc495_flexbe_flexbe_states.kyle_pubInput_state import KylePubInputState
from cpsc495_flexbe_flexbe_states.timed_twist_state import TimedTwistState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Apr 13 2017
@author: team3
'''
class final_labSM(Behavior):
	'''
	final
	'''


	def __init__(self):
		super(final_labSM, self).__init__()
		self.name = 'final_lab'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(TurtlebotSimpleRecoverySM, 'Turtlebot Simple Recovery')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:807 y:293, x:1163 y:18
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

		# [/MANUAL_CREATE]

		# x:35 y:227, x:161 y:228, x:363 y:243, x:536 y:22, x:472 y:241, x:547 y:181, x:544 y:99, x:674 y:184, x:263 y:228
		_sm_container_0 = ConcurrencyContainer(outcomes=['finished', 'failed', 'danger', 'preempted'], input_keys=['plan'], conditions=[
										('failed', [('DWA', 'failed')]),
										('finished', [('DWA', 'done')]),
										('preempted', [('DWA', 'preempted')]),
										('danger', [('Safety', 'cliff')]),
										('danger', [('Safety', 'bumper')])
										])

		with _sm_container_0:
			# x:101 y:78
			OperatableStateMachine.add('DWA',
										FollowPathState(topic="low_level_planner"),
										transitions={'done': 'finished', 'failed': 'failed', 'preempted': 'preempted'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'preempted': Autonomy.Off},
										remapping={'plan': 'plan'})

			# x:343 y:91
			OperatableStateMachine.add('Safety',
										TurtlebotStatusState(bumper_topic='mobile_base/events/bumper', cliff_topic='mobile_base/events/cliff'),
										transitions={'bumper': 'danger', 'cliff': 'danger'},
										autonomy={'bumper': Autonomy.Off, 'cliff': Autonomy.Off})



		with _state_machine:
			# x:193 y:26
			OperatableStateMachine.add('ClearCostmap',
										ClearCostmapsState(costmap_topics=['high_level_planner/clear_costmap','low_level_planner/clear_costmap'], timeout=5.0),
										transitions={'done': 'Receive Goal', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:205 y:207
			OperatableStateMachine.add('Receive Path',
										GetPathState(planner_topic="high_level_planner"),
										transitions={'planned': 'ExecutePlan', 'empty': 'Continue', 'failed': 'Continue'},
										autonomy={'planned': Autonomy.Off, 'empty': Autonomy.Low, 'failed': Autonomy.Low},
										remapping={'goal': 'goal', 'plan': 'plan'})

			# x:194 y:301
			OperatableStateMachine.add('ExecutePlan',
										OperatorDecisionState(outcomes=["yes","no"], hint="Execute the current plan?", suggestion="yes"),
										transitions={'yes': 'Container', 'no': 'Continue'},
										autonomy={'yes': Autonomy.High, 'no': Autonomy.Full})

			# x:446 y:275
			OperatableStateMachine.add('Container',
										_sm_container_0,
										transitions={'finished': 'Log Success', 'failed': 'AutoReplan', 'danger': 'EStop', 'preempted': 'Continue'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'danger': Autonomy.Inherit, 'preempted': Autonomy.Inherit},
										remapping={'plan': 'plan'})

			# x:435 y:146
			OperatableStateMachine.add('Continue',
										OperatorDecisionState(outcomes=["yes","no","recover","clearcostmap"], hint="Continue planning to new goal?", suggestion="yes"),
										transitions={'yes': 'Receive Goal', 'no': 'finished', 'recover': 'LogRecovery', 'clearcostmap': 'ClearCostmap'},
										autonomy={'yes': Autonomy.High, 'no': Autonomy.Full, 'recover': Autonomy.Full, 'clearcostmap': Autonomy.Full})

			# x:1052 y:227
			OperatableStateMachine.add('Turtlebot Simple Recovery',
										self.use_behavior(TurtlebotSimpleRecoverySM, 'Turtlebot Simple Recovery'),
										transitions={'finished': 'AutoReplan', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:664 y:307
			OperatableStateMachine.add('Log Success',
										LogState(text="Success!", severity=Logger.REPORT_HINT),
										transitions={'done': 'initialPub'},
										autonomy={'done': Autonomy.Off})

			# x:664 y:374
			OperatableStateMachine.add('Log Fail',
										LogState(text="Path execution failure", severity=Logger.REPORT_HINT),
										transitions={'done': 'Recover'},
										autonomy={'done': Autonomy.Off})

			# x:960 y:70
			OperatableStateMachine.add('Log Recovered',
										LogState(text="Re-plan after recovery", severity=Logger.REPORT_HINT),
										transitions={'done': 'New Plan'},
										autonomy={'done': Autonomy.Off})

			# x:772 y:71
			OperatableStateMachine.add('New Plan',
										GetPathState(planner_topic="high_level_planner"),
										transitions={'planned': 'Container', 'empty': 'Receive Goal', 'failed': 'Continue'},
										autonomy={'planned': Autonomy.Off, 'empty': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'goal': 'goal', 'plan': 'plan'})

			# x:203 y:113
			OperatableStateMachine.add('Receive Goal',
										GetPoseState(topic='flex_nav_global/goal'),
										transitions={'done': 'Receive Path'},
										autonomy={'done': Autonomy.Low},
										remapping={'goal': 'goal'})

			# x:866 y:374
			OperatableStateMachine.add('Recover',
										OperatorDecisionState(outcomes=["yes","no"], hint="Should we attempt recovery?", suggestion="yes"),
										transitions={'yes': 'LogRecovery', 'no': 'finished'},
										autonomy={'yes': Autonomy.High, 'no': Autonomy.Full})

			# x:887 y:236
			OperatableStateMachine.add('LogRecovery',
										LogState(text="Starting recovery behavior", severity=Logger.REPORT_HINT),
										transitions={'done': 'Turtlebot Simple Recovery'},
										autonomy={'done': Autonomy.Off})

			# x:875 y:162
			OperatableStateMachine.add('AutoReplan',
										OperatorDecisionState(outcomes=["yes","no"], hint="Re-plan to current goal?", suggestion="yes"),
										transitions={'yes': 'Log Recovered', 'no': 'Continue'},
										autonomy={'yes': Autonomy.High, 'no': Autonomy.Full})

			# x:453 y:376
			OperatableStateMachine.add('EStop',
										TimedStopState(timeout=0.25, cmd_topic='stamped_cmd_vel_mux/input/navi', odom_topic='mobile_base/odom'),
										transitions={'done': 'Log Fail', 'failed': 'Log Fail'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

			# x:75 y:417
			OperatableStateMachine.add('initialPub',
										KylePubState(cmd_topic='/makethisupcount', valueToPub=0),
										transitions={'done': 'getVelocity'},
										autonomy={'done': Autonomy.Off})

			# x:215 y:471
			OperatableStateMachine.add('getVelocity',
										SubscriberState(topic='/makethisupvel', blocking=True, clear=False),
										transitions={'received': 'getAng', 'unavailable': 'getCount'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'myvelocity'})

			# x:402 y:461
			OperatableStateMachine.add('getAng',
										SubscriberState(topic='/makethisupang', blocking=True, clear=False),
										transitions={'received': 'Ball_in_image', 'unavailable': 'getCount'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'angularmy'})

			# x:559 y:450
			OperatableStateMachine.add('Ball_in_image',
										KyleVerifyState(ValueToMeasureAgainst=7777.0),
										transitions={'verified': 'getCount', 'notVerified': 'move'},
										autonomy={'verified': Autonomy.Off, 'notVerified': Autonomy.Off},
										remapping={'inputValueVel': 'myvelocity', 'inputValueAng': 'angularmy'})

			# x:706 y:496
			OperatableStateMachine.add('move',
										KyleTwistState(cmd_topic='/turtlebot/stamped_cmd_vel_mux/input/navi'),
										transitions={'done': 'ShouldRobotStop', 'getNewMove': 'getVelocity'},
										autonomy={'done': Autonomy.Off, 'getNewMove': Autonomy.Off},
										remapping={'input_velocity': 'myvelocity', 'input_rotation_rate': 'angularmy'})

			# x:960 y:523
			OperatableStateMachine.add('ShouldRobotStop',
										OperatorDecisionState(outcomes=['yes','no'], hint="Should the Robot Stop?", suggestion=None),
										transitions={'yes': 'finished', 'no': 'Continue'},
										autonomy={'yes': Autonomy.Off, 'no': Autonomy.Off})

			# x:658 y:615
			OperatableStateMachine.add('getCount',
										SubscriberState(topic='/makethisupcount', blocking=True, clear=False),
										transitions={'received': 'verifyCount', 'unavailable': 'ShouldRobotStop'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'mycount'})

			# x:443 y:679
			OperatableStateMachine.add('verifyCount',
										KyleVerifyState(ValueToMeasureAgainst=45),
										transitions={'verified': 'Continue', 'notVerified': 'increaseCount'},
										autonomy={'verified': Autonomy.Off, 'notVerified': Autonomy.Off},
										remapping={'inputValueVel': 'mycount', 'inputValueAng': 'mycount'})

			# x:242 y:708
			OperatableStateMachine.add('increaseCount',
										KylePubInputState(cmd_topic='/makethisupcount', increaseBy=1),
										transitions={'done': 'rotate'},
										autonomy={'done': Autonomy.Off},
										remapping={'valueToIncrease': 'mycount'})

			# x:75 y:709
			OperatableStateMachine.add('rotate',
										TimedTwistState(target_time=.1, velocity=0, rotation_rate=.5, cmd_topic='/turtlebot/stamped_cmd_vel_mux/input/navi'),
										transitions={'done': 'getVelocity'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

	# [/MANUAL_FUNC]
