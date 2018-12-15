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
def findsubsets(S,m):
    return set(itertools.combinations(S, m))
# def findantenna():

def findantenna(polycol,antennaid,powerlevel):
    antennaindex=((antennaid+1)/2)-1
    powerlevelindex=(powerlevel-10)/5
    return polycol[antennaindex][powerlevelindex]



def distanceRssi(rssi,rand):

    return (pow(10,(-52-rssi)/10*rand))*100

##print(distanceRssi(-2,1))
def stage2 (list_of_circles,query_point,k):
    # circle=0
    count = 0
    probablity_list=[0]*len(list_of_circles)
    for radius in range(0,500):
        count=0
        i=radius*1

        circle = query_point.buffer(i)
        for l in range(len(list_of_circles)):
            poly=list_of_circles[l]
            if(circle.contains(poly)):
                probablity_list[l]=1
            elif (circle.intersects(poly)):
                area_intersected = circle.intersection(poly).area
                area_poly=poly.area
                probablity = area_intersected/area_poly
                probablity_list[l]=probablity
            else:
                probablity_list[l]=0
        # print probablity_list
        for values in probablity_list:
            if values == 1:
                count+=1

        if count >= k:
            break;
    return probablity_list



def candidate_selection():
    '''i/p:
    ck : k number of candidates
    threshold probablity
    o/p:
    output possible candidates
'''
def kbound_filtering():
    '''
    i/p rtree, qpoint, k
    o/p fk,numberofcandidates


    '''

def apriori(dic,threshold , k):
    A=[]
    selected_candidates=[]
    for key,values in dic.iteritems():
        A.append(key)
    for subset in findsubsets(A,k):
        prod=1
        for element in subset:
            # print element
            val=dic[element]
            prod*=val
        #print prod
        if prod > threshold:
            selected_candidates.append(subset)
    return selected_candidates




def cal_centroid(antenna_points,circleradius,powerlevelpoly):
    x_antenna=antenna_points[0]
    y_antenna=antenna_points[1]
    #print "antenna points"
    #print (x_antenna,y_antenna)
    point2=Point(x_antenna,y_antenna)
    circle = point2.buffer(circleradius)

    # #print fullpolyset[4]
    interornot=circle.intersection(powerlevelpoly)
    #print "interesection points"
    #print interornot
    centroid=interornot.centroid
    #print "centroid"
    #print centroid
    fig = plt.figure(1, figsize=(5,5), dpi=90)
    ax = fig.add_subplot(111)
    ring_patch = PolygonPatch(circle,color="yellow")
    ring_patch2 = PolygonPatch(powerlevelpoly,color="red")
    ax.add_patch(ring_patch)
    x22=[]
    y22=[]
    x22,y22=interornot.exterior.coords.xy
    x23=[]
    y23=[]
    pointList3=[]
    x23,y23=circle.exterior.coords.xy
    for a,c in zip(x22,y22):
        for b,d in zip(x23,y23):
            if((a,c)==(b,d)):
                #print "a,c values"
                #print (a,c)
                pointList3.append(Point(a,c))
    #print "length of pointList3"
    #print len(pointList3)
    poly22=interornot
    ring_patch3 = PolygonPatch(poly22,color="green")
    #print len(pointList3)
    length_pl3=len(pointList3)
    if (length_pl3>2):
        #print "wt brooo!!!!!!"
        #print "inside "
        poly22 = geometry.Polygon([[p.x, p.y] for p in pointList3])
        # ring_patch3 = PolygonPatch(poly22,color="green")
    ax.add_patch(ring_patch2)
    ax.add_patch(ring_patch3)
    return poly22

    #
    # #print x22
    # finalpoints=[]
    # # line = geometry.LineString(circle)
    # # point = geometry.Point(Point_X, Point_Y)
    # for i in range(0,len(x22)):
    #     temppoint=Point(x22[i],y22[i])
    #     if ((circle.within(temppoint))):
    #         finalpoints.append((x22[i],y22[i]))
    # #print "finalpoints::>>>>"
    # #print finalpoints



def findantennacoordinates(antennaid):
    if((antennaid==1)or (antennaid==2)):
        return (152.4,396.24)
    else:
        return (1066.8,182.88)

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
antenna_x_values=[152.4,1066.88]
antenna_y_values=[396.24,182.88]
# direction_values=['r','l','r','l','l','l']
direction_values=['r','l']

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




