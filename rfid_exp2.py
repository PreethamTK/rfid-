import numpy as np
import pandas as pd
from descartes import PolygonPatch
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
import numpy as  np
import bezier
import math
import matplotlib.cbook as cbook
from scipy.misc import imread
from shapely import geometry
from pyrtree import RTree,Rect


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import itertools

# def find_interesection_plot():



def distanceRssi(rssi,rand):

    return (pow(10,(-52-rssi)/10*rand))*100

def findantenna(polycol,antennaid,powerlevel):
    antennaindex=antennaid-1
    powerlevelindex=(powerlevel-10)/5
    poly22=polycol[antennaindex][powerlevelindex]
    ring_patch3 = PolygonPatch(poly22,color="blue")
    # ax.add_patch(ring_patch3)

    return poly22




def findantennacoordinates(antennaid):
    xcor=antenna_x_values[antennaid-1]
    ycor=antenna_y_values[antennaid-1]
    return (xcor,ycor)

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
distance={10: [30,55,69,81,90,81,69,55,30],15: [35,70,89,126,187,126,89,70,35], 20: [58,87,154,206,326,206,154,87,58], 25 : [64,256,340,412,587,412,340,256,64] ,30 : [210,480,547,760,1080,760,547,480,210] }
# ax = plot(x_a1,y_a1)

no_of_antenna = int(input("Enter the number of antennas"))
pointrtree=[]
nodes = []
polycol=[]
fullpolyset =[]
antenna_points=[]
# antenna_x_values=[44,44,44,2100,2100,2100]
# antenna_y_values=[212,562,912,212,562,912]
antenna_x_values=[400,800,1350,1900]
antenna_y_values=[870,50,870,50]
# direction_values=['r','l','r','l','l','l']
direction_values=['d','u','d','u']

for l in range(0,no_of_antenna):
    x_a1=antenna_x_values[l]
    y_a1=antenna_y_values[l]
    position = direction_values[l]
    antenna_points.append((x_a1,y_a1))


    # x_a1=int(input("Enter the position of antena (x coorinate)"))
    # y_a1=int(input("Enter the position of antena (y coorinate)"))
    # position = str(raw_input("Enter the direction in which the antena is facing u for up d for down l for left  r for right "))
    # antenna_points.append((x_a1,y_a1))
    # # y_a1=5
    # ax = plt(x_a1,y_a1)

    i=30
    xcor=[None]*9
    ycor=[None]*9
    j=0
    #print xcor
    curve =[None]*10
    p=0
    polycollection=[]
    for power in [10,15,20,25,30]:
        j=0
        pointList=[]
        pointList2=[]
        # k=0
        for angle in [0,30,45,60,90,120,135,150,180]:
            dist= distance[power][j]
            # if angle==60:
            #     angle=45
            # if angle==120:
            #     angle=135
            if position == 'l':
                angle=90-angle
            if position == 'r':
                angle = 90-angle

            cosx=math.cos(math.radians(angle))
            sinx=math.sin(math.radians(angle))
            xcor[j] = position_calculate_x(position,x_a1,cosx,dist)
            ycor[j] = position_calculate_y(position,y_a1,sinx,dist)
            #print "("+str(xcor[j])+","+str(ycor[j])+") at angle"+str(angle)
            p1 = geometry.Point(xcor[j],ycor[j])
            # if angle <90:
            pointList.append(p1)

            # ycor[j] = y_a1+(dist*sinx)
            j+=1
        # #print pointList

        templist = []
        pointat0=xcor[0],ycor[0]
        pointat90=xcor[4],ycor[4]
        pointat180=xcor[7],ycor[7]
        if position=='r' or position=='l':
            pointbottom = x_a1,ycor[3]

            pointtop = xcor[4],ycor[7]

            templist.append(pointbottom)

            # templist.append(pointat90)
            templist.append(pointtop)
        if position =='u' or position=='d':
            pointbottom=xcor[3],y_a1
            pointrequired = xcor[7],ycor[4]

            templist.append(pointbottom)

            # templist.append(pointat90)
            templist.append(pointrequired)


        nodesA_1_10_1 = np.array([[xcor[0],xcor[1],xcor[2],xcor[3],xcor[4]],[ycor[0],ycor[1],ycor[2],ycor[3],ycor[4]]])
        nodesA_1_10_2 = np.array([[xcor[4],xcor[5],xcor[6],xcor[7],xcor[8]],[ycor[4],ycor[5],ycor[6],ycor[7],ycor[8]]])
        nodes.append(nodesA_1_10_1)
        nodes.append(nodesA_1_10_2)
        #print "lenfth of plist:"
        #print len(pointList)
        del pointList[7]
        del pointList[5]
        del pointList[3]
        del pointList[1]


        poly = geometry.Polygon([[p.x, p.y] for p in pointList])
        polycollection.append(poly)
        fullpolyset.append(poly)
        pointrtree.append(templist)
        # #print(poly.wkt)



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
    polycol.append(polycollection)
curve1 = bezier.Curve(nodes[0], degree=3)
ax = curve1.plot(num_pts=256)
del nodes[0]
for n in nodes:

    curve1 = bezier.Curve(n, degree=3)
    curve1.plot(num_pts=256, ax=ax)



