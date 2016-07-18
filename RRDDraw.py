import rrdtool
import json

class RRDDraw(object):
	"""docstring for rrdDraw"""

	def draw(all_info):
		self.all_info = all_info
		#print "Do not thing"
		print self.all_info

    def decodeInfo(self):
        #print self.all_info.keys()
        for mac_key in self.all_info.keys():
            mac_address = mac_key
            #print self.all_info[mac_address].keys()
            for key in self.all_info[mac_address].keys():
                print key
                if key == "cpu_percent":
                    print self.all_info[mac_address][key]
                if key == "virtual_memory":
                    print self.all_info[mac_address][key]