#print xcor
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
#
# datafile = cbook.get_sample_data('/home/preetham/codes/staff')
# img = imread(datafile)
#
# plt.imshow(img, zorder=0, extent=[0, 3500, 0, 9.0])
# samplepoint = []
samplepoint=[]
# numberofpoints=int(raw_input("enter the number of points"))
pointfile=open("/home/preetham/codes/samplepoint.txt","r")

for i in pointfile:
    acomab=str(i)
    xco=float(acomab.split(',')[0])
    yco=float(acomab.split(',')[1])
    p1234=Point(xco,yco)
    samplepoint.append(p1234)
antenna_index=[]
pointfile.close()
antennafile=open("/home/preetham/codes/antennafile.txt","r")

for i in antennafile:
    aid=int(i)
    antenna_index.append(aid)
antennafile.close()

# samplepoint=[Point(13.5,145),Point(500,817),Point(300,200),Point(565,340),Point(365,340),Point(500,217),Point(497,500),Point(386,296)]
acomab=str(raw_input("enter the QUERY point"))
xco=float(acomab.split(',')[0])
yco=float(acomab.split(',')[1])
point1=Point(xco,yco)
query_point=point1
point=point1

# point = Point(95,890)

# plt.plot(-5,750)
dict3={}
'''polygonpointlist=[]
dict = {}
#print "length"
#print len(fullpolyset)

print "polycol"
print len(polycol)
for x  in fullpolyset:
    # #print x
    dict[str(x)]=[]
# j=-1
antenna_detect_list=[]
indexj=-1
samplepoint2=[]
for sp in samplepoint:
    indexj+=1
    i=-1
    antenna_detect=0
    detectvalue=0
    for molly in polycol:
        some_value=0


        for poly in molly:
            i+=1
            if poly.intersects(sp):
                samplepoint2.append(sp)
                detectvalue=0
                some_value=-1
                #print str(i)+"th index of polygon"
                polygonpointlist.append(poly)
                #print "antenna detected"
                #print antenna_detect
                antenna_detect_list.append(antenna_detect)
                # #print str(sp.x) + "," + str(sp.y)
                point = str(sp.x) + "," + str(sp.y)+""+str(i)+"index"
                dict[str(poly)].append(point)
                break

        antenna_detect+=1
        if(some_value==-1):
            break
    if(detectvalue==0):

        print "not detected"+str(sp)
        # del samplepoint[indexj]
samplepoint=samplepoint2
#print "antennas detected"
#print len(antenna_detect_list)
distancelist=[]
point = point1
#print "poly"
#print len(polygonpointlist)
#print "samplepoint"
#print len(samplepoint)
indexi=0
#print "no of antennas"
#print len(antenna_points)
#print "no in antnna detected list"
#print len(antenna_detect_list)
#print "antenna index length"
#print len(antenna_index)
'''
'''for x in samplepoint:
    #print indexi
    #print "antena index blah"
    # #print antenna_index[indexi]
    # y_antenna=antenna_points[antenna_detect_list[indexi]][1]
    # x_antenna=antenna_points[ante/nna_index[indexi]][0]
    indexi+=1
    #print x
    point2=Point()
    dis=0
    dis=x.distance(point)
    distancelist.append(dis)
circleradiusdistance=[]
indexi=0
'''

#
# for x in samplepoint:
#     y_antenna=antenna_points[antenna_detect_list[indexi]][1]
#     x_antenna=antenna_points[antenna_detect_list[indexi]][0]
#     # #print x
#     indexi+=1
#     point2=Point(x_antenna,y_antenna)
#     #print point2
#     dis=0
#     dis=x.distance(point2)
#     circleradiusdistance.append(dis)

#print distancelist
#print polygonpointlist
point = point1

found_dist=[]
# print "polygonpointlist"
# print len(polygonpointlist)


rfid_readings=pd.read_csv("/home/preetham/Downloads/rfid_tag.csv")
antenna_id_list=rfid_readings["ANTENNA"]
rssi_list=rfid_readings["AVG RSSI"]
power_list=rfid_readings["POWER"]

circleradiusdistance=[]
for rssi in rssi_list:
    radius=distanceRssi(rssi,3)
    circleradiusdistance.append(radius)


predicted_points=[]
polygonpointlist=[]
id_dict={}
uncertain_region_list=[]
print "Distance recieved from rssi"
for x in circleradiusdistance:
    print x
print "\n \n \n"

