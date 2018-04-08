from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
import numpy as  np
import bezier
import math


def position_calculate_x(direction , x ,cosx , dist):
    d=0
    if(direction=="u"):
        d= x-(dist*cosx)
        # ycor[j] = y_a1+(dist*sinx)
    elif (direction=="d"):
        d = x + (dist*cosx)
    elif(direction == "l"):
        d = x - (dist*cosx)
    else:
        d = x + (dist*cosx)
    return d

def position_calculate_y(direction , x ,cosx , dist):
    d=0
    if(direction=="u"):

        d= x+(dist*cosx)
        # ycor[j] = y_a1+(dist*sinx)
    elif (direction=="d"):
        d = x - (dist*cosx)
    elif(direction == "l"):
        d = x - (dist*cosx)
    else:
        d = x + (dist*cosx)
    return d

# Get current size
distance={10: [30,55,69,90,69,55,30],15: [35,70,89,187,89,70,35], 20: [58,87,154,326,154,87,58], 25 : [64,256,340,587,340,256,64] ,30 : [210,480,547,1080,547,480,210] }
# ax = plot(x_a1,y_a1)
no_of_antenna = int(input("Enter the number of antennas"))
nodes = []
for l in range(0,no_of_antenna):


    x_a1=int(input("Enter the position of antena (x coorinate)"))
    y_a1=int(input("Enter the position of antena (y coorinate)"))
    position = str(raw_input("Enter the direction in which the antena is facing u for up d for down l for left  r for right "))

    # y_a1=5
    # ax = plt(x_a1,y_a1)

    i=30
    xcor=[None]*7
    ycor=[None]*7
    j=0
    print xcor
    curve =[None]*10
    p=0

    for power in [10,15,20,25,30]:
        j=0
        for angle in [0,30,60,90,120,150,180]:
            dist= distance[power][angle/i]
            if angle==60:
                angle=45
            if angle==120:
                angle=135
            if position == 'l':
                angle=90-angle
            if position == 'r':
                angle = 90-angle
            cosx=math.cos(math.radians(angle))
            sinx=math.sin(math.radians(angle))
            xcor[j] = position_calculate_x(position,x_a1,cosx,dist)
            ycor[j] = position_calculate_y(position,y_a1,sinx,dist)

            # ycor[j] = y_a1+(dist*sinx)
            j+=1
        nodesA_1_10_1 = np.array([[xcor[0],xcor[1],xcor[2],xcor[3]],[ycor[0],ycor[1],ycor[2],ycor[3]]])
        nodesA_1_10_2 = np.array([[xcor[3],xcor[4],xcor[5],xcor[6]],[ycor[3],ycor[4],ycor[5],ycor[6]]])
        nodes.append(nodesA_1_10_1)
        nodes.append(nodesA_1_10_2)


        # curve1 = bezier.Curve(nodesA_1_10_1, degree=3)
        # curve2 = bezier.Curve.from_nodes(nodesA_1_10_2)
        # if p==0:
        #     ax = curve1.plot(num_pts=256)
        #     #ax = ax.plot(num_pts=256)
        #     curve2.plot(num_pts=256, ax=ax)
        # else:
        #     curve1.plot(num_pts=256, ax=ax)
        #     curve2.plot(num_pts=256, ax=ax)
        # p+=1

curve1 = bezier.Curve(nodes[0], degree=3)
ax = curve1.plot(num_pts=256)
del nodes[0]
for n in nodes:

    curve1 = bezier.Curve(n, degree=3)
    curve1.plot(num_pts=256, ax=ax)




print xcor
    # xat0= x_a1-

nodesA_1_10_1 = np.array([[xcor[0],xcor[1],xcor[2],xcor[3]],[ycor[0],ycor[1],ycor[2],ycor[3]]])
nodesA_1_10_2 = np.array([[xcor[3],xcor[4],xcor[5],xcor[6]],[ycor[3],ycor[4],ycor[5],ycor[6]]])


# nodesA_1_10_1 = np.array([[6.6,7.0,6.3+0.69,6.3],[0.0,0.3,0.74,0.9]])
# nodesA_1_10_2 = np.array([[6.3,6.3-0.69,6.3-0.69,6.0],[0.9,0.7,0.3,0.0]])
# nodesA_1_10_3 = np.array([[6.0,6.3,6.6],[0.0,-0.1,0.0]])

# curve1 = bezier.Curve(nodesA_1_10_1, degree=3)
# curve2 = bezier.Curve.from_nodes(nodesA_1_10_2)
# # curve3 = bezier.Curve.from_nodes(nodesA_1_10_3)
#
# ax = curve1.plot(num_pts=256)
# #ax = ax.plot(num_pts=256)
# curve2.plot(num_pts=256, ax=ax)
# #curve3.plot(num_pts=256, ax=ax)
# j=0
# for angle in [0,30,60,90,120,150,180]:
#     dist= distance[25][angle/i]
#     if angle==60:
#         angle=45
#     if angle==120:
#         angle=135
#     cosx=math.cos(math.radians(angle))
#     sinx=math.sin(math.radians(angle))
#     xcor[j] = x_a1-(dist*cosx)
#     ycor[j] = y_a1+(dist*sinx)
#     j+=1
# nodesA_1_15_1 = np.array([[xcor[0],xcor[1],xcor[2],xcor[3]],[ycor[0],ycor[1],ycor[2],ycor[3]]])
# nodesA_1_15_2 = np.array([[xcor[3],xcor[4],xcor[5],xcor[6]],[ycor[3],ycor[4],ycor[5],ycor[6]]])
#
# curve3 = bezier.Curve(nodesA_1_15_1, degree=3)
# curve4 = bezier.Curve.from_nodes(nodesA_1_15_2)
# curve3.plot(num_pts=256,ax=ax)
# #ax = ax.plot(num_pts=256)
# curve4.plot(num_pts=256, ax=ax)




# ax.plot(x,y, marker='.',color='black')
# ax = curve1.plot(num_pts=256)




plt.margins(x=0)
plt.margins(y=0)
plt.xticks(np.arange(-50, 1800, step=50))
# plt.yticks(np.arange(10))
plt.yticks(np.arange(-50, 1800, step=50))

plt.show()
