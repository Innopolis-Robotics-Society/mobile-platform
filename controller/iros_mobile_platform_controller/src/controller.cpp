#include <geometry_msgs/msg/twist.hpp>
#include <rclcpp/rclcpp.hpp>

#include "iros_mobile_platform_msgs/msg/wheels_data.hpp"

#define M_PI 3.14159265358979323846 /* pi */

/*
Node implementing differential drive controller

Subscribes: Twist message over /cmd_vel topic

Sublishes: WheelsData message over the /wheels_control topic (velocity in rpm by
default)
*/
class DiffDriveController : public rclcpp::Node {
 public:
  DiffDriveController() : Node("diff_drive_controller") {
    // Parameters for the differential drive robot
    this->declare_parameter<double>("robot_base_",
                                    0.62);  // Distance between the wheels (measured)
    this->declare_parameter<double>("wheel_radius_",
                                    0.065);  // Radius of the wheels (measured)
    this->declare_parameter<std::string>("measurement_units_", "rpm");

    this->get_parameter("robot_base_", robot_base_);
    this->get_parameter("wheel_radius_", wheel_radius_);
    this->half_robot_base_ = robot_base_ / 2;

    // Subscriber to the cmd_vel topic
    cmd_vel_sub_ = this->create_subscription<geometry_msgs::msg::Twist>(
        "cmd_vel", 10,
        std::bind(&DiffDriveController::cmdVelCallback, this,
                  std::placeholders::_1));

    // Publisher for the wheel velocities
    wheels_pub_ = this->create_publisher<iros_mobile_platform_msgs::msg::WheelsData>(
        "wheels_control", 10);
  }

 private:
  static constexpr double UPPER_VELOCITY_LIMIT = 100.0;
  static constexpr double LOWER_VELOCITY_LIMIT = -100.0;

  void velocityHandler(const geometry_msgs::msg::Twist::SharedPtr msg) {
    auto clampAndCheckValidValues = [&](double& vel_value) {
      if (vel_value > UPPER_VELOCITY_LIMIT) {
        vel_value = UPPER_VELOCITY_LIMIT;
      } else if (vel_value < LOWER_VELOCITY_LIMIT) {
        vel_value = LOWER_VELOCITY_LIMIT;
      }
    };
    clampAndCheckValidValues(msg->linear.x);
    clampAndCheckValidValues(msg->linear.y);
    clampAndCheckValidValues(msg->angular.z);

    auto clampAndCheckNonExistingComponents = [&](double& vel_value) {
      vel_value = 0;
    };

    clampAndCheckNonExistingComponents(msg->linear.z);
    clampAndCheckNonExistingComponents(msg->angular.x);
    clampAndCheckNonExistingComponents(msg->angular.y);
  }

  void cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg) {
    velocityHandler(msg);
    // Extract linear and angular velocities from the message
    double lin_vx = msg->linear.x;
    double lin_vy = msg->linear.y;
    double linear_velocity = std::sqrt(lin_vx * lin_vx + lin_vy * lin_vy);

    if (lin_vx < 0 || lin_vy < 0) {
      linear_velocity = -linear_velocity;
    }
    double angular_velocity = msg->angular.z;

    // Compute the wheel velocities
    double angular_right =
        (linear_velocity + this->half_robot_base_ * angular_velocity) /
        (wheel_radius_);
    double angular_left =
        (linear_velocity - this->half_robot_base_ * angular_velocity) /
        (wheel_radius_);
    double angular_right_rpm = angular_right * 30 / M_PI;
    double angular_left_rpm = angular_left * 30 / M_PI;

    // Create and publish the custom message
    auto wheels_msg = iros_mobile_platform_msgs::msg::WheelsData();
    wheels_msg.left = static_cast<float>(angular_left_rpm);
    wheels_msg.right = static_cast<float>(angular_right_rpm);

    RCLCPP_INFO(this->get_logger(), "Publishing wheels_msg.left: '%s'",
                std::to_string(wheels_msg.left).c_str());
    RCLCPP_INFO(this->get_logger(), "Publishing wheels_msg.right: '%s'",
                std::to_string(wheels_msg.right).c_str());
    RCLCPP_INFO(this->get_logger(), "Robot base '%d'",
                this->get_parameter("robot_base_", robot_base_));
    std::cout << robot_base_ << std::endl;

    wheels_pub_->publish(wheels_msg);
  }

  rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_sub_;
  rclcpp::Publisher<iros_mobile_platform_msgs::msg::WheelsData>::SharedPtr wheels_pub_;

  double wheel_radius_;
  double robot_base_;
  double half_robot_base_;
};

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<DiffDriveController>());
  rclcpp::shutdown();
  return 0;
}
