#!/usr/bin/env python
import roslib
import rospy
import numpy
import time
import math
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose,Twist
from std_msgs.msg import String, Float32, ColorRGBA, Bool, Int8, Int16
from driver.msg import Model, Models, Type, Types, Zone, Zones, ChangeUpGoal, ChangeUpGoals, ChangeUpField

black = ColorRGBA()
black.r = 0
black.g = 0
black.b = 0
black.a = 1

grey = ColorRGBA()
grey.r = 100
grey.g = 100
grey.b = 100
grey.a = 1

white = ColorRGBA()
white.r = 255
white.g = 255
white.b = 255
white.a = 1

red = ColorRGBA()
red.r = 255
red.g = 0
red.b = 0
red.a = 1

green = ColorRGBA()
green.r = 0
green.g = 255
green.b = 0
green.a = 1

blue = ColorRGBA()
blue.r = 0
blue.g = 0
blue.b = 255
blue.a = 1

ballRadius = Float32()
ballRadius.data = 0.08001
ballWidth = Float32()
ballWidth.data = 0

robotRadius = Float32()
robotRadius.data = 0.3
robotWidth = Float32()
robotWidth.data = 1

goalRadius = Float32()
goalRadius.data = 0.130048
goalWidth = Float32()
goalWidth.data = 0.054229

fieldRadius = Float32()
fieldRadius.data = 0
fieldWidth = Float32()
fieldWidth.data = 1

lft = Float32()
lft.data = -1.6335
mid = Float32()
mid.data = 0
rgt = Float32()
rgt.data = 1.6335

top = Float32()
top.data = 1.6335
dwn = Float32()
dwn.data = -1.6335

fieldX1 = Float32()
fieldX1.data = 0
fieldY1 = Float32()
fieldY1.data = 0
fieldX2 = Float32()
fieldX2.data = -1.82*2
fieldY2 = Float32()
fieldY2.data = 1.82*2

zip = Float32()
zip.data = 0


