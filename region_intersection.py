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

def findsubsets(S,m):
    return set(itertools.combinations(S, m))
# Get current size
def find_k_intersection(k):
    list_inter_4=[]
    l=0
    for subarray in index_intersection_arr:

        # for element in subarray:
        if(len(subarray)<k):
            list_inter_4.append([])
        if(len(subarray)>=k):
            arr_4=[]
            subset1=findsubsets(subarray,k)
            subs=[]
            for sub2 in subset1:
                little_subs=[]
                for x in sub2:
                    # little_subs


                    little_subs.append(total_polygons[x])
                subs.append(little_subs)
            for sub,zzz in zip(subs,subset1):
                b=True
                r=None
                if sub[0].intersects(sub[1]):
                    interesection_region=sub[0].intersection(sub[1])

                    for index in range(2,len(sub)):
                        if interesection_region.intersects(sub[index]):
                            interesection_region=interesection_region.intersection(sub[index])
                            r=interesection_region
                        else:
                            print "breaking because of false value of iteration =  "+str(l)
                            print zzz
                            b=False
                            break
                else:
                    print "breaking because of false value of iteration =  "+str(l)
                    print zzz
                    b=False

                    # break

                if b :
                    # if r
                    # if r.geom_type=="Polygon":
                    #     ring_patch3 = PolygonPatch(r,color="green")
                    #     #ax.add_patch(ring_patch3)
                    #     # print "Jeisthen"
                    # else:
                    #     break
                        # print "Jeichoooo"
                    # ring_patch3 = PolygonPatch(r,color="green")
                    # #ax.add_patch(ring_patch3)
                    # print zzz
                    temp_dict={}
                    b2=True
                    b3=False
                    for z in zzz:
                        if z==l:
                            b3=True
                            break

                    for z in zzz:

                        if str(z/5) in temp_dict:
                            b2=False
                            break
                        else:
                            temp_dict[str(z/5)]=1
                    if b2 and b3:
                        arr_4.append(zzz)
                        # print zzz
                    # print "main set"
                    # print subset1
                # else :
                    # print "empty"

            list_inter_4.append(arr_4)
        l+=1
    return list_inter_4


def distanceRssi(rssi,rand):

    return (pow(10,(-52-rssi)/10*rand))*100

def findantenna(polycol,antennaid,powerlevel):
    antennaindex=antennaid-1
    powerlevelindex=(powerlevel-10)/5
    poly22=polycol[antennaindex][powerlevelindex]
    ring_patch3 = PolygonPatch(poly22,color="blue")
    # #ax.add_patch(ring_patch3)

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
# antenna_x_values=[400,800,1350,1900]
# antenna_y_values=[870,50,870,50]
# direction_values=['r','l','r','l','l','l']
# direction_values=['d','u','d','u']

antenna_x_values=[350,350,1550,1550]
antenna_y_values=[250,600,250,600]
# direction_values=['r','l','r','l','l','l']
direction_values=['r','r','l','l']

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

total_polygons = []
for x in polycol:
    for y in x:
        total_polygons.append(y)
poly22=total_polygons[4].intersection(total_polygons[8])
ring_patch3 = PolygonPatch(poly22,color="blue")
#ax.add_patch(ring_patch3)

polycol_copy=[]
for x in polycol:
    polycol_copy.append(x)

new_total_polygons=[]
for i in range(0,len(total_polygons)):
    if i%5==0:
        new_total_polygons.append(total_polygons[i])
        continue
    else:
        previous_polygon=total_polygons[i-1]
        current_polygon=total_polygons[i]
        current_polygon=current_polygon.difference(previous_polygon)
        new_total_polygons.append(current_polygon)

poly22=new_total_polygons[3]
# poly22=total_polygons[4].intersection(total_polygons[8])
ring_patch3 = PolygonPatch(poly22,color="orange")
#ax.add_patch(ring_patch3)

total_polygons=new_total_polygons



save_dict={}

# for plot1 in polycol_copy[0]:
#     for plot2 in polycol_copy[1]:
#         for plot3 in polycol_copy[2]:
#             for plot4 in polycol_copy[3]:
#                 temp_arr=[plot1,plot2,plot3,plot4]
#                 for i in range(1,5):
#                     r=5-i
#                     subset=findsubsets(temp_arr,r)
#                     for sub_array in subset:
#                         if sub_array[0].intersects(sub_array[1]):
#                             interesection_region= sub_array[0].intersection_area
#                         else:
#                             continue
#                         for j in range(0,r):
#                             interesection_region
#
# for plot1 in polycol_copy[0]:
main_intersection_arr=[]
index_intersection_arr=[]
# l=0
for i in range(0,len(total_polygons)):
    arr=[]

    arr2=[i]
    for j in range(0,len(total_polygons)):
        if i==j:
            continue
        if ((i/5)==(j/5)):
            continue
        poly1=total_polygons[i]
        poly2=total_polygons[j]
        if(poly1.intersects(poly2)):
            inter=poly1.intersection(poly2)
            arr.append(inter)
            save_dict[str(inter)]=[i,j]
            arr2.append(j)
    main_intersection_arr.append(arr)
    index_intersection_arr.append(arr2)

