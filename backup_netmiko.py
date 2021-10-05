import logging
from netmiko import ConnectHandler
from netmiko import SSHDetect
import datetime 
import time
import sys
import yaml
import pathlib
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()
#from netmiko.ssh_exception import NetMikoTimeoutException
#from netmiko.ssh_exception import AuthenticationException
#from netmiko.ssh_exception import SSHException
class backup_of_multiple_device():
	def __init__(self):
		current_dir = pathlib.Path(__file__).parent
		current_dir = str(current_dir)
		Variable=yaml.safe_load(open(current_dir+'/device_list.yaml'))
		self.IP_ADDRESS = (Variable['IP_ADDRESS'])
		self.username = (Variable['username'])
		self.password = (Variable['password'])
		self.send_commands = (Variable['send_commands'])
		self.device_type = (Variable['device_type'])
                self.backup_path = (Variable['backup_path'])
	def Connect(self):
		device_list=[]
		connection =''
		for i in range(0,len(self.IP_ADDRESS)):
			connection="connection_{}".format(i)
			connection= {
			   "device_type": self.device_type,
			   "host": self.IP_ADDRESS[i],
			   "username":self.username,
			   "password":self.password,
			     }
			device_list.append(connection)
		return device_list

       	def Backing_up_configuration(self,client,net_connect):
		#logger.info("Backing_up_configuration for device %s", self.IP_ADDRESS)
		TNOW=datetime.datetime.now().replace(microsecond=0)
		TNOW=str(TNOW).replace(" ","_")
		logger.info("Intiating backup_" +str(client['host'])+"_"+str(TNOW))
		k=0
		listing=[]
		while k < (len(self.send_commands)):
			listing.append(self.send_commands[k])
			k=k+1

                logger.info("config back up done for the device %s ",str(client['host']))
                
                SAVE_FILE=open("{}/backing_up_config".format(self.backup_path)+"_"+str(client['host']),"w")
                for i in range(len(listing)):
		    output = net_connect.send_command(listing[i])
		    SAVE_FILE.write(output)
                    SAVE_FILE.write("\n\n")
		SAVE_FILE.close()
                
	

        def config_from_file(self,client,net_connect,file_name):
            logger.info("connecting and doing the config from the file %s",client['host'])
            file_name_input = "config/"+str(file_name)
            output = net_connect.send_config_from_file(file_name_input)
            print(output)