for i in range(0,len(power_list)):

    circleradius=circleradiusdistance[i]
    #print "circle radius :"
    #print circleradius
    #print "point right now "
    #print samplepoint[i]
    antennaid=antenna_id_list[i]
    powerlevel=power_list[i]
    powerlevelpoly=findantenna(polycol,antennaid,powerlevel)
    polygonpointlist.append(powerlevelpoly)
    #print "antenna id"
    # #print antenna_index[i]
    antenna_points=findantennacoordinates(antennaid)

    uncertain_region=cal_centroid(antenna_points,circleradius,powerlevelpoly)
    cent=uncertain_region.centroid
    predicted_points.append(cent)
    found_dist.append(cent.distance(point))
    uncertain_region_list.append(uncertain_region)
    # break
# point = Point(1,750 )
'''
without r trees ;
'''
print "predicted points "
id_point=0
for points in predicted_points:
    string= str(points.x)+","+str(points.y)
    id_dict[string]=id_point
    id_point+=1
    print points.x , points.y
#print  "accurate distance :"
#print distancelist
#print "predicted distance"
#print found_dist
k=5
final_k_points=[]
final_k_points_predicted_distance=[]
final_k_points_actual_distance=[]
final_k_points_3=[]
samplepoint=predicted_points
distancelist=found_dist
for x in samplepoint:
    final_k_points_3.append(x)
for i in range(0,len(distancelist)):
    for j in range(1,len(distancelist)):
        if(distancelist[j]<distancelist[j-1]):
            distancelist[j],distancelist[j-1]=distancelist[j-1],distancelist[j]
            final_k_points_3[j],final_k_points_3[j-1]=final_k_points_3[j-1],final_k_points_3[j]
            # uncertain_region_list[j],uncertain_region_list[j-1]=uncertain_region_list[j-1],uncertain_region_list[j]
uncertain_region_list_pruned=[]
point=point1
#print "query point"
#print point.x,point.y
for j in range(0,500):
    i=j*10
    if len(final_k_points)>k:
        break


    #print "\n"
    circle = point.buffer(i)

    for pop in fullpolyset:

        if i ==0:
            if pop.contains(circle):
                for j in range(0,len(polygonpointlist)):


                    if ((polygonpointlist[j]==pop) and not(str(pop) in dict3)):
                        #print "point in power level "+str(j)
                        # #print samplepoint[j]
                        final_k_points.append(samplepoint[j])
                        final_k_points_actual.append(found_dist[j])
                        final_k_points_predicted_distance.append(found_dist[j])
                        uncertain_region_list_pruned.append(uncertain_region_list[j])

                    # #print "adding to dict "+str(pop)
                        # #print dict[str(pop)]
                dict3[str(pop)]=str(pop)

        else:

            if pop.intersects(circle):

                for j in range(0,len(polygonpointlist)):

                    if ((polygonpointlist[j]==pop )and (not(str(pop) in dict3))):

                        #print "point in power level "+str(pop)
                        # #print samplepoint[j]
                        # #print "adding to dict "+str(pop)

                        # dict3[str(pop)]=str(pop)
                        final_k_points.append(samplepoint[j])
                        final_k_points_predicted_distance.append(found_dist[j])
                        final_k_points_actual_distance.append(distancelist[j])
                        uncertain_region_list_pruned.append(uncertain_region_list[j])

                dict3[str(pop)]=str(pop)
#print "query point"
#print point.x,point.y
print "final length of short listed k' points"

print len(final_k_points)

print "final k' points with id "
for points in final_k_points:
    string= str(points.x)+","+str(points.y)
    idofpoint=id_dict[string]
    print idofpoint


print "\n \n \n "
print " k' points before an additional iteration"
# print final_k_points
# print final_k_points
for x in final_k_points:
    print x.x,x.y

final_k_points_predicted_distance.sort()
largest_distance=final_k_points_predicted_distance[5]


i=largest_distance
circle = point.buffer(i)