print "each levels intersection"
list_inter_4=[]
for subarray in index_intersection_arr:
    print subarray

l=0

for subarray in index_intersection_arr:

    # for element in subarray:
    if(len(subarray)<2):
        list_inter_4.append([])
    if(len(subarray)>=2):
        arr_4=[]
        subset1=findsubsets(subarray,2)
        print "iteration "+str(l)
        print subset1

        subs=[]
        for sub2 in subset1:
            little_subs=[]
            for x in sub2:
                # little_subs


                little_subs.append(total_polygons[x])
            subs.append(little_subs)
        print "checking lenght"
        print len(subs)
        print len(subset1)
        print "\n"
        for sub,zzz in zip(subs,subset1):
            b=True
            r=None
            if sub[0].intersects(sub[1]):
                interesection_region=sub[0].intersection(sub[1])
                for index in range(2,len(sub)):
                    if interesection_region.intersects(sub[index]):
                        interesection_region=interesection_region.intersection(sub[index])
                        r=interesection_region
                    else:
                        b=False
                        break
            else:
                b=False

                break

            if b :
                # if r
                # if r.geom_type=="Polygon":
                #     ring_patch3 = PolygonPatch(r,color="green")
                #     #ax.add_patch(ring_patch3)
                #     # print "Jeisthen"
                # else:
                #     break
                    # print "Jeichoooo"
                # ring_patch3 = PolygonPatch(r,color="green")
                # #ax.add_patch(ring_patch3)
                # print zzz
                temp_dict={}
                b2=True
                b3=False
                for z in zzz:
                    if z==l:
                        b3=True
                        break

                for z in zzz:

                    if str(z/5) in temp_dict:
                        b2=False
                        break
                    else:
                        temp_dict[str(z/5)]=1
                if b2 and b3:
                    arr_4.append(zzz)
                    # print zzz
                # print "main set"
                # print subset1
            # else :
                # print "empty"

        list_inter_4.append(arr_4)
    l+=1

print "number of 4"
for x in list_inter_4:
    print x



list4=find_k_intersection(4)
list3=find_k_intersection(3)
list2=find_k_intersection(2)
list4=find_k_intersection(4)
print "number of 4"
for x in list4:
    print x
print "\n\n\n\n"

print "number of 3"
for x in list3:
    print x
print "\n\n\n\n"

print "number of 2"
for x in list2:
    print x
print "\n\n\n\n"

main_dict={}
inter_list4=[]

for subs in list4:
    # print sub
    if len(subs)==0:
        inter_list4.append([])
        continue
    else:
        for sub in subs:
            print sub
            intersection_ar=total_polygons[sub[0]].intersection(total_polygons[sub[1]])
            intersection_ar=intersection_ar.intersection(total_polygons[sub[2]])
            intersection_ar=intersection_ar.intersection(total_polygons[sub[3]])
            print type(sub)
            sortedlist=[sub[0],sub[1],sub[2],sub[3]]
            sortedlist.sort()
            inter_list4.append([intersection_ar])

            # sub.sort()
            main_dict[str(sortedlist)]=intersection_ar
            ring_patch3 = PolygonPatch(intersection_ar,color="blue")
            # #ax.add_patch(ring_patch3)
print "list4"
print list4
print "list 3 lentgh"
print len(list3)
print list3
print"\n\n"
m=0
inter_list3=[]
for subs in list3:
    if len(subs)==0:
        m+=1
        inter_list3.append([])
        continue
    else:
        listfortemp=[]
        for sub in subs:
            print "m "+str(m)
            if m >19:
                break
            if len(list4[m])==0:


                intersection_ar=total_polygons[sub[0]].intersection(total_polygons[sub[1]])
                intersection_ar=intersection_ar.intersection(total_polygons[sub[2]])
                sortedlist=[sub[0],sub[1],sub[2]]
                sortedlist.sort()
                listfortemp.append(intersection_ar)
                main_dict[str(sortedlist)]=intersection_ar
                ring_patch3 = PolygonPatch(intersection_ar,color="blue")
                # #ax.add_patch(ring_patch3)
            else:

                temp_list=[sub[0],sub[1],sub[2]]
                print "temp list"
                print temp_list
                set1=set([sub[0],sub[1],sub[2]])
                set2=set([4,9,14,19])
                print "set1 set 2 are"
                print set1
                print set2
                print "\n\n\n"
                if set1.intersection(set2)==set1:
                    print "set do intersect"
                    intersection_ar=total_polygons[sub[0]].intersection(total_polygons[sub[1]])
                    intersection_ar=intersection_ar.intersection(total_polygons[sub[2]])
                    intersection_ar=intersection_ar.difference(inter_list4[m][0])
                    listfortemp.append(intersection_ar)
                    temp_list.sort()
                    main_dict[str(temp_list)]=intersection_ar

                    ring_patch3 = PolygonPatch(intersection_ar,color="green")
                    #ax.add_patch(ring_patch3)

                else:
                    intersection_ar=total_polygons[sub[0]].intersection(total_polygons[sub[1]])
                    intersection_ar=intersection_ar.intersection(total_polygons[sub[2]])
                    sortedlist=[sub[0],sub[1],sub[2]]
                    sortedlist.sort()
                    listfortemp.append(intersection_ar)
                    main_dict[str(sortedlist)]=intersection_ar
                    ring_patch3 = PolygonPatch(intersection_ar,color="red")
                    #ax.add_patch(ring_patch3)

        m+=1
        inter_list3.append(listfortemp)

