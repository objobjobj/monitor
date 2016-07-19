import rrdtool
import json
import re

##
##                 -----                                  |----   cpu_precent
#  all_info struct|
#                  -----  Virutal Machine Mac Address ----|----   virtual_memory    |---  net_io_sent
#                 |
#                  -----                                  |----   net_io     -------|---  net_io_recv
##
##

static_basic_path = './RRDDrawDir/'
static_step = 4
static_counter_calculate_type = 'COUNTER'
static_gauge_calculate_type = 'GAUGE'
static_max_num = 100000
static_pic_formate = '.png'

# for the data-set name must be short, use a dict to short the key words
static_short_key = {"cpu_percent" : "cpup", "virtual_memory" : "vmem",
    "net_io" : "net"}

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

    def createRRD_net_io(self, name, start_time, calculate_type):
        rrdtool.create(static_basic_path + str(name) + '.rrd',
            '--start', str(start_time),
            '--step', str(static_step),
            # _s is net_io_sent, _r is net_io_recv
            'DS:' + str(name) + '_s' + ':' + calculate_type + ':' + str(static_step * 2) + ':U:U',
            'DS:' + str(name) + '_r' + ':' + calculate_type + ':' + str(static_step * 2) + ':U:U',
            'RRA:AVERAGE:0.5:1:' + str(static_max_num)
            )

    def updateRRD(self, name, item):
        rrdtool.update(static_basic_path + str(name) + '.rrd', str(item))

    def graphRRD_cpu_precent(self, name, start_time, end_time):
        y1_name = str(name) + '_y1'

        rrdtool.graph(static_basic_path + str(name) + static_pic_formate,
            '--step', str(static_step),
            '--start', start_time,
            '--end', end_time,
            'DEF:' + y1_name + '=' + static_basic_path + str(name) + '.rrd' + ':' + str(name) + ':AVERAGE',
            'LINE3:' +y1_name + '#00FF00'
            )
        return

    def graphRRD_virtual_memory(self, name, start_time, end_time):
        y1_name = str(name) + '_y1'
        
        rrdtool.graph(static_basic_path + str(name) + static_pic_formate,
            '--step', str(static_step),
            '--start', start_time,
            '--end', end_time,
            'DEF:' + y1_name + '=' + static_basic_path + str(name) + '.rrd' + ':' + str(name) + ':AVERAGE',
            'AREA:' +y1_name + '#00FF00'
            )
        return

    def graphRRD_net_io(self, name, start_time, end_time):
        # _s is net_io_sent, _r is net_io_recv
        sent_name = str(name) + '_s'
        recv_name = str(name) + '_r'
        
        rrdtool.graph(static_basic_path + str(name) + static_pic_formate,
            '--step', str(static_step),
            '--start', start_time,
            '--end', end_time,
            'DEF:' + sent_name + '=' + static_basic_path + str(name) + '.rrd' + ':' + str(name) + '_s'  + ':AVERAGE',
            'DEF:' + recv_name + '=' + static_basic_path + str(name) + '.rrd' + ':' + str(name) + '_r'  + ':AVERAGE',
            'LINE1:' +sent_name + '#00FF00:net_sent',
            'LINE1:' +recv_name + '#FF0000:net_recv',
            )
        return

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
                #print rrdname

                # cpu_precent draw
                if key == "cpu_percent":
                    ###create rrd file
                    self.createRRD(rrdname, str(start_time), static_gauge_calculate_type)

                    #print start_time
                    #print end_time
                    #print self.all_info[mac_address][key]
                    #print len(self.all_info[mac_address][key])

                    ###update rrd item by iteartor
                    for infos in self.all_info[mac_address][key]:
                        #print infos
                        time_stamp = infos.keys()[0]
                        array = str(infos[time_stamp])[1:len(infos[time_stamp]) - 1].replace(' ', '').split(',')
                        item = time_stamp + ':' + array[0]
                        #print item
                        self.updateRRD(rrdname, item)
                    
                    ###graph the rrd picture
                    self.graphRRD_cpu_precent(rrdname, str(start_time), str(end_time))

                # memory graph draw
                if key == "virtual_memory":
                    ###create rrd file
                    self.createRRD(rrdname, str(start_time), static_gauge_calculate_type)

                    ###update rrd item
                    for infos in self.all_info[mac_address][key]:
                        time_stamp = infos.keys()[0]
                        main_info_group = re.match(r"^svmem(.*?)$", infos[time_stamp])
                        main_info = main_info_group.group(1)
                        if (main_info == ""):
                            continue

                        letter = re.compile(r'[a-zA-Z=]')
                        need_info = re.sub(letter, '',str(main_info))

                        array = str(need_info)[1:len(need_info) - 1].replace(r'[a-z]', '').split(',')
                        if len(array) != 10:
                            continue
                        item = time_stamp + ':' + array[2].strip()
                        #print item
                        self.updateRRD(rrdname, item)


                    ###graph the rrd picture
                    self.graphRRD_virtual_memory(rrdname, str(start_time), str(end_time))

                if key == "net_io":
                    ###create rrd file
                    self.createRRD_net_io(rrdname, str(start_time), static_counter_calculate_type)

                    ###update rrd item
                    for infos in self.all_info[mac_address][key]:
                        #print infos
                        time_stamp = infos.keys()[0]
                        info = infos[time_stamp]
                        item = time_stamp + ':' + info
                        #print item
                        self.updateRRD(rrdname, item)

                    ###graph the rrd picture
                    self.graphRRD_net_io(rrdname, str(start_time), str(end_time))

                    #print self.all_info[mac_address][key]
