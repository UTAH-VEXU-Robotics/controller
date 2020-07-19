#include "ros/ros.h"
#include "std_msgs/String.h"
#include "driver/Action.h"
#include "driver/Actions.h"
#include "driver/ChangeUpField.h"
#include "driver/ChangeUpGoal.h"
#include "driver/ChangeUpGoals.h"
#include "driver/Model.h"
#include "driver/Models.h"
#include "driver/Task.h"
#include "driver/Tasks.h"
#include "driver/Type.h"
#include "driver/Types.h"
#include "driver/Zone.h"
#include "driver/Zones.h"

#include <sstream>
#include <memory>

void chatterCallback(const driver::Models::ConstPtr& imodels){
  for (driver::Model model: imodels->models){
    std::cout << model.zone << "\n";
  }
//  models = imodels.Ptr();
}

int main(int argc, char **argv){
  ros::init(argc, argv, "talker");
  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("field/models", 100, chatterCallback);

  ros::Rate loop_rate(10);

  while (ros::ok()){
    ros::spinOnce();
  }

  return 0;
}
