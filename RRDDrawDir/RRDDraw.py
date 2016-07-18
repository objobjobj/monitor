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
static_pic_formate = '.png'

static_short_key = {"cpu_percent" : "cp"}

class RRDDraw(object):
    """docstring for rrdDraw"""

    def __init__(self, all_info):
        self.all_info = all_info

    def createRRD(self, name, start_time, calculate_type):
        #print "create rrd"
        rrdtool.create(static_basic_path + str(name) + '.rrd',
            '--start', str(start_time),
            '--step', str(static_step),
            'DS:' + str(name) + ':' + calculate_type + ':' + str(static_step * 2) + ':U:U',
            'RRA:AVERAGE:0.5:1:' + str(static_max_num)
            )

    def updateRRD(self, name, item):
        rrdtool.update(static_basic_path + str(name) + '.rrd', str(item))

    def graphRRD(self, key, name, start_time, end_time):
        if key == "cpu_percent":
            rrdtool.graph(static_basic_path + str(name) + static_pic_formate,
                '--step', str(static_step),
                '--start', start_time,
                '--end', end_time,
                'DEF:my_cpu_precent=' + static_basic_path + str(name) + '.rrd' + ':' + str(name) + ':AVERAGE',
                'LINE2:my_cpu_precent#00FF00'
                )


    def draw(self):
    #print self.all_info.keys()
        for mac_key in self.all_info.keys():
            mac_address = mac_key
            #print self.all_info[mac_address].keys()
            for key in self.all_info[mac_address].keys():
                #print key

                # Get basic info we need 

                # ensure the array not be empty
                info_length = len(self.all_info[mac_address][key])
                if info_length == 0:
                    continue

                # get the start and end time in the array
                # we should decrese the static step to get the correct answer
                start_time = int(self.all_info[mac_address][key][0].keys()[0]) - static_step
                end_time = self.all_info[mac_address][key][info_length - 1].keys()[0]

                # ensure the key is we need
                if not static_short_key.has_key(key):
                    continue

                #set up rrdname
                rrdname = mac_address + '_' + static_short_key[key]
                print rrdname

                if key == "cpu_percent":
                    ###create rrd file
                    self.createRRD(rrdname, str(start_time), static_gauge_calculate_type)

                    #print start_time
                    #print end_time

                    ###update rrd item by iteartor
                    #print self.all_info[mac_address][key]
                    #print len(self.all_info[mac_address][key])
                    for infos in self.all_info[mac_address][key]:
                        #print infos
                        time_stamp = infos.keys()[0]
                        array = str(infos[time_stamp])[1:len(infos[time_stamp]) - 1].replace(' ', '').split(',')
                        item = time_stamp + ':' + array[0]
                        #print item
                        self.updateRRD(rrdname, item)
                    
                    ###graph the rrd picture
                    self.graphRRD(key, rrdname, str(start_time), str(end_time))


                #if key == "virtual_memory":
                #    print self.all_info[mac_address][key]