for pop in fullpolyset:

    if i ==0:
        if pop.contains(circle):
            for j in range(0,polygonpointlist):


                if ((polygonpointlist[j]==pop) and not(str(pop) in dict3)):
                    # #print "point in power level "+str(j)
                        # #print samplepoint[j]
                    final_k_points.append(samplepoint[j])
                    final_k_points_actual.append(found_dist[j])
                    final_k_points_predicted_distance.append(found_dist[j])
                    uncertain_region_list_pruned.append(uncertain_region_list[j])
                    # #print "adding to dict "+str(pop)
                        # #print dict[str(pop)]
            dict3[str(pop)]=str(pop)

    else:

        if pop.intersects(circle):

            for j in range(0,len(polygonpointlist)):

                if ((polygonpointlist[j]==pop )and (not(str(pop) in dict3))):

                    # #print "point in power level "+str(pop)
                        # #print samplepoint[j]
                        # #print "adding to dict "+str(pop)

                        # dict3[str(pop)]=str(pop)
                    final_k_points.append(samplepoint[j])
                    final_k_points_predicted_distance.append(found_dist[j])
                    final_k_points_actual_distance.append(distancelist[j])
                    uncertain_region_list_pruned.append(uncertain_region_list[j])


            dict3[str(pop)]=str(pop)




print "final final list of shrortlistede k points"
print len(final_k_points)
print "final k' points"
for x in final_k_points:
    print x.x,x.y


# print final_k_points
#print "total numnber of points"
#print len(samplepoint)

final_k_points_1=final_k_points
final_k_points_2=[]




for x in final_k_points:
    final_k_points_2.append(x)

                        # #print dict[str(pop)]
# #print "dict3"
# #print dict3
# #print final_k_points
# #print "final_k_points_actual"
# #print final_k_points_actual_distance
# #print "final_k_points_predicted_distance"
# #print final_k_points_predicted_distance

for i in range(0,len(final_k_points_actual_distance)):
    for j in range(1,len(final_k_points_actual_distance)):
        if(final_k_points_actual_distance[j]<final_k_points_actual_distance[j-1]):
            final_k_points_actual_distance[j],final_k_points_actual_distance[j-1]=final_k_points_actual_distance[j-1],final_k_points_actual_distance[j]
            final_k_points_1[j],final_k_points_1[j-1]=final_k_points_1[j-1],final_k_points_1[j]
for i in range(0,len(final_k_points_predicted_distance)):
    for j in range(1,len(final_k_points_predicted_distance)):
        if(final_k_points_predicted_distance[j]<final_k_points_predicted_distance[j-1]):
            final_k_points_predicted_distance[j],final_k_points_predicted_distance[j-1]=final_k_points_predicted_distance[j-1],final_k_points_predicted_distance[j]
            final_k_points_2[j],final_k_points_2[j-1]=final_k_points_2[j-1],final_k_points_2[j]


# #print final_k_points_1
# #print
# sorted_k_actual_distance,sorted_k_points1=zip(*sorted(zip(final_k_points_actual_distance, final_k_points)))
# sorted_k_predicted_distance,sorted_k_points2=zip(*sorted(zip(final_k_points_predicted_distance, final_k_points)))
#
# #print "sorted points"
# #print "final_k_points_actual"
# #print final_k_points_actual_distance
# #print "final_k_points_predicted_distance"
# #print final_k_points_predicted_distance
dict4={}

for p,d in zip(final_k_points_3[0:k],distancelist[0:k]):
    #print p.x ,p.y,d
    stt=str(p.x)+","+str(p.y)
    dict4[stt]=stt
print "predicted k points"
print dict4
#print "\n"
#print "\n"
# #print "actual points"
# for p,d in zip(final_k_points_1[0:k],final_k_points_actual_distance[0:k]):
#     #print p.x ,p.y,d

#print "predicted points"

count_accuracy=0
for p in final_k_points_2:
    print p.x ,p.y
    stt=str(p.x)+","+str(p.y)
    if stt in dict4:
        print stt+" matching with the k predicted.. belongs to the knn"
        count_accuracy+=1
#print "count"

#print count_accuracy
#print "Accuracy is"
accuracy=float(float(count_accuracy)/float(k))
print "accuracy"
print accuracy

print "Lets start second stage of pruning :)"
print "\n"
print "\n"

secondlevelpruning_list=stage2(uncertain_region_list_pruned,query_point,k)
print secondlevelpruning_list
# secondlevelpruning_list.sort()
# print "sorted second level"
# print secondlevelpruning_list
print "Lets start third stage of pruning :)"
print "\n"
print "\n"

dict5 = {}
print "length of final_k_points"
print len(final_k_points)
print "length of secondlevelpruning_list"
print len(secondlevelpruning_list)
for points,prob in zip(final_k_points,secondlevelpruning_list):
    string= str(points.x)+","+str(points.y)
    print string+ " , " + str(prob)
    idofpoint=id_dict[string]
    dict5[idofpoint]=prob