def main():
    # publisher objects
    main.types = Types()
    main.zones = Zones()
    main.models = Models()
    main.field = ChangeUpField()

    # the initial vars to just change later
    initialPose = Pose()
    initialModels = Models()

    itypes = [
        ['robot','circle',robotRadius,robotWidth],
        ['ball', 'circle',ballRadius,ballWidth],
        ['goal', 'circle',goalRadius,goalWidth],
        ['field', 'rect', zip, zip],
    ]

    for itype in itypes:
        type = Type()
        type.name = itype[0]
        type.shape = itype[1]
        type.radius = itype[2]
        type.width = itype[3]
        main.types.types.append(type)

    def findType(name):
        for obj in main.types.types:
            if(obj.name == name):
                return obj
        print("type not found!")

        #maybe useful?
    for itype in itypes:
        type = findType(itype[0])
        assert type.name == itype[0]
        assert type.shape == itype[1]
        assert type.radius == itype[2]
        assert type.width == itype[3]


    izones = [
        # name           #types     #x1      #y1      #x2   #y2    #radius
        # the first zone is a field
        ['field', 'field', grey, fieldX1, fieldY1, fieldX2, fieldY2, initialModels],
        ['lft_top_goal', 'goal', black, lft, top, zip, zip, initialModels],
        ['mid_top_goal', 'goal', black, mid, top, zip, zip, initialModels],
        ['rgt_top_goal', 'goal', black, rgt, top, zip, zip, initialModels],
        ['lft_mid_goal', 'goal', black, lft, mid, zip, zip, initialModels],
        ['mid_mid_goal', 'goal', black, mid, mid, zip, zip, initialModels],
        ['rgt_mid_goal', 'goal', black, rgt, mid, zip, zip, initialModels],
        ['lft_dwn_goal', 'goal', black, lft, dwn, zip, zip, initialModels],
        ['mid_dwn_goal', 'goal', black, mid, dwn, zip, zip, initialModels],
        ['rgt_dwn_goal', 'goal', black, rgt, dwn, zip, zip, initialModels],
    ]

    for izone in izones:
        zone = Zone()
        zone.name = izone[0]
        zone.type = izone[1]
        zone.color = izone[2]
        zone.x1 = izone[3]
        zone.y1 = izone[4]
        zone.x2 = izone[5]
        zone.y2 = izone[6]
        zone.models = izone[7]
        main.zones.zones.append(zone)

    def findZone(name):
        for obj in main.zones.zones:
            if(obj.name == name):
                return obj
        print("zone not found!")

    imodels=[
        # the fist model is the robot
        ['robot', white, 'field', 'robot', '', initialPose],
        ['ball',red,'field','red1', 'body',initialPose],
        ['ball',red,'field','red2', 'body',initialPose],
        ['ball',red,'field','red3', 'body',initialPose],
        ['ball',red,'mid_top_goal','red4', 'body',initialPose],
        ['ball',red,'mid_top_goal','red5', 'body',initialPose],
        ['ball',red,'mid_dwn_goal','red6', 'body',initialPose],
        ['ball',red,'lft_mid_goal','red7', 'body',initialPose],
        ['ball',red,'lft_top_goal','red8', 'body',initialPose],
        ['ball',red,'field','red9', 'body',initialPose],
        ['ball',red,'field','red10','body',initialPose],
        ['ball',red,'rgt_dwn_goal','red11','body',initialPose],
        ['ball',red,'rgt_mid_goal','red12','body',initialPose],
        ['ball',red,'rgt_top_goal','red13','body',initialPose],
        ['ball',red, 'lft_dwn_goal', 'red14', 'body', initialPose],
        ['ball', blue, 'field', 'blue1',  'body', initialPose],
        ['ball', blue, 'field', 'blue2',  'body', initialPose],
        ['ball', blue, 'field', 'blue3',  'body', initialPose],
        ['ball', blue, 'mid_top_goal', 'blue4',  'body', initialPose],
        ['ball', blue, 'mid_dwn_goal', 'blue5',  'body', initialPose],
        ['ball', blue, 'mid_dwn_goal', 'blue6',  'body', initialPose],
        ['ball', blue, 'lft_dwn_goal', 'blue7',  'body', initialPose],
        ['ball', blue, 'lft_top_goal', 'blue8',  'body', initialPose],
        ['ball', blue, 'rgt_dwn_goal', 'blue9',  'body', initialPose],
        ['ball', blue, 'rgt_mid_goal', 'blue10', 'body', initialPose],
        ['ball', blue, 'rgt_top_goal', 'blue11', 'body', initialPose],
        ['ball', blue, 'field', 'blue12', 'body', initialPose],
        ['ball', blue, 'field', 'blue13', 'body', initialPose],
        ['ball', blue, 'lft_mid_goal', 'blue14', 'body', initialPose],
    ]
    modelPoses=[
        # the fist model is the robot
        ['robot', 0.633686721058, -1.39194882216, 0.0997087770738],
        ['red1', 0.0, 0.2487, 0.0800099999967],
        ['red2', 0.2487, 0.0, 0.0800099999967],
        ['red3', 0.0, 0.81375, 0.0800099999967],
        ['red4', 0.00146976659807, 1.63156428191, 0.396581261397],
        ['red5', 0.0240113762385, 1.62193593341, 0.0800271181202],
        ['red6', -0.00656466288878, -1.63940329292, 0.236740707394],
        ['red7', -1.61358286062, 0.0102068251477, 0.0800105462861],
        ['red8', -1.6134335244, 1.62682662319, 0.0800099999873],
        ['red9', -1.4393, -1.4393, 0.0800099999967],
        ['red10', -1.4393, 1.4393, 0.0800099999967],
        ['red11', 1.63792541721, -1.64526359704, 0.236744859064],
        ['red12', 1.63553671269, -0.00699725340991, 0.236746927086],
        ['red13', 1.63952621539, 1.63388809791, 0.236745095785],
        ['red14', -1.63282006258, -1.63646320493, 0.0800067739113],
        ['blue1', 0.0, -0.2487, 0.0800099999967],
        ['blue2', -0.2487, 0.0, 0.0800099999967],
        ['blue3', 0.0, -0.81375, 0.0800099999967],
        ['blue4', -0.00632284870405, 1.6329191691, 0.236755383602],
        ['blue5', 0.00123421530103, -1.64078638107, 0.396571427742],
        ['blue6', 0.0256863687412, -1.63940159521, 0.0800099999946],
        ['blue7', -1.64398654753, -1.64429012611, 0.239447645944],
        ['blue8', -1.64458043606, 1.63516331632, 0.236747437855],
        ['blue9', 1.61944346481, -1.61882679362, 0.0800099999927],
        ['blue10', 1.61483014229, 0.0177284115879, 0.0800099723762],
        ['blue11', 1.60739369411, 1.63674208941, 0.0800099311779],
        ['blue12', 1.4393, -1.4393, 0.0800099999967],
        ['blue13', 1.4393, 1.4393, 0.0800099999967],
        ['blue14', -1.64152449588, -0.00590554941898, 0.236747871432],
    ]
    zoneModels=[
        # the first zone is a field
        ['field',        ['robot','red1','red2','red3','red9','red10','blue1','blue2','blue3','blue12','blue13']],
        ['lft_top_goal', ['red8','blue8']],
        ['mid_top_goal', ['red4','red5','blue4']],
        ['rgt_top_goal', ['red13','blue11']],
        ['lft_mid_goal', ['red7','blue14']],
        ['mid_mid_goal', []],
        ['rgt_mid_goal', ['red12','blue10']],
        ['lft_dwn_goal', ['red14','blue7']],
        ['mid_dwn_goal', ['red6','blue5','blue6']],
        ['rgt_dwn_goal', ['red11','blue9']],
    ]

    for imodel in imodels:
        model = Model()
        model.type = imodel[0]
        model.color = imodel[1]
        model.zone = imodel[2]
        model.name = imodel[3]
        model.link = imodel[4]
        model.pose = imodel[5]
        main.models.models.append(model)

    def findModel(name):
        for obj in main.models.models:
            if(obj.name == name):
                return obj
        print("model not found!")

    for modelPose in modelPoses:
        model = findModel(modelPose[0])
        pose = Pose()
        pose.position.x = modelPose[1]
        pose.position.y = modelPose[2]
        pose.position.z = modelPose[3]
        model.pose = pose

    for zoneModel in zoneModels:
        zone = findZone(zoneModel[0])
        for modelName in zoneModel[1]:
            zone.models.models.append(findModel(modelName))
        zone.models.models = sorted(zone.models.models, key=lambda model: model.pose.position.z)

    def findModelInZone(modelName,zoneName):
        zone = findZone(zoneName)
        for model in zone.models.models:
            if(model.name == modelName):
                return model
        print("model is not in zone!")

    changeUpGoals = [
        ['lft_top_goal', [], [] ],
        ['mid_top_goal', [], [] ],
        ['rgt_top_goal', [], [] ],
        ['lft_mid_goal', [], [] ],
        ['mid_mid_goal', [], [] ],
        ['rgt_mid_goal', [], [] ],
        ['lft_dwn_goal', [], [] ],
        ['mid_dwn_goal', [], [] ],
        ['rgt_dwn_goal', [], [] ],
    ]

    redPoints = Int16()
    redPoints.data = 0
    bluePoints = Int16()
    bluePoints.data = 0

    distanceFromRobot = Float32()
    distanceFromRobot.data = 0.0

    main.field.redPoints  = redPoints
    main.field.bluePoints = bluePoints

    for changeUpGoal in changeUpGoals:
        goal = ChangeUpGoal()
        goal.zoneName = changeUpGoal[0]
        goal.modelNames = changeUpGoal[1]
        goal.modelColors = changeUpGoal[2]
        goal.distanceFromRobot = distanceFromRobot
        main.field.goals.goals.append(goal)

    main.field.goalsColor = []
    main.field.fieldName = izones[0][0]
    main.field.modelNames = []
    main.field.modelColors = []
    main.field.distanceFromRobot = []

    def findGoalInField(name):
        for obj in main.field.goals.goals:
            if(obj.zoneName == name):
                return obj
        print("goal is not in field!")

    def findModelInGoalInField(modelName,goalName):
        goal = findGoalInField(goalName)
        for name in goal.modelNames:
            if(name == modelName):
                return findModel(name)
        print("model is not in a goal!")

