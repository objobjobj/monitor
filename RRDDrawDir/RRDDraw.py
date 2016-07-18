import rrdtool
import json

##
##                 -----                                  |----   cpu_precent      ----   [ {time_stamp : [cpu_precent_array]} ]
#  all_info struct|
#                  -----  Virutal Machine Mac Address ----|----   virtual_memory
#                 |
#                  -----    
##
##

static_basic_path = './RRDDrawDir/'
static_step = 4
static_counter_calculate_type = 'COUNTER'
static_gauge_calculate_type = 'GAUGE'
static_max_num = 100000

class RRDDraw(object):
    """docstring for rrdDraw"""

    def __init__(self, all_info):
        self.all_info = all_info
        self.decodeInfo()

    def createRRD(self, name, start_time, calculate_type):
        #print "create rrd"
        rrdtool.create(static_basic_path + str(name)+'.rrd',
            '--start', str(start_time),
            '--step', str(static_step),
            'DS:data:'+calculate_type+':'+str(static_step * 2)+':U:U',
            'RRA:AVERAGE:0.5:1:' + str(static_max_num)
            )

    def updateRRD(self, name, item):
        rrdtool.update(static_basic_path + str(name)+'.rrd', str(item))

    def draw(self, all_info):
        print "Do nothing"


    def decodeInfo(self):
    #print self.all_info.keys()
        for mac_key in self.all_info.keys():
            mac_address = mac_key
            #print self.all_info[mac_address].keys()
            for key in self.all_info[mac_address].keys():
                #print key
                if key == "cpu_percent":
                    # ensure the array not be empty
                    info_length = len(self.all_info[mac_address][key])
                    if info_length == 0:
                        return

                    # get the start and end time in the array
                    start_time = self.all_info[mac_address][key][0].keys()[0]
                    end_time = self.all_info[mac_address][key][info_length-1].keys()[0]

                    #set up rrdname
                    rrdname = mac_address + '_' + key

                    #create rrd file
                    self.createRRD(rrdname, str(start_time), static_gauge_calculate_type)

                    print start_time
                    #update rrd item by iteartor
                    #print self.all_info[mac_address][key]
                    #print len(self.all_info[mac_address][key])
                    for infos in self.all_info[mac_address][key]:
                        #print infos
                        time_stamp = infos.keys()[0]
                        array = str(infos[time_stamp])[1:len(infos[time_stamp])-1].replace(' ', '').split(',')
                        item = time_stamp + ':' + array[0]
                        print item
                        self.updateRRD(rrdname, item)
                     
                #if key == "virtual_memory":
                #    print self.all_info[mac_address][key]
