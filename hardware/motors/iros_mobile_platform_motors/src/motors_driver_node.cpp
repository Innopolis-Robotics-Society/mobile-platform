#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
// #include "std_msgs/msg/string.hpp"
#include <algorithm>
#include <diagnostic_msgs/msg/diagnostic_status.hpp>
#include <vector>

#include "can_msgs/msg/frame.hpp"
#include "iros_mobile_platform_msgs/msg/wheels_data.hpp"

using std::placeholders::_1;
using namespace std::chrono_literals;

#define CAN_OUT_TOPIC "/CAN/can0/transmit"
#define CAN_IN_TOPIC "/CAN/can0/receive"

#define VELOCITY_CONTROL_TOPIC "/wheels_control"

#define HEARTBEAT_EXPIRE 2
// TODO: check if 0x05 state is present at any time
// (0x7F is "pre-operational", and 0x05 is "operating" state)
#define HEARTBEAT_TARGET_STATE 0x7F

#define NODE_ID 1

class MotorsDriverNode : public rclcpp::Node {
 public:
  MotorsDriverNode() : Node("motors_driver_node") {
    this->declare_parameter<std::string>("hardware_id", "motor_driver");
    this->get_parameter_or<std::string>("hardware_id", hardware_id,
                                        "motor_driver");

    // subscription_ = this->create_subscription<std_msgs::msg::String>(
    // "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));

    wheels_velocities_input =
        this->create_subscription<iros_mobile_platform_msgs::msg::WheelsData>(
            VELOCITY_CONTROL_TOPIC, 10,
            std::bind(&MotorsDriverNode::topic_callback, this, _1));

    can_output =
        this->create_publisher<can_msgs::msg::Frame>(CAN_OUT_TOPIC, 10);

    heartbeat = this->create_subscription<can_msgs::msg::Frame>(
        CAN_IN_TOPIC, 10,
        std::bind(&MotorsDriverNode::get_heartbeat, this, _1));

    syncronous_velocity_control_init();

    last_beat = this->now();
    // timer_ = this->create_wall_timer(500ms,
    // std::bind(&MotorsDriverNode::syncronous_velocity_control_init, this));

    status_pub = this->create_publisher<diagnostic_msgs::msg::DiagnosticStatus>(
        "status", rclcpp::QoS(rclcpp::KeepLast(10)));

    status_update_timer = this->create_wall_timer(
        1s, std::bind(&MotorsDriverNode::publish_status, this));
  }

 private:
  void publish_status() {
    auto msg = std::make_shared<diagnostic_msgs::msg::DiagnosticStatus>();
    msg->hardware_id = hardware_id;
    msg->values = {};
    msg->name = "";

    if ((this->now() - this->last_beat).seconds() > HEARTBEAT_EXPIRE) {
      msg->level = diagnostic_msgs::msg::DiagnosticStatus::STALE;
      msg->message = "Disconnected or lost";
    } else {
      if (last_heartbeat_state == HEARTBEAT_TARGET_STATE) {
        msg->level = diagnostic_msgs::msg::DiagnosticStatus::OK;
        msg->message = "Running";
      } else {
        msg->level = diagnostic_msgs::msg::DiagnosticStatus::WARN;
        msg->message = "Connected, but in wrong state of operation";
      }
    }
    status_pub->publish(*msg);
  }

  void topic_callback(const iros_mobile_platform_msgs::msg::WheelsData &msg) {
    // Make int
    int left = std::round(msg.left);
    int right = std::round(msg.right);

    // Bound velocity between -255 and 255 rev/min
    left = -std::clamp(left, -0xFF, 0xFF);
    right = std::clamp(right, -0xFF, 0xFF);

    // Send data over CAN
    can_msgs::msg::Frame CANmsg =
        synchronized_velocity_send_frame((u_int16_t)left, (u_int16_t)right);
    can_output->publish(CANmsg);
  }

  can_msgs::msg::Frame synchronized_velocity_send_frame(u_int16_t l,
                                                        u_int16_t r) {
    // Server send function code = 1100 (0xC)
    u_int32_t COB_ID = (0xC << 7) + (u_int32_t)NODE_ID;  // 0x600 + id

    std::array<uint8_t, 8UL> data;
    data[0] = 0x23;  // Send request
    data[1] = 0xFF;
    data[2] = 0x60;  // 0x60FF - index
    data[3] = 0x03;  // subindex
    data[4] = l;     // left wheel velocity
    data[5] = l >> 8;
    data[6] = r;  // right wheel velocity
    data[7] = r >> 8;

    can_msgs::msg::Frame frame;

    frame.id = COB_ID;
    frame.dlc = 8;
    frame.data = data;

    return frame;
  }

  void syncronous_velocity_control_init() {
    RCLCPP_INFO(this->get_logger(), "OK\n");

    std::vector<std::array<uint8_t, 8UL>> commands =
        std::vector<std::array<uint8_t, 8UL>>({
            {0x2B, 0x17, 0x10, 0x00, 0xE8, 0x03, 0x00, 0x00},
            {0x2B, 0x0F, 0x20, 0x00, 0x01, 0x00, 0x00, 0x00},
            {0x2F, 0x60, 0x60, 0x00, 0x03, 0x00, 0x00, 0x00},
            {0x23, 0x83, 0x60, 0x01, 0x64, 0x00, 0x00, 0x00},
            {0x23, 0x83, 0x60, 0x02, 0x64, 0x00, 0x00, 0x00},
            {0x23, 0x84, 0x60, 0x01, 0x64, 0x00, 0x00, 0x00},
            {0x23, 0x84, 0x60, 0x02, 0x64, 0x00, 0x00, 0x00},
            {0x2B, 0x40, 0x60, 0x00, 0x06, 0x00, 0x00, 0x00},
            {0x2B, 0x40, 0x60, 0x00, 0x07, 0x00, 0x00, 0x00},
            {0x2B, 0x40, 0x60, 0x00, 0x0F, 0x00, 0x00, 0x00},

        });

    // for(int i == 0; i < commands.size(); i++) {
    //   can_msgs::msg::Frame msg = can_msgs::msg::Frame();
    //   msg.
    // };

    for (std::array<uint8_t, 8UL> command : commands) {
      can_msgs::msg::Frame msg;
      msg.id = (0xC << 7) + (u_int32_t)NODE_ID;
      msg.dlc = 8;
      msg.data = command;

      can_output->publish(msg);
    }
  }

  void get_heartbeat(const can_msgs::msg::Frame &msg) {
    if (msg.id != 0x700 + NODE_ID) return;

    last_heartbeat_state = msg.data[0];

    if ((this->now() - this->last_beat).seconds() > HEARTBEAT_EXPIRE)
      syncronous_velocity_control_init();
    this->last_beat = this->now();
  }

  rclcpp::Subscription<iros_mobile_platform_msgs::msg::WheelsData>::SharedPtr
      wheels_velocities_input;
  rclcpp::Subscription<can_msgs::msg::Frame>::SharedPtr heartbeat;
  rclcpp::Publisher<can_msgs::msg::Frame>::SharedPtr can_output;
  rclcpp::Publisher<diagnostic_msgs::msg::DiagnosticStatus>::SharedPtr
      status_pub;

  rclcpp::TimerBase::SharedPtr status_update_timer;
  rclcpp::Time last_beat;
  std::string hardware_id;

  uint8_t last_heartbeat_state = 0x04;

  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MotorsDriverNode>());
  rclcpp::shutdown();
  return 0;
}