#    print(main.field)
#    print(main.types)
#    print(main.zones)
#    print(main.models)

    print("logic models")
    rospy.init_node('logic_models')

    typesPub = rospy.Publisher('/field/types', Types,   queue_size=3)
    zonesPub = rospy.Publisher('/field/zones', Zones,   queue_size=3)
    modelPub = rospy.Publisher('/field/models', Models, queue_size=3)
    fieldPub = rospy.Publisher('/field/field', ChangeUpField, queue_size=3)

    main.gazeboBool = False
    main.lastGazeboTime = rospy.Time.now() - rospy.Duration(5)
    print(main.lastGazeboTime)

    def gazeboCallback(imodels):
        main.gazeboBool = True
        main.lastGazeboTime = rospy.Time.now()
        main.models = imodels

    def modelsCallback(imodels):
        if(main.gazeboBool):
            if( rospy.Time.now() - main.lastGazeboTime > rospy.Duration(10) ):
                main.gazeboBool = False

        if not main.gazeboBool:
            main.models = imodels

    rospy.Subscriber('/gazebo/get_field', Models, gazeboCallback)#(types, zones, models, typesPub, zonesPub, modelPub))
    rospy.Subscriber('/field/new_models', Models, modelsCallback)#(types, zones, models, typesPub, zonesPub, modelPub))

    def inCircle(x, y, center_x, center_y, radius):
        return (float(x) - float(center_x)) ** 2 + (float(y) - float(center_y)) ** 2 < float(radius) ** 2

    def nonZeroFloat(ia):
        a = ia
        if(a == 0):
            a = .000001
        return float(a)

    def distBetweenPoints(ia,ib):
        return math.sqrt((nonZeroFloat(ib[0]) - nonZeroFloat(ia[0]))**2 + (nonZeroFloat(ib[1]) - nonZeroFloat(ia[1])) ** 2)

    redInt = Int8()
    redInt.data = 1
    blueInt = Int8()
    blueInt.data = -1
    noneInt = Int8()
    noneInt.data = 0

    while not rospy.is_shutdown():
        try:

            # reset zone models
            for zone in main.zones.zones:
                for model in zone.models.models:
                    zone.models.models.pop()

            # reset goal modelNames and modelColors
            for goal in main.field.goals.goals:
                goal.modelNames = []
                goal.modelColors = []
                goal.distanceFromRobot = distanceFromRobot

            # reset field points
            redPoints.data = 0
            bluePoints.data = 0
            main.field.goalsColor = []
            main.field.modelNames = []
            main.field.modelColors = []
            main.field.distanceFromRobot = []

            # recalculate the zone and goal in models
            for model in main.models.models:
                model.zone = ''
                for zone in main.zones.zones:
                    zoneType = findType(zone.type)
                    if(zoneType.shape == 'circle'):
                        if(inCircle(float(model.pose.position.x),
                                    float(model.pose.position.y),
                                    float(zone.x1.data),
                                    float(zone.y1.data),
                                    float(zoneType.radius.data))):
                            model.zone = zone.name
                if(model.zone == ''):
                    model.zone = 'field'

                # add models to zone
                findZone(model.zone).models.models.append(model)

            # arrange zone models in order of height
            for zone in main.zones.zones:
                zone.models.models = sorted(zone.models.models, key=lambda model: model.pose.position.z)
                if(zone.name != 'field'):
                    # add models to goal (if the zone is not a field)
                    goal = findGoalInField(zone.name)

                    actualDistanceFromRobot = Float32()
                    actualDistanceFromRobot.data = distBetweenPoints(
                        (findZone(goal.zoneName).x1.data, findZone(goal.zoneName).y1.data),
                        (findModel(imodels[0][3]).pose.position.x, findModel(imodels[0][3]).pose.position.y)
                    )

