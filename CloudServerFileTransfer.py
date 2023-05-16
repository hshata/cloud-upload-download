import paramiko
import sys
import subprocess


#connecting to the first shell
vm = paramiko.SSHClient() #initiating our object vm [virtual machine server] (we can call this variable anything we want)

#***modify path to private key***#
vm.load_host_keys('C:\\Users\\xxxxx\\.ssh\\known_hosts') #loading the private key [must match the public key on the server]
vm.load_system_host_keys() #activating our priate key

#***modify username and hostname if needed***#
vm.connect(hostname='xxx.xxxx.xxx', username='xxxx') #connecting with our server with hostname and username 

#Now transporting to our next shell
vmtransport = vm.get_transport() #initiating the transport service

#***modify based on which server you want to reach (destiny server)***#
dest_addr = ('10.xx.x.x', 22) #this is the cloud server ip address
#***modify local IP Address***#
local_addr = ('192.xxx.xx.x', 22) #this is our local PC IP address 
vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr) #now transporting from our local PC to cloud server through tcpip

#Now creating our ssh jumb variable
jhost = paramiko.SSHClient()

#***modify path to private key***#
jhost.load_host_keys('C:\\Users\\xxxx\\.ssh\\known_hosts') #loading the private key for the jump host 
jhost.load_system_host_keys() #activating our priate key for the jumb service

#Now sending a connect request to our second shell [our destination - cloud server]
#***modify the hostname, username, and password based on which server you want to jump to***#
jhost.connect(hostname='xxx.xxxx.xxx', username='xxx', password='xxx', 
              sock=vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)) 

#Asking the cloud serve to show us all the file on their capacit by using exec_command('ls -la')
stdin, stdout, stderr = jhost.exec_command('ls -la')

#*** remove the # to uncomment this line and to test the outcome and decode it***#
#print(f'STDOUT: {stdout.read().decode("utf8")}') #printing all the files on the server and decoding it 

#***modify the (path to the file you want to download, and the name it will be written with on your PC after downloading)***#
download = jhost.open_sftp() #download client
download.get('/home/xxx/xxx/xxx.txt','downloaded.txt') 

upload = jhost.open_sftp() # upload client
upload.put('upload.txt','/home/native/xxx/xxx.txt') #upload file and location

#This is to close our session after we finish each cycle/task
download.close() #closing our download session
jhost.close() #closing our session with the cloud server
vm.close() #closing our session with the console




