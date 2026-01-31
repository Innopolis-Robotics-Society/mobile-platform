#include <chrono>
#include <cmath>
#include <rclcpp/rclcpp.hpp>

#include "geometry_msgs/msg/twist.hpp"
#include "overlord100_msgs/msg/wheels_data.hpp"
using std::placeholders::_1;

// Auxiliary node to check the velocity published by the controller
class ControllerSubscriber : public rclcpp::Node {
   public:
    ControllerSubscriber() : Node("controller_subscriber") {
        subscription_ =
            this->create_subscription<overlord100_msgs::msg::WheelsData>(
                "wheels_control", 10,
                std::bind(&ControllerSubscriber::topic_callback, this, _1));
    }

   private:
    void topic_callback(
        const overlord100_msgs::msg::WheelsData wheels_data) const {
        RCLCPP_INFO(this->get_logger(), "I heard sth //'%s'",
                    std::to_string(wheels_data.left).c_str());
    }

    rclcpp::Subscription<overlord100_msgs::msg::WheelsData>::SharedPtr
        subscription_;
};
int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ControllerSubscriber>());
    rclcpp::shutdown();
    return 0;
}
