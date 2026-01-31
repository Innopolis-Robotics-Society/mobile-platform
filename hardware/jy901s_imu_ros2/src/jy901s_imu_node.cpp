#include <atomic>
#include <thread>
#include <string>
#include <stdint.h>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include <sensor_msgs/msg/magnetic_field.hpp>
#include <sensor_msgs/msg/nav_sat_fix.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <geometry_msgs/msg/quaternion.hpp>
#include "wit_c_sdk.hpp"
#include "serial.hpp"
#include "REG.hpp"


#define ACC_UPDATE 0x01
#define GYRO_UPDATE 0x02
#define ANGLE_UPDATE 0x04
#define MAG_UPDATE 0x08
#define READ_UPDATE 0x80
#define GPS_UPDATE 0x03

static int fd, s_iCurBaud = 38400;
static volatile char s_cDataUpdate = 0;

//const int c_uiBaud[] = {2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600};
const int c_uiBaud[] = {38400};

static void AutoScanSensor(char *dev);
static void SensorDataUpdata(uint32_t uiReg, uint32_t uiRegNum);
static void Delayms(uint16_t ucMs);

#define PI 3.14159265358979323846

class ImuPublisher : public rclcpp::Node {
public:
    ImuPublisher()
        : Node("jy901s_imu_publisher")
    {
        this->declare_parameter("port", "/dev/ttyTHS0");
        this->declare_parameter("baudrate", 38400);
        this->declare_parameter("reverse_pitch_roll", false);

        this->port = this->get_parameter("port").as_string();
        this->baudrate = this->get_parameter("baudrate").as_int();
        this->reverse_pitch_roll = this->get_parameter("reverse_pitch_roll").as_bool();

        imu_pub = this->create_publisher<sensor_msgs::msg::Imu>("imu/data_raw", 1000);
        mag_pub = this->create_publisher<sensor_msgs::msg::MagneticField>("imu/mag", 1000);
        gps_pub = this->create_publisher<sensor_msgs::msg::NavSatFix>("gps/fix", 1000);
        //timer = nh.createTimer(ros::Duration(0.005), &ImuPublisher::imuPublishCallback, this); // 200 Hz

        printf("Trying to open %s at %lu\r\n", port.c_str(), baudrate);
        if ((fd = serial_open(const_cast<char*>(port.c_str()), baudrate) < 0))
	    {
	        printf("Error opening serial port ... exiting ....\r\n");
            //ROS_ERROR("Error opening serial port ... exiting ....");
            //this->~ImuPublisher();
            return;
	    }
	    else
	        printf("Opened serial port: %s at baudrate: %d\r\n", port.c_str(), static_cast<int>(baudrate));
		    //ROS_INFO("Opened serial port: %s at baudrate: %d", port.c_str(), static_cast<int>(baudrate));

        WitInit(WIT_PROTOCOL_NORMAL, 0x50);
	    WitRegisterCallBack(SensorDataUpdata);

        //ROS_INFO("Starting to publish imu data ...");
	    AutoScanSensor(const_cast<char*>(port.c_str()));

        pubThread = std::thread(&ImuPublisher::imuPublish, this);
    }

    ~ImuPublisher() {
        running = false;
        if (pubThread.joinable()) {
            pubThread.join();
        }
        serial_close(fd);
    }

