#import commands
import psutil
import json
import re
# find a element is in an array or not
def _array_find(array, e):
	for item in array:
		if item == e:
			return True
	return False

def _is_end_with_d_or_daemon(str):
	end_d = re.match(r"^.*?d$", str)
	end_daemon = re.match(r"^.*?daemon$", str)
	if end_d != None or end_daemon != None:
		return True
	return False

class CollectProcessInfo:
	def _get_process_info(self):
		protect_process = {}
		pids = psutil.pids()
		res = []
		#print _array_find(pids, 11111)
		for pid in pids:
			p = psutil.Process(pid)

			# if ppid == 1 and ppid doesn't exit in pids, it is not a daemon
			ppid = p.ppid()
			if ppid != 1:
				#print str(p.name()) + '\t' + str(p.ppid()) + '\t' + str(p.terminal())
				if _array_find(pids, ppid) == True:# or ppid == 0:
					continue

			if p.terminal() != None:
				continue

			if not _is_end_with_d_or_daemon(p.name()):
				continue

			this_p = {}
			this_p["id"] = pid
			this_p["name"] = p.name()
			this_p["exe"] = p.exe()
			this_p["cmd_line"] = p.cmdline()
			this_p["memory_percent"] = p.memory_percent()
			protect_process[pid] = this_p
			#print str(p.name()) + '\t' + str(p.ppid()) + '\t' + str(p.terminal())
		protect_process = sorted(protect_process.iteritems(),  key=lambda d:protect_process[d[0]]["memory_percent"], reverse = True)
		cou = 0
		for i in protect_process:
			if cou > 10:
				break;
			res.append(i)
			cou += 1
		#print res
		return res
		#return ""
		#result_temp = commands.getoutput("ps -C \"$(xlsclients | cut -d' ' -f3 | paste - -s -d ',')\" --ppid 2 --pid 2 --deselect -o tty,uid,pid,ppid,comm | grep ^\?")
		#return result_temp

		#result = result_temp.split('\n')

		#print result_temp

		#res_process = []

		#for item in result:
		#  if len(item.split()) < 3 or str.isdigit(item.split()[2]) == False:
		#  	continue
		#  id = int(item.split()[2])
		#  proc = psutil.Process(pid = id)
		#  res_process.append(proc.as_dict(attrs=['pid', 'name', 'username']))

		#return json.dumps(res_process)

#c = CollectProcessInfo()
#c._get_process_info()