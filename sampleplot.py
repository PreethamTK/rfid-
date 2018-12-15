import pandas as pd
import numpy as np
# import numpy as np
# import pandas as pd
from descartes import PolygonPatch
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
# import numpy as  np
import bezier
import math
import matplotlib.cbook as cbook
from scipy.misc import imread
from shapely import geometry
from pyrtree import RTree,Rect


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import itertools

# rfid_readings=pd.read_csv("/home/preetham/Downloads/rfid_tag.csv")
rfid_readings=pd.read_csv("/home/preetham/Downloads/exp1-id_csv.csv")
query_points=pd.read_csv("/home/preetham/codes/query_points.csv")
xq=query_points["X"]
yq=query_points["Y"]
data=rfid_readings
xcor=data["x"]
ycor=data["y"]
sno=data["sno"]
# distance_list=[]
# point_list=[]
dict={}
i=0
for x,y in zip(xcor,ycor):
    dict[str((x,y))]=sno[i]
    i+=1

count=1
output=[]

for x_query,y_query in zip(xq,yq):
    print "iteration number"
    print count
    count+=1

    distance_list=[]
    point_list=[]
    for x,y in zip(xcor,ycor):
        query_point=Point(float(x_query),float(y_query))
        current = Point(x,y)
        d=query_point.distance(current)
        distance_list.append(d)
        point_list.append(str((x,y)))
    a=distance_list
    b=point_list
    for i in range(0,len(a)):
        for j in range(1,len(a)):
            if a[j]< a[j-1]:
                a[j],a[j-1]=a[j-1],a[j]
                b[j],b[j-1]=b[j-1],b[j]
    print a[0:5]
    print b[0:5]
    final_tags=[]
    for name in b[0:5]:
        tagid=dict[name]
        final_tags.append(tagid)
    print final_tags
    output.append(str(final_tags))
    print "\n\n"

dict3={"X":xq,"Y":yq,"Nearest tags":output}
df=pd.DataFrame.from_dict(dict3)
df.to_csv("/home/preetham/codes/output_query_points.csv", sep='\t', encoding='utf-8')

# import matplotlib.pyplot as plt
data= rfid_readings
xcor=data["x"]
ycor=data["y"]
sno=data["sno"]

plt.plot(xcor, ycor, 'ro')

# plt.plot(xcord, ycord, 'ro',color="green")










i=0

for x,y in zip(xcor,ycor):
    plt.annotate(xy=[x,y], s=str(sno[i]))
    i+=1
plt.xticks(np.arange(0, 2800, step=200))
# plt.yticks(np.arange(10))
plt.yticks(np.arange(0, 2800, step=200))

plt.show()