# print main_dict

                # temp_list=[sub[]]
print "len of list3"
print len(list3)
print "inter list 3"
for x in inter_list3:
    print len(x)
print "\n\n\nlist 3"
for x in list3:
    print len(x)
m=0
inter_list2=[]
for subs in list2:
    if len(subs)==0:
        m+=1
        inter_list2.append([])
        continue
    else:
        listfortemp=[]
        for sub in subs:

            if len(list3[m])==0:

                intersection_ar=total_polygons[sub[0]].intersection(total_polygons[sub[1]])
                # intersection_ar=intersection_ar.intersection(total_polygons[sub[2]])
                sortedlist=[sub[0],sub[1]]
                sortedlist.sort()
                listfortemp.append(intersection_ar)
                main_dict[str(sortedlist)]=intersection_ar
                ring_patch3 = PolygonPatch(intersection_ar,color="blue")
                # #ax.add_patch(ring_patch3)
            else:
                temp_list=[sub[0],sub[1]]
                intersection_ar=total_polygons[sub[0]].intersection(total_polygons[sub[1]])
                changes=False
                for t in range(0,len(list3[m])):
                    changes=True
                    set1=set([sub[0],sub[1]])

                    set2=set([list3[m][t][0],list3[m][t][1],list3[m][t][2]])
                    print "set 1 and set 2 in list 2 is "
                    print set1
                    print set2
                    if set1.intersection(set2)==set1:
                        # intersection_ar=total_polygons[sub[0]].intersection(total_polygons[sub[1]])
                        # intersection_ar=intersection_ar.intersection(total_polygons[sub[2]])
                        intersection_ar=intersection_ar.difference(inter_list3[m][t])
                listfortemp.append(intersection_ar)
                temp_list.sort()
                main_dict[str(temp_list)]=intersection_ar

                ring_patch3 = PolygonPatch(intersection_ar,color="blue")
                # #ax.add_patch(ring_patch3)

                    # else:
                    #     intersection_ar=total_polygons[sub[0]].intersection(total_polygons[sub[1]])
                    #     intersection_ar=intersection_ar.intersection(total_polygons[sub[2]])
                    #     sortedlist=[sub[0],sub[1],sub[2]]
                    #     sortedlist.sort()
                    #     listfortemp.append(intersection_ar)
                    #     main_dict[str(sortedlist)]=intersection_ar
                    #     ring_patch3 = PolygonPatch(intersection_ar,color="blue")
                    #     #ax.add_patch(ring_patch3)
        inter_list2.append(listfortemp)
        m+=1


print "len of list2"
print len(list2)
print "inter list 2"
for x in inter_list2:
    print len(x)
print "\n\n\nlist 2"
for x in list2:
    print len(x)


inter_list1=[]
p=0
# for subs in total_polygons:
for p in range(len(inter_list2)):
    if len(inter_list2[p])==0:
        inter_list1.append(total_polygons[p])
        main_dict[str([p])]=total_polygons[p]

        continue
    else:
        print p
        area=total_polygons[p]
        tempi=0
        for x in inter_list2[p]:
            print "topology"+str(tempi)
            print "value "+str(list2[p][tempi])
            tempi+=1
            if tempi==3 and p==14:
                break

            # ring_patch3 = PolygonPatch(x,color="orange")
            ax.add_patch(ring_patch3)

            area=area.difference(x)
        inter_list1.append(area)
        main_dict[str([p])]=area
interlist1=[]
for p in range(len(inter_list3)):
    if len(inter_list3[p])==0:
        interlist1.append(inter_list1[p])
        main_dict[str([p])]=inter_list1[p]

        continue
    else:
        print "p value"
        print p
        area=inter_list1[p]
        tempi=0
        for x in inter_list3[p]:
            print "topology"+str(tempi)
            print "value "+str(list3[p][tempi])
            tempi+=1
            # if tempi==3 and p==14:
            #     break

            # ring_patch3 = PolygonPatch(x,color="orange")
            ax.add_patch(ring_patch3)

            area=area.difference(x)
        interlist1.append(area)
        main_dict[str([p])]=area

