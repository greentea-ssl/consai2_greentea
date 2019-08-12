#include <world_observer/geometry/geometry.hpp>

#include <tf/transform_datatypes.h>


namespace geometry2d
{

Pose::Pose()
{
    this->x = 0.0;
    this->y = 0.0;
    this->theta = 0.0;
}

Pose::Pose(geometry_msgs::Pose   pose)
{
    this->x = pose.position.x;
    this->y = pose.position.y;
    this->theta = YawFromQuaternion(pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w);
    this->theta = pi2pi(this->theta);
}

Pose::Pose(geometry_msgs::Pose2D pose)
{
    this->x = pose.x;
    this->y = pose.y;
    this->theta = pose.theta;
    this->theta = pi2pi(this->theta);
}

MatrixWrapper::ColumnVector Pose::ToColumnVector()
{
    MatrixWrapper::ColumnVector  measurement(3);

    measurement(1) = this->x;
    measurement(2) = this->y;
    measurement(3) = this->theta;

    return  measurement;
}

Velocity::Velocity()
{
    this->x = 0.0;
    this->y = 0.0;
    this->theta = 0.0;
}

Velocity::Velocity(double x, double y, double theta)
{
    this->x = x;
    this->y = y;
    this->theta = theta;
}


Velocity::Velocity(geometry_msgs::Twist twist)
{
    this->x = twist.linear.x;
    this->y = twist.linear.y;
    this->theta = twist.angular.z;
}


Accel::Accel()
{
    this->x = 0.0;
    this->y = 0.0;
    this->theta = 0.0;
}

Accel::Accel(double x, double y, double theta)
{
    this->x = x;
    this->y = y;
    this->theta = theta;
}


Accel::Accel(geometry_msgs::Accel accel)
{
    this->x = accel.linear.x;
    this->y = accel.linear.y;
    this->theta = accel.angular.z;
}

Odometry::Odometry()
{
}

Odometry::Odometry(Pose pose, Velocity velocity)
{
    this->pose = pose;
    this->velocity = velocity;
}

double YawFromQuaternion(double x, double y, double z, double w)
{
    double  roll, pitch, yaw;
    tf::Quaternion  q(x, y, z, w);
    tf::Matrix3x3 m(q);

    m.getRPY(roll, pitch, yaw);

    return yaw;
}

double pi2pi(double rad)
{
    while(rad >=  M_PI) rad -= 2.0*M_PI;
    while(rad <= -M_PI) rad += 2.0*M_PI;
    return rad;
}

}