threshold=0.8
print "dict5"
print dict5
get_subset= apriori(dict5,threshold,k)
print "subsets for the given threshold is \n \n"
for x in get_subset:
    print x



print "\n"
print "\n"
print "\n"
    # #print sorted_k_points1.x
#print "but actual k points without the algorithm"
# #print dict4
# #print sorted_k_points2.x


#
# x_antenna=antenna_points[0][0]
# y_antenna=antenna_points[0][1]
# #print (x_antenna,y_antenna)
# point2=Point(x_antenna,y_antenna)
# circle = point2.buffer(123)
#
# #print fullpolyset[4]
# interornot=circle.intersection(fullpolyset[4])
# #print "interesection points"
# #print interornot
# centroid=interornot.centroid
# #print "centroid"
# #print centroid
# fig = plt.figure(1, figsize=(5,5), dpi=90)
# ax = fig.add_subplot(111)
# ring_patch = PolygonPatch(circle,color="yellow")
# ring_patch2 = PolygonPatch(fullpolyset[4],color="red")
# ax.add_patch(ring_patch)
# x22=[]
# y22=[]
# x22,y22=interornot.exterior.coords.xy
# x23=[]
# y23=[]
# pointList3=[]
# x23,y23=circle.exterior.coords.xy
# for a,c in zip(x22,y22):
#     for b,d in zip(x23,y23):
#         if((a,c)==(b,d)):
#             #print "a,c values"
#             #print (a,c)
#             pointList3.append(Point(a,c))
# #print "length of pointList3"
# #print len(pointList3)
# poly22 = geometry.Polygon([[p.x, p.y] for p in pointList3])
# ring_patch3 = PolygonPatch(poly22,color="green")
#
#
# #print x22
# finalpoints=[]
# # line = geometry.LineString(circle)
# # point = geometry.Point(Point_X, Point_Y)
# for i in range(0,len(x22)):
#     temppoint=Point(x22[i],y22[i])
#     if ((circle.within(temppoint))):
#         finalpoints.append((x22[i],y22[i]))
# #print "finalpoints::>>>>"
# #print finalpoints
#
#
#
# ax.add_patch(ring_patch2 )
# ax.add_patch(ring_patch3 )
#



'''
with r trees;
change all the things to rect
change the circle to rect
tree construction
querying
'''



#print "\n"
#print "\n"
#print "\n"
#print "\n"
for x123 in pointrtree:



    print x123

t = RTree()
i=0
# ax = fig.add_axes([0,0,1,1])

'''
insertion is done
'''
#print "tag 10 is :)"
#print pointrtree[0]
#print "aaa"
for rectangepoints in pointrtree:
    x1=rectangepoints[0][0]
    y1=rectangepoints[0][1]
    x2=rectangepoints[1][0]
    y2=rectangepoints[1][1]
    # #print x1
    # wi=x2-x1
    # he=y2-y1
    #
    # p = plt.Rectangle(
    #  (x1, y1), wi, he,angle=0 ,fill=False
    #
    #  )
    # ax.add_patch(p)


    st="tag"+str(i)
    i+=1
    #print st
    t.insert(st,Rect(x1,y1,x2,y2))



'''
querying
'''

point_res = t.query_point( (2,1025) )
# rect_res = t.query_rect( Rect(0,1020,4,1040) )

rectx1=0
recty1=1020
rectx2=4
recty2=1040

tempx1=-1000.0
tempy1=1030.0
tempx2=-972.5
tempy2= 1000.0
wi=rectx2-rectx1
he=recty2-recty1

p = plt.Rectangle(
 (rectx1, recty1), wi, he,angle=0 ,fill=False

 )
ax.add_patch(p)

# '''
# real_point_res = [r.leaf_obj() for r in t.query_rect( (2,4,2.5,4.5) ) if r.is_leaf()]
for x123 in range(0,10):
    rect_res = t.query_rect( Rect(rectx1,recty1,rectx2,recty2) )
    rectx1-=20
    recty1-=50
    rectx2+=20
    recty2+=50
    #print "iteration "+str(x123)
    #print "x1"+str(x1)
    #print "y1"+str(y1)

    # wi=rectx2-rectx1
    # he=recty2-recty1
    #
    # p = plt.Rectangle(
    # (rectx1, recty1), wi, he,angle=0 ,fill=False
    #
    # )
    # ax.add_patch(p)

    for qp in rect_res:
        print qp.leaf_obj()
# #print real_point_res









# #print polycollection[3].contains(polycollection[2])


plt.show()
