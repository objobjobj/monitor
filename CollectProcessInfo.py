import commands
import psutil
import json

class CollectProcessInfo:
	def _get_process_info(self):
		result_temp = commands.getoutput("ps -C \"$(xlsclients | cut -d' ' -f3 | paste - -s -d ',')\" --ppid 2 --pid 2 --deselect -o tty,uid,pid,ppid,comm | grep ^\?")
		return result_temp

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