for p in range(len(inter_list4)):
    if len(inter_list4[p])==0:
        interlist1.append(inter_list1[p])
        main_dict[str([p])]=interlist1[p]

        continue
    else:
        print p
        area=interlist1[p]
        tempi=0
        for x in inter_list4[p]:
            print "topology"+str(tempi)
            print "value "+str(list4[p][tempi])
            tempi+=1
            # if tempi==3 and p==14:
            #     break

            # ring_patch3 = PolygonPatch(x,color="orange")
            ax.add_patch(ring_patch3)

            area=area.difference(x)
        interlist1.append(area)
        main_dict[str([p])]=area




polygon_set=[]

for key,value in main_dict.iteritems():
    print key
    polygon_set.append(value)


print "checking"
print main_dict[str([9])]
ring_patch3 = PolygonPatch(main_dict[str([9,17])],color="black")
ax.add_patch(ring_patch3)
print main_dict


import pandas as pd;

rfid_readings=pd.read_csv("/home/preetham/Downloads/exp2-id_csv.csv")
xcor=rfid_readings["x"]
ycor=rfid_readings["y"]
sno=rfid_readings["sno"]

i=0
plt.plot(xcor, ycor, 'ro')
for x,y in zip(xcor,ycor):
    plt.annotate(xy=[x,y], s=str(sno[i]))
    i+=1


# rfid_readings=pd.read_csv("/home/preetham/Downloads/exp2-id_csv.csv")
# data_read={}
# sno_list=rfid_readings["sno"]
# power_list=rfid_readings["Power"]
# antenna_list=rfid_readings["Antenna"]
# print "sno lentgh"
# print len(sno_list)
# print "ant lentgh"
# print len(antenna_list)
# print "sno lentgh"
# print len(sno_list)
# print power_list
#
# # for record in rfid_readings:
# #     print record["sno"]
# #     if(str(record["sno"]) in data_read):
# #         data_read["sno"].append((record["antenna"]-1)*4+record["Power"])
# #     else:
# #         data_read[str(record["sno"])]=(record["antenna"]-1)*4+record["Power"]
# i=0
# for sno in sno_list:
#     data_read[str(sno)]=[]
#
#
# for sno,antenna in zip(sno_list,antenna_list):
#     power=power_list[i]
#     print "power right now" +str(power)
#     print "antenna right now" +str(antenna)
#
#     if str(sno) in data_read:
#         antenna_value=(antenna-1)*4
#         power_value=(power-10)/5
#         value=((antenna-1)*5)+((power-10)/5)
#         print value
#         data_read[str(sno)].append(value)
#     else:
#         value=((antenna-1)*5)+((power-10)%5)
#
#         data_read[str(sno)]=[value]
#     i+=1
# print data_read
# keep_dict={}
# tag_name_dict={}
# key,value in data_read.iteritems():
#     print key+ " : " + str(value)
#     polygon_name=main_dict[str(value)]
#     if str(polygon_name) in keep_dict:
#         keep_dict[str(polygon_name)]+=1
#         tag_name_dict[str(polygon_name)].append(key)
#     else:
#         keep_dict[str(polygon_name)]=1
#         tag_name_dict[str(polygon_name)]=[key]
#
#
#
# k=5
# for radius in range(1,12):
#     total_tags=[]
#     radi=radius*100
#     circle = query_point.buffer(radi)
#     ration_value=0
#     total_tags_detected=0
#     total_polygons=polygon_set
#     dict3=keep_dict
#
#     for poly in total_polygons:
#         if circle.intersects(poly):
#             # list_of_points=dict3[poly]
#             no_of_tags=dict3[str(poly)]
#             print "no. of tags detected"
#             print no_of_tags
#             # dict3[str(powerlevelpoly)]+=1
#
#             total_tags_detected+=no_of_tags
#             print "tags detected id"
#             getid=tag_name_dict[str(poly)]
#             list_of_points=getid
#             total_tags.append(list_of_points)
#             print list_of_points
#             intersection_area=circle.intersection(poly).area
#             poly_area=poly.area
#             ra_value=(intersection_area/poly_area)*float(no_of_tags)
#             ration_value+=ra_value
#             print "ratio value for this curve"
#             print ra_value
#     print "ratio value for this iteration"
#     print ration_value
#
#     if ration_value>=k:
#         print "breaking"
#         print "total_tags_detected"
#         print total_tags_detected
#         print "tags detected are"
#         arr=np.array(total_tags)
#         arr.flatten()
#         print arr
#         break
#
#




plt.show()
