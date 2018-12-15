import pandas as pd;

rfid_readings=pd.read_csv("/home/preetham/Downloads/exp2-id_csv.csv")
data_read={}
sno_list=rfid_readings["sno"]
power_list=rfid_readings["Power"]
antenna_list=rfid_readings["Antenna"]
print "sno lentgh"
print len(sno_list)
print "ant lentgh"
print len(antenna_list)
print "sno lentgh"
print len(sno_list)
print power_list

# for record in rfid_readings:
#     print record["sno"]
#     if(str(record["sno"]) in data_read):
#         data_read["sno"].append((record["antenna"]-1)*4+record["Power"])
#     else:
#         data_read[str(record["sno"])]=(record["antenna"]-1)*4+record["Power"]
i=0
for sno in sno_list:
    data_read[str(sno)]=[]


for sno,antenna in zip(sno_list,antenna_list):
    power=power_list[i]
    print "power right now" +str(power)
    print "antenna right now" +str(antenna)

    if str(sno) in data_read:
        antenna_value=(antenna-1)*4
        power_value=(power-10)/5
        value=((antenna-1)*5)+((power-10)/5)
        print value
        data_read[str(sno)].append(value)
    else:
        value=((antenna-1)*5)+((power-10)%5)

        data_read[str(sno)]=[value]
    i+=1
print data_read

for key,value in data_read.iteritems():
    print key+ " : " + str(value)
