// #include <chrono>
// #include <memory>

// #include "geometry_msgs/msg/twist.hpp"
// #include "rclcpp/rclcpp.hpp"

// using namespace std::chrono_literals;

// class CmdVelPublisher : public rclcpp::Node {
//    public:
//     CmdVelPublisher() : Node("cmd_vel_publisher"), count_(0) {
//         this->declare_parameter<double>("linear_x", 0.0);
//         this->declare_parameter<double>("linear_y", 0.0);
//         this->declare_parameter<double>("linear_z", 0.0);
//         this->declare_parameter<double>("angular_x", 0.0);
//         this->declare_parameter<double>("angular_y", 0.0);
//         this->declare_parameter<double>("angular_z", 0.0);

//         publisher_ =
//             this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
//         timer_ = this->create_wall_timer(
//             500ms, std::bind(&CmdVelPublisher::publish_velocity, this));
//     }

//    private:
//     void publish_velocity() {
//         double linear_x = this->get_parameter("linear_x").as_double();
//         double linear_y = this->get_parameter("linear_y").as_double();
//         double linear_z = this->get_parameter("linear_z").as_double();
//         double angular_x = this->get_parameter("angular_x").as_double();
//         double angular_y = this->get_parameter("angular_y").as_double();
//         double angular_z = this->get_parameter("angular_z").as_double();

//         auto message = geometry_msgs::msg::Twist();
//         // message.linear.x = -10.0;
//         // message.linear.y = 10.0;
//         // message.linear.z = 0.0;
//         // message.angular.x = 0.0;
//         // message.angular.y = 0.0;
//         // message.angular.z = 100.0;

//         message.linear.x = linear_x;
//         message.linear.y = linear_y;
//         message.linear.z = linear_z;
//         message.angular.x = angular_x;
//         message.angular.y = angular_y;
//         message.angular.z = angular_z;

//         RCLCPP_INFO(this->get_logger(),
//                     "Publishing: linear.x: '%f' angular.z: '%f'",
//                     message.linear.x, message.angular.z);
//         publisher_->publish(message);

//         this->set_parameters(linear_x);

//     }

//     rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
//     rclcpp::TimerBase::SharedPtr timer_;
//     size_t count_;
//     // double linear_x_;
//     // double linear_y_;
//     // double linear_z_;
//     // double angular_x_;
//     // double angular_y_;
//     // double angular_z_;
// };

// int main(int argc, char* argv[]) {
//     rclcpp::init(argc, argv);
//     rclcpp::spin(std::make_shared<CmdVelPublisher>());

//     // rclcpp::Parameter linear_x_("linear_x", 0.0);
//     // rclcpp::Parameter linear_y_("linear_y", 0.0);
//     // rclcpp::Parameter linear_z_("linear_z", 0.0);

//     // rclcpp::Parameter angular_x_("angular_x", 0.0);
//     // rclcpp::Parameter angular_y_("angular_y", 0.0);
//     // rclcpp::Parameter angular_z_("angular_z", 0.0);

//     rclcpp::shutdown();
//     return 0;
// }

#include <chrono>
#include <memory>

#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

// Auxiliary node to publish velocity via the /cmd_vel topic
class CmdVelPublisher : public rclcpp::Node {
 public:
  CmdVelPublisher() : Node("cmd_vel_publisher"), count_(0) {
    publisher_ =
        this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
    timer_ = this->create_wall_timer(
        500ms, std::bind(&CmdVelPublisher::publish_velocity, this));
  }

 private:
  void publish_velocity() {
    auto message = geometry_msgs::msg::Twist();
    message.linear.x = -2.0;
    message.linear.y = 110.0;
    message.linear.z = 0.0;
    message.angular.x = 0.0;
    message.angular.y = 10.0;
    message.angular.z = 0.0;
    RCLCPP_INFO(this->get_logger(),
                "Publishing: linear.x: '%f' angular.z: '%f'", message.linear.x,
                message.angular.z);
    publisher_->publish(message);
  }

  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  size_t count_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<CmdVelPublisher>());
  rclcpp::shutdown();
  return 0;
}
