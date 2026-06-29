#!/usr/bin/env python3
"""
encoders_to_odom — конвертирует скорости энкодеров (RPM) в одометрию.

Подписывается:  /encoders_velocities  (iros_mobile_platform_msgs/WheelsData)
Публикует:      /iros_mobile_platform_controller/odom  (nav_msgs/Odometry)
                TF: odom -> base_link  (только если publish_tf=True)

Параметры ROS:
  wheel_radius  (float, default=0.126)   — радиус колеса, метры
  robot_base    (float, default=0.62)    — расстояние между колёсами, метры
  publish_tf    (bool,  default=False)   — публиковать TF odom->base_link
                                           (False если запущен EKF — он сам публикует)
  odom_frame    (str,   default='odom')
  base_frame    (str,   default='base_link')
"""

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TransformStamped, Quaternion
from nav_msgs.msg import Odometry
from iros_mobile_platform_msgs.msg import WheelsData
from tf2_ros import TransformBroadcaster


def euler_to_quaternion(yaw: float) -> Quaternion:
    """Конвертирует угол yaw в кватернион (roll=0, pitch=0)."""
    q = Quaternion()
    q.x = 0.0
    q.y = 0.0
    q.z = math.sin(yaw / 2.0)
    q.w = math.cos(yaw / 2.0)
    return q


class EncodersToOdom(Node):
    def __init__(self):
        super().__init__('encoders_to_odom')

        # ── Параметры ──────────────────────────────────────────────────────
        self.declare_parameter('wheel_radius', 0.126)
        self.declare_parameter('robot_base',   0.62)
        self.declare_parameter('publish_tf',   False)
        self.declare_parameter('odom_frame',   'odom')
        self.declare_parameter('base_frame',   'base_link')

        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.robot_base   = self.get_parameter('robot_base').value
        self.publish_tf_  = self.get_parameter('publish_tf').value
        self.odom_frame   = self.get_parameter('odom_frame').value
        self.base_frame   = self.get_parameter('base_frame').value

        self.get_logger().info(
            f'encoders_to_odom: wheel_radius={self.wheel_radius}, '
            f'robot_base={self.robot_base}, publish_tf={self.publish_tf_}'
        )

        # ── Состояние одометрии ────────────────────────────────────────────
        self.x     = 0.0
        self.y     = 0.0
        self.theta = 0.0
        self.last_time = self.get_clock().now()

        # ── Скорости (для публикации в Odometry.twist) ─────────────────────
        self.linear_vel  = 0.0
        self.angular_vel = 0.0

        # ── Pub / Sub / TF ─────────────────────────────────────────────────
        self.odom_pub = self.create_publisher(
            Odometry,
            'iros_mobile_platform_controller/odom',
            10
        )

        if self.publish_tf_:
            self.tf_broadcaster = TransformBroadcaster(self)

        self.create_subscription(
            WheelsData,
            'encoders_velocities',
            self._encoders_callback,
            10
        )

    # ── Колбек энкодеров ───────────────────────────────────────────────────
    def _encoders_callback(self, msg: WheelsData):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9

        # Защита от слишком большого dt (пауза в данных или первый пакет)
        if dt <= 0.0 or dt > 1.0:
            self.last_time = current_time
            return

        # RPM → линейная скорость колеса (м/с)
        # Левое колесо физически вращается в обратную сторону при движении вперёд
        v_left  = -msg.left  * (2.0 * math.pi / 60.0) * self.wheel_radius
        v_right =  msg.right * (2.0 * math.pi / 60.0) * self.wheel_radius

        # Дифференциальная кинематика
        self.linear_vel  = (v_left + v_right) / 2.0
        self.angular_vel = (v_right - v_left) / self.robot_base

        # Интегрирование позиции (метод трапеций для угла)
        delta_theta = self.angular_vel * dt
        self.theta  += delta_theta

        # Стандартная формула REP-105: X — вперёд, Y — влево
        self.x += self.linear_vel * math.cos(self.theta) * dt
        self.y += self.linear_vel * math.sin(self.theta) * dt

        self.last_time = current_time

        self._publish(current_time)

    # ── Публикация ─────────────────────────────────────────────────────────
    def _publish(self, stamp):
        now = stamp.to_msg()
        q   = euler_to_quaternion(self.theta)

        # ── nav_msgs/Odometry ──────────────────────────────────────────────
        odom = Odometry()
        odom.header.stamp    = now
        odom.header.frame_id = self.odom_frame
        odom.child_frame_id  = self.base_frame

        odom.pose.pose.position.x  = self.x
        odom.pose.pose.position.y  = self.y
        odom.pose.pose.position.z  = 0.0
        odom.pose.pose.orientation = q

        # Ковариация позиции (диагональ: x, y, z, roll, pitch, yaw)
        odom.pose.covariance = [
            0.01, 0.0,  0.0,  0.0,  0.0,  0.0,
            0.0,  0.01, 0.0,  0.0,  0.0,  0.0,
            0.0,  0.0,  1e9,  0.0,  0.0,  0.0,
            0.0,  0.0,  0.0,  1e9,  0.0,  0.0,
            0.0,  0.0,  0.0,  0.0,  1e9,  0.0,
            0.0,  0.0,  0.0,  0.0,  0.0,  0.05,
        ]

        odom.twist.twist.linear.x  = self.linear_vel
        odom.twist.twist.angular.z = self.angular_vel

        # Ковариация скоростей
        odom.twist.covariance = [
            0.01, 0.0,  0.0,  0.0,  0.0,  0.0,
            0.0,  1e9,  0.0,  0.0,  0.0,  0.0,
            0.0,  0.0,  1e9,  0.0,  0.0,  0.0,
            0.0,  0.0,  0.0,  1e9,  0.0,  0.0,
            0.0,  0.0,  0.0,  0.0,  1e9,  0.0,
            0.0,  0.0,  0.0,  0.0,  0.0,  0.05,
        ]

        self.odom_pub.publish(odom)

        # ── TF odom → base_link (только если publish_tf=True) ─────────────
        if self.publish_tf_:
            t = TransformStamped()
            t.header.stamp    = now
            t.header.frame_id = self.odom_frame
            t.child_frame_id  = self.base_frame

            t.transform.translation.x = self.x
            t.transform.translation.y = self.y
            t.transform.translation.z = 0.0
            t.transform.rotation      = q

            self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = EncodersToOdom()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
