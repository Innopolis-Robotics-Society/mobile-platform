#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
// #include "std_msgs/msg/string.hpp"
#include <algorithm>
#include <vector>

#include "can_msgs/msg/frame.hpp"
#include "iros_mobile_platform_msgs/msg/wheels_data.hpp"

using std::placeholders::_1;
using namespace std::chrono_literals;

#define PERIOD 50ms

#define CAN_OUT_TOPIC "/CAN/can0/transmit"
#define CAN_IN_TOPIC "/CAN/can0/receive"

#define VELOCITIES_TOPIC "/encoders_velocities"
#define ANGLES_TOPIC "/encoders_positions"

#define NODE_ID 1

class EncodersNode : public rclcpp::Node {
 public:
  EncodersNode() : Node("encoders_node") {
    positions = {0, 0};

    request = this->create_publisher<can_msgs::msg::Frame>(CAN_OUT_TOPIC, 10);

    response = this->create_subscription<can_msgs::msg::Frame>(
        CAN_IN_TOPIC, 10, std::bind(&EncodersNode::get_response, this, _1));

    pub_velocities = this->create_publisher<iros_mobile_platform_msgs::msg::WheelsData>(
        VELOCITIES_TOPIC, 10);
    pub_angles = this->create_publisher<iros_mobile_platform_msgs::msg::WheelsData>(
        ANGLES_TOPIC, 10);

    timer_ = this->create_wall_timer(
        PERIOD, std::bind(&EncodersNode::send_request, this));
  }

 private:
  void get_response(const can_msgs::msg::Frame& msg) {
    if (msg.data[0] != 0x43) return;
    if (msg.data[1] == 0x6C) {
      iros_mobile_platform_msgs::msg::WheelsData vels;
      vels.left = static_cast<int16_t>(msg.data[4] + (msg.data[5] << 8)) * 0.1;
      vels.right = static_cast<int16_t>(msg.data[6] + (msg.data[7] << 8)) * 0.1;
      pub_velocities->publish(vels);
      return;
    }

    if (msg.data[3] == 1 || msg.data[3] == 2) {
      positions[msg.data[3] - 1] =
          static_cast<int32_t>(msg.data[4] + (msg.data[5] << 8) +
                               (msg.data[6] << 16) + (msg.data[7] << 24));
    }

    iros_mobile_platform_msgs::msg::WheelsData angles;
    angles.left = positions[0] / 4096. / 4;
    angles.right = positions[1] / 4096. / 4;
    pub_angles->publish(angles);
  }

  void send_request() {
    std::vector<std::array<uint8_t, 8UL>> commands =
        std::vector<std::array<uint8_t, 8UL>>(
            {{0x40, 0x6C, 0x60, 0x03, 0x00, 0x00, 0x00, 0x00},
             {0x40, 0x64, 0x60, 0x01, 0x00, 0x00, 0x00, 0x00},
             {0x40, 0x64, 0x60, 0x02, 0x00, 0x00, 0x00, 0x00}});

    for (auto command : commands) {
      can_msgs::msg::Frame msg;
      msg.id = (0xC << 7) + (u_int32_t)NODE_ID;
      msg.dlc = 8;
      msg.data = command;

      request->publish(msg);
    }
  }

  std::array<int32_t, 2L> positions;

  rclcpp::Publisher<iros_mobile_platform_msgs::msg::WheelsData>::SharedPtr
      pub_velocities;
  rclcpp::Publisher<iros_mobile_platform_msgs::msg::WheelsData>::SharedPtr pub_angles;

  rclcpp::Publisher<can_msgs::msg::Frame>::SharedPtr request;
  rclcpp::Subscription<can_msgs::msg::Frame>::SharedPtr response;

  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<EncodersNode>());
  rclcpp::shutdown();
  return 0;
}
