#!/usr/bin/env python3
# coding: UTF-8

import rospy
import multicast
import math

from consai2_receiver_proto import referee_pb2
from consai2_msgs.msg import Referee
from geometry_msgs.msg import Point


class RefereeReceiver(object):
    def __init__(self):
        self._HOST = rospy.get_param('consai2_description/referee_addr', '224.5.23.1')
        self._PORT = rospy.get_param('consai2_description/referee_port', 10003)
        self._sock = multicast.Multicast(self._HOST, self._PORT)

        self._pub_referee = rospy.Publisher('~raw_referee', Referee, queue_size=1)

    def receive(self):
        BUF_LENGTH = 2048

        buf = self._sock.recv(BUF_LENGTH)

        if buf:
            self._publish_referee(buf)

    def _publish_referee(self, buf):
        packet_referee = referee_pb2.SSL_Referee()
        packet_referee.ParseFromString(buf)

        referee = Referee()
        referee.packet_timestamp = packet_referee.packet_timestamp
        referee.stage = packet_referee.stage
        if packet_referee.HasField('stage_time_left'):
            referee.stage_time_left = packet_referee.stage_time_left
        referee.command = packet_referee.command
        referee.command_counter = packet_referee.command_counter
        referee.command_timestamp = packet_referee.command_timestamp
        referee.yellow = packet_referee.yellow
        referee.blue = packet_referee.blue

        if packet_referee.HasField('designated_position'):
            referee.designated_position = Point(
                    packet_referee.designated_position.x * 0.001, # millimeter to meter
                    packet_referee.designated_position.y * 0.001, # millimeter to meter
                    0)
        
        if packet_referee.HasField('blueTeamOnPositiveHalf'):
            referee.blue_team_on_positive_half = packet_referee.blueTeamOnPositiveHalf

        if packet_referee.HasField('gameEvent'):
            referee.game_event.game_event_type = packet_referee.gameEvent.gameEventType
            if packet_referee.gameEvent.HasField('originator'):
                referee.game_event.originator_team = packet_referee.gameEvent.originator.team
                if packet_referee.gameEvent.originator.HasField('botId'):
                    referee.game_event.originator_bot_id = packet_referee.gameEvent.originator.botId
            if packet_referee.gameEvent.HasField('message'):
                referee.game_event.message = packet_referee.gameEvent.message

        self._pub_referee.publish(referee)


if __name__ == '__main__':
    rospy.init_node('referee_receiver')

    receiver = RefereeReceiver()

    r   = rospy.Rate(60)
    while not rospy.is_shutdown():
        receiver.receive()

        r.sleep()