#                    print(findModel(imodels[0][3]).pose)
#                    print(goal.zoneName,(findZone(goal.zoneName).x1.data, findZone(goal.zoneName).y1.data),
#                        (findModel(imodels[0][3]).pose.position.x, findModel(imodels[0][3]).pose.position.y))
#                    print(zone.name,actualDistanceFromRobot)

                    goal.distanceFromRobot = actualDistanceFromRobot

                    for model in zone.models.models:
                        if(model.zone == zone.name):
                            #if(len(goal.modelNames)>0):
                            goal.modelNames.append(model.name)

                            if(model.color == red):
                                redPoints.data += 1
                                goal.modelColors.append(redInt)
                            elif(model.color == blue):
                                bluePoints.data += 1
                                goal.modelColors.append(blueInt)
                elif(zone.name == 'field'):
                    for model in zone.models.models:
                        if (model.zone == zone.name):
                            # if(len(goal.modelNames)>0):
                            main.field.modelNames.append(model.name)

                            if (model.color == red):
                                main.field.modelColors.append(redInt)
                            elif (model.color == blue):
                                main.field.modelColors.append(blueInt)

                            actualDistanceFromRobot = Float32()
                            actualDistanceFromRobot.data = distBetweenPoints(
                                (model.pose.position.x, model.pose.position.y),
                                (findModel(imodels[0][3]).pose.position.x, findModel(imodels[0][3]).pose.position.y)
                            )

                            main.field.distanceFromRobot.append(actualDistanceFromRobot)

            fieldColors = [
                [blueInt,blueInt,redInt],
                [blueInt,noneInt,redInt],
                [blueInt, redInt,redInt],
            ]

            fieldGoals = [
                [main.field.goals.goals[0], main.field.goals.goals[1], main.field.goals.goals[2]],
                [main.field.goals.goals[3], main.field.goals.goals[4], main.field.goals.goals[5]],
                [main.field.goals.goals[6], main.field.goals.goals[7], main.field.goals.goals[8]],
            ]

            for x in range(len(fieldColors)):
                for y in range(len(fieldColors[0])):
                    goal = fieldGoals[x][y]
                    num = noneInt