    void imuPublish() {

        while(running) {

            while (serial_read_data(fd, reinterpret_cast<unsigned char*>(cBuff), 1))
            {
                WitSerialDataIn(cBuff[0]);
            }
            Delayms(2);

            if (s_cDataUpdate)
            {
                if(reverse_pitch_roll == false)
                {
                    for (size_t i = 0; i < 3; i++)
                    {
                        fAcc[i] = sReg[AX + i] / 32768.0f * 16.0f * 9.8f;
                        fGyro[i] = sReg[GX + i] / 32768.0f * 2000.0f * (PI / 180.0f);
                        fAngle[i] = sReg[Roll + i] / 32768.0f * 180.0f * (PI / 180.0f);
                    }
                }
                else
                {

                    fAcc[0] = sReg[AX + 1] / 32768.0f * 16.0f * 9.8f;
                    fAcc[1] = sReg[AX + 0] / 32768.0f * 16.0f * 9.8f;
                    fAcc[2] = sReg[AX + 2] / 32768.0f * 16.0f * 9.8f;

                    fGyro[0] = sReg[GX + 1] / 32768.0f * 2000.0f * (PI / 180.0f);
                    fGyro[1] = sReg[GX + 0] / 32768.0f * 2000.0f * (PI / 180.0f);
                    fGyro[2] = sReg[GX + 2] / 32768.0f * 2000.0f * (PI / 180.0f);

                    fAngle[0] = sReg[Roll + 1] / 32768.0f * 180.0f * (PI / 180.0f);
                    fAngle[1] = sReg[Roll + 0] / 32768.0f * 180.0f * (PI / 180.0f);
                    fAngle[2] = sReg[Roll + 2] / 32768.0f * 180.0f * (PI / 180.0f);
                    
                   // ROS_INFO("Using reverse pitch roll ---- ");

                }

                // if acc, gyro and angle are updated
                if ((s_cDataUpdate & ACC_UPDATE) && (s_cDataUpdate & GYRO_UPDATE) && (s_cDataUpdate & ANGLE_UPDATE))
                {
                    auto imu_msg = sensor_msgs::msg::Imu();
                    imu_msg.header.stamp = rclcpp::Clock{RCL_ROS_TIME}.now(); // careful with it
                    imu_msg.header.frame_id = "imu_link";

                    imu_msg.linear_acceleration.x = fAcc[0];
                    imu_msg.linear_acceleration.y = fAcc[1];
                    imu_msg.linear_acceleration.z = fAcc[2];

                    // set linear acc covariance
                    imu_msg.linear_acceleration_covariance[0] = 0.05;
                    imu_msg.linear_acceleration_covariance[1] = 0.0;
                    imu_msg.linear_acceleration_covariance[2] = 0.0;
                    imu_msg.linear_acceleration_covariance[3] = 0.0;
                    imu_msg.linear_acceleration_covariance[4] = 0.05;
                    imu_msg.linear_acceleration_covariance[5] = 0.0;
                    imu_msg.linear_acceleration_covariance[6] = 0.0;
                    imu_msg.linear_acceleration_covariance[7] = 0.0;
                    imu_msg.linear_acceleration_covariance[8] = 0.05;

                    imu_msg.angular_velocity.x = fGyro[0];
                    imu_msg.angular_velocity.y = fGyro[1];
                    imu_msg.angular_velocity.z = fGyro[2];

                    // set angular vel covariance
                    imu_msg.angular_velocity_covariance[0] = 0.01;
                    imu_msg.angular_velocity_covariance[1] = 0.0;
                    imu_msg.angular_velocity_covariance[2] = 0.0;
                    imu_msg.angular_velocity_covariance[3] = 0.0;
                    imu_msg.angular_velocity_covariance[4] = 0.01;
                    imu_msg.angular_velocity_covariance[5] = 0.0;
                    imu_msg.angular_velocity_covariance[6] = 0.0;
                    imu_msg.angular_velocity_covariance[7] = 0.0;
                    imu_msg.angular_velocity_covariance[8] = 0.01;

                    tf2::Quaternion q;
                    q.setRPY(fAngle[0], fAngle[1], fAngle[2]);

                    imu_msg.orientation.x = q.x();
                    imu_msg.orientation.y = q.y();
                    imu_msg.orientation.z = q.z();
                    imu_msg.orientation.w = q.w();

                    // set orientation covariance
                    imu_msg.orientation_covariance[0] = 0.1;
                    imu_msg.orientation_covariance[1] = 0.0;
                    imu_msg.orientation_covariance[2] = 0.0;
                    imu_msg.orientation_covariance[3] = 0.0;
                    imu_msg.orientation_covariance[4] = 0.1;
                    imu_msg.orientation_covariance[5] = 0.0;
                    imu_msg.orientation_covariance[6] = 0.0;
                    imu_msg.orientation_covariance[7] = 0.0;
                    imu_msg.orientation_covariance[8] = 0.1;

                    imu_pub->publish(imu_msg);

                    s_cDataUpdate &= ~ACC_UPDATE;
                    s_cDataUpdate &= ~GYRO_UPDATE;
                    s_cDataUpdate &= ~ANGLE_UPDATE;
                }

                // if mag updated
                if (s_cDataUpdate & MAG_UPDATE)
                {
                    auto mag_msg = sensor_msgs::msg::MagneticField();
                    mag_msg.header.stamp = rclcpp::Clock{RCL_ROS_TIME}.now();
                    mag_msg.header.frame_id = "imu_link";

                    mag_msg.magnetic_field.x = sReg[HX];
                    mag_msg.magnetic_field.y = sReg[HY];
                    mag_msg.magnetic_field.z = sReg[HZ];

                    //set mag covariance
                    mag_msg.magnetic_field_covariance[0] = 0.01;
                    mag_msg.magnetic_field_covariance[1] = 0.0;
                    mag_msg.magnetic_field_covariance[2] = 0.0;
                    mag_msg.magnetic_field_covariance[3] = 0.0;
                    mag_msg.magnetic_field_covariance[4] = 0.01;
                    mag_msg.magnetic_field_covariance[5] = 0.0;
                    mag_msg.magnetic_field_covariance[6] = 0.0;
                    mag_msg.magnetic_field_covariance[7] = 0.0;
                    mag_msg.magnetic_field_covariance[8] = 0.01;

                    mag_pub->publish(mag_msg);

                    s_cDataUpdate &= ~MAG_UPDATE;
                }

                // if gps updated
                if (s_cDataUpdate & GPS_UPDATE)
                {
                    auto gps_msg = sensor_msgs::msg::NavSatFix();
                    gps_msg.header.stamp = rclcpp::Clock{RCL_ROS_TIME}.now();
                    gps_msg.header.frame_id = "navsat_link";


                    int32_t lonValue = (sReg[LonH] << 8) | sReg[LonL];
                    int32_t latValue = (sReg[LatH] << 8) | sReg[LatL];


                    // Handle negative values if needed
                    if (sReg[LonH] == 0xFF) {
                        lonValue = -((~lonValue) + 1);
                    }
                    if (sReg[LatH] == 0xFF) {
                        latValue = -((~latValue) + 1);
                    }

                    // Convert to decimal degrees
                    double longitude = (lonValue / 60.0) / 100.0;
                    double latitude = (latValue / 60.0) / 100.0;

                    //std::cout << "longitude: " << longitude << std::endl;
                    //std::cout << "latitude: " << latitude << std::endl << std::endl;

                    gps_msg.longitude = (lonValue / 10000000.0 * 100) + ((lonValue  % 10000000) / 10000000.0);
                    gps_msg.latitude = (latValue / 10000000.0 * 100) + ((latValue  % 10000000) / 10000000.0);
                    
                    gps_msg.altitude = 0.0;
                    gps_msg.position_covariance_type = sensor_msgs::msg::NavSatFix::COVARIANCE_TYPE_UNKNOWN;

                    gps_pub->publish(gps_msg);

                    s_cDataUpdate &= ~GPS_UPDATE;
                }

            }

        }

    }

private:
    rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr imu_pub;
    rclcpp::Publisher<sensor_msgs::msg::MagneticField>::SharedPtr mag_pub;
    rclcpp::Publisher<sensor_msgs::msg::NavSatFix>::SharedPtr gps_pub;
    //rclcpp::Timer timer;
    std::atomic<bool> running{true};
    float fAcc[3], fGyro[3], fAngle[3];
	int i, ret;
	char cBuff[1];
    std::thread pubThread;
    std::string port;
    unsigned long baudrate;
    bool reverse_pitch_roll;

};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ImuPublisher>());
    rclcpp::shutdown();
    return 0;
}

