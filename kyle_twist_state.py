#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyPublisher
from flexbe_core.proxy import ProxySubscriberCached
from flexbe_core.proxy import ProxyServiceCaller
from flexbe_core.proxy import ProxyActionClient

from geometry_msgs.msg import TwistStamped


class KyleTwistState(EventState):
    '''
    This state publishes an open loop constant TwistStamped command based on parameters.

    -- target_time     float     Time which needs to have passed since the behavior started.
    -- velocity        float     Body velocity (m/s)
    -- rotation_rate   float     Angular rotation (radians/s)
    -- cmd_topic       string    topic name of the robot velocity command (default: 'cmd_vel')
    <= done                 Given time has passed.
    '''

    def __init__(self, cmd_topic='cmd_vel'):
        # Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
        super(KyleTwistState, self).__init__(outcomes = ['done','getNewMove'],
                                             input_keys=['input_velocity','input_rotation_rate'])

        # Store state parameter for later use.
        #self._target_time           = rospy.Duration(target_time)
        self._twist                 = TwistStamped()
        #self._twist.twist.linear.x  = velocity
        #self._twist.twist.angular.z = rotation_rate

        # The constructor is called when building the state machine, not when actually starting the behavior.
        # Thus, we cannot save the starting time now and will do so later.
        self._start_time = None

        self._done       = None # Track the outcome so we can detect if transition is blocked

        self._cmd_topic    = cmd_topic
        self._pub          = ProxyPublisher(       {self._cmd_topic: TwistStamped})

    def execute(self, userdata):
        # This method is called periodically while the state is active.
        # If no outcome is returned, the state will stay active.

    #    if (self._done):
            # We have completed the state, and therefore must be blocked by autonomy level
            # Stop the robot, but and return the prior outcome
    #        ts = TwistStamped() # Zero twist to stop if blocked
    #        ts.header.stamp = rospy.Time.now()
    #        self._pub.publish(self._cmd_topic, ts)
    #        return self._done

    #    if rospy.Time.now() - self._start_time > self._target_time:
            # Normal completion, do not bother repeating the publish
    #        self._done = 'done'
    #        return 'done'

        # Normal operation
        #self._twist.twist.linear.x = 1.0
        #self._twist.twist.angular.z = 1.0

        self._twist.twist.linear.x = userdata.input_velocity.data/1000
        self._twist.twist.angular.z = userdata.input_rotation_rate.data/1000

        self._twist.header.stamp = rospy.Time.now()  # update the timestamp
        self._pub.publish(self._cmd_topic, self._twist)
        if (userdata.input_rotation_rate.data > -35) and (userdata.input_rotation_rate.data < 35) :
            return 'done'
        return 'getNewMove'

    def on_enter(self, userdata):
        # This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
        self._start_time = rospy.Time.now()
        self._done       = None # reset the completion flag
        #self._twist.twist.linear.x = 1.0
        #self._twist.twist.angular.z = 1.0
        self._twist.twist.linear.x = userdata.input_velocity.data/1000
        self._twist.twist.angular.z = userdata.input_rotation_rate.data/1000