#                    print(fieldGoals)
#                    print(len(goal.modelColors))
                    if(len(goal.modelColors)>0):
                        color = findGoalInField(goal.zoneName).modelColors[-1]
                        if(color == redInt):
                            num = redInt
                        elif(color == blueInt):
                            num = blueInt
#                        print(x,y,color)
                    fieldColors[x][y] = num

            goal_rows = [
                #horizontal
                [[0,0], [0,1], [0,2]],
                [[1,0], [1,1], [1,2]],
                [[2,0], [2,1], [2,2]],

                #vertical
                [[0,0], [1,0], [2,0]],
                [[0,1], [1,1], [2,1]],
                [[0,2], [1,2], [2,2]],

                #diagonal
                [[0,0], [1,1], [2,2]],
                [[2,0], [1,1], [0,2]],
            ]

#            print(fieldColors)
#            print(goal_rows)

            for i in range(0,len(goal_rows)):
                sum = fieldColors[goal_rows[i][0][0]][goal_rows[i][0][1]].data + \
                      fieldColors[goal_rows[i][1][0]][goal_rows[i][1][1]].data + \
                      fieldColors[goal_rows[i][2][0]][goal_rows[i][2][1]].data

                if(sum == 3):
                    redPoints.data += 6
                    main.field.goalsColor.append(redInt)
                elif(sum == -3):
                    bluePoints.data += 6
                    main.field.goalsColor.append(blueInt)
                else:
                    main.field.goalsColor.append(noneInt)

            main.field.redPoints = redPoints
            main.field.bluePoints = bluePoints

#            print(main.field)

            fieldPub.publish(main.field)
            typesPub.publish(main.types)
            zonesPub.publish(main.zones)
            modelPub.publish(main.models)

            time.sleep(.25)


        except rospy.ROSInterruptException:
            print("failed to display models")

if __name__ == '__main__':
    main()