static void SensorDataUpdata(uint32_t uiReg, uint32_t uiRegNum)
{
	int i;
	for (i = 0; i < uiRegNum; i++)
	{
		switch (uiReg)
		{
			//            case AX:
			//            case AY:
		case AZ:
			s_cDataUpdate |= ACC_UPDATE;
			break;
			//            case GX:
			//            case GY:
		case GZ:
			s_cDataUpdate |= GYRO_UPDATE;
			break;
			//            case HX:
			//            case HY:
		case HZ:
			s_cDataUpdate |= MAG_UPDATE;
			break;
			//            case Roll:
			//            case Pitch:
		case Yaw:
			s_cDataUpdate |= ANGLE_UPDATE;
			break;
			//			  case LonL:
			//			  case LatL:
		case LatL:
			s_cDataUpdate |= GPS_UPDATE;
		default:
			s_cDataUpdate |= READ_UPDATE;
			break;
		}
		uiReg++;
	}
}

static void Delayms(uint16_t ucMs)
{
	usleep(ucMs * 1000);
}

static void AutoScanSensor(char *dev)
{
	int i, iRetry;
	char cBuff[1];

	for (i = 1; i < sizeof(c_uiBaud); i++)
	{
		serial_close(fd);
        Delayms(1000);
		s_iCurBaud = c_uiBaud[i];
		fd = serial_open(dev, c_uiBaud[i]);

		iRetry = 2;
		do
		{
			s_cDataUpdate = 0;
			WitReadReg(AX, 3);
			Delayms(1000);
			while (serial_read_data(fd, reinterpret_cast<unsigned char*>(cBuff), 1))
			{
				WitSerialDataIn(cBuff[0]);
			}
			if (s_cDataUpdate != 0)
			{
				printf("%d baud find sensor\r\n\r\n", c_uiBaud[i]);
				return;
			}
			iRetry--;
		} while (iRetry);
	}
	printf("can not find sensor\r\n");
	printf("please check your connection\r\n");
}