nodesA_1_10_1 = np.array([[xcor[0],xcor[1],xcor[2],xcor[3]],[ycor[0],ycor[1],ycor[2],ycor[3]]])
nodesA_1_10_2 = np.array([[xcor[3],xcor[4],xcor[5],xcor[6]],[ycor[3],ycor[4],ycor[5],ycor[6]]])
plt.margins(x=0)
plt.margins(y=0)
plt.xticks(np.arange(-50, 1800, step=50))
# plt.yticks(np.arange(10))
plt.yticks(np.arange(-50, 1800, step=50))



acomab=str(raw_input("enter the QUERY point"))
xco=float(acomab.split(',')[0])
yco=float(acomab.split(',')[1])
point1=Point(xco,yco)
query_point=point1
point=point1


point = point1

found_dist=[]
# print "polygonpointlist"
# print len(polygonpointlist)


rfid_readings=pd.read_csv("/home/preetham/Downloads/exp2-id_csv.csv")
antenna_id_list=rfid_readings["Antenna"]
rssi_list=rfid_readings["Avg_Rssi"]
power_list=rfid_readings["Power"]
tagid_list=rfid_readings["sno"]

dict6={}
repeating_id=[]
for sno in tagid_list:
    # for j in range(i+1,)
    print sno
    if (str(sno) in dict6):
        print "here"
        dict6[str(sno)]+=1
    else:
        # print "here"
        dict6[str(sno)]=1

# for key, value in dict6.iteritems():
#     if value > 1:
#         repeating_id.append(int(key))

# for x in repeating_id:














circleradiusdistance=[]
for rssi in rssi_list:
    radius=distanceRssi(rssi,3)
    circleradiusdistance.append(radius)


polygonpointlist=[]



total_polygons = []
for x in polycol:
    for y in x:
        total_polygons.append(y)
dict7={}
print "dcit 6"
print dict6
'''
for sno,aid in zip(tagid_list,antenna_id_list):

    list_power_poly=[]

    if int(dict6[str(sno)])>1:
        print "the repeating sno values "
        print sno
        for i in range(0,len(tagid_list)):
            if tagid_list[i]==sno:
                antennaid=antenna_id_list[i]
                powerlevel=power_list[i]
                powerlevelpoly=findantenna(polycol,antennaid,powerlevel)
                list_power_poly.append(powerlevelpoly)

        # for poly in list_power_poly:
        # if not(list_power_poly[0].intersects(list_power_poly[1])):
            # print "never intersect with id "+str(sno)
        intersection_area=list_power_poly[0].intersection(list_power_poly[1])
        if not(list_power_poly[0].intersects(list_power_poly[1])):
            print "never intersect with id "+str(sno)
            intersection_area=list_power_poly[0]
        if(len(list_power_poly)>2):

            for j in range(2,len(list_power_poly)):
                intersection_area=list_power_poly[j].intersection(intersection_area)
        total_polygons.append(intersection_area)
        dict7[sno]=str(len(total_polygons)-1)

'''
dict3={}
dict4={}
id=0
tag_list_power=[]




for x in total_polygons:
    print x

    dict3[str(x)]=0 #maintain the number of tags in the p level
    dict4[str(x)]=id #for th
    id+=1
    tag_list_power.append([])



for i in range(0,len(power_list)):

    circleradius=circleradiusdistance[i]

    #print "circle radius :"
    #print circleradius
    #print "point right now "
    #print samplepoint[i]o
    sno=tagid_list[i]
    if(str(sno) in dict7):
        indexvalue=int(dict7[sno])
        powerlevelpoly=total_polygons[indexvalue]
        polygonpointlist.append(total_polygons[indexvalue])
        #print "antenna id"
        # #print antenna_index[i]
        dict3[str(powerlevelpoly)]+=1
        getid=dict4[str(powerlevelpoly)]
        tag_list_power[getid].append(sno)
        continue

    antennaid=antenna_id_list[i]
    powerlevel=power_list[i]
    powerlevelpoly=findantenna(polycol,antennaid,powerlevel)
    polygonpointlist.append(powerlevelpoly)
    #print "antenna id"
    # #print antenna_index[i]
    dict3[str(powerlevelpoly)]+=1
    getid=dict4[str(powerlevelpoly)]
    tag_list_power[getid].append(sno)

    antenna_points=findantennacoordinates(antennaid)
    # break

    # uncertain_region=cal_centroid(antenna_points,circleradius,powerlevelpoly)
    # cent=uncertain_region.centroid
    # predi/cted_points.append(cent)
    # found_dist.append(cent.distance(point))
    # uncertain_region_list.append(uncertain_region)
k=5
for radius in range(1,12):
    total_tags=[]
    radi=radius*100
    circle = query_point.buffer(radi)
    ration_value=0
    total_tags_detected=0
    for poly in total_polygons:
        if circle.intersects(poly):
            # list_of_points=dict3[poly]
            no_of_tags=dict3[str(poly)]
            print "no. of tags detected"
            print no_of_tags
            # dict3[str(powerlevelpoly)]+=1

            total_tags_detected+=no_of_tags
            print "tags detected id"
            getid=dict4[str(poly)]
            list_of_points=tag_list_power[getid]
            total_tags.append(list_of_points)
            print list_of_points
            intersection_area=circle.intersection(poly).area
            poly_area=poly.area
            ra_value=(intersection_area/poly_area)*float(no_of_tags)
            ration_value+=ra_value
            print "ratio value for this curve"
            print ra_value
    print "ratio value for this iteration"
    print ration_value

    if ration_value>=k:
        print "breaking"
        print "total_tags_detected"
        print total_tags_detected
        print "tags detected are"
        arr=np.array(total_tags)
        arr.flatten()
        print arr
        break







plt.show()
