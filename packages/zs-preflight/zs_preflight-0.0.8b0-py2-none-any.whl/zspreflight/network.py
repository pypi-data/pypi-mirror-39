#!/usr/bin/python
import subprocess
import os

class network_check():
    def __init__(self):
        pass

    def nic_count(self):
        out = {'out':0,'result':'Fail','optional':False,'text':'System NIC Count'}
        try:
            proc = subprocess.Popen("sudo ls -I br* -I lo -I vir* /sys/class/net/", stdout=subprocess.PIPE, shell=True)
            (output,err) = proc.communicate()
            output = str(output).strip()
            output = len(output.split('\n'))
            out = {'out':output,'result':'Pass','optional':False,'text':'System NIC Count'}
        except Exception as e:
            out = {'out':'Unknown','result':e,'optional':False,'text':'System NIC Count'}

        return out

    def nic_type(self):
        #nic speed
        #nic type
        nic = []
        out = {'result':'Fail','optional':False,'out':nic,'text':'System Nic Info'}
        #supress output
        null = open(os.devnull, 'w')
        try:
            output = self._list_nics()
            for o in output:
                #if (os.path.isdir("/sys/class/net/"+o)):
                    #skip if the net card does not exist
                #    continue
                did = subprocess.Popen("sudo ls -al /sys/class/net/%s/device"%o, stdout=null, shell=True)
                (didout,err) = did.communicate()
                didout = str(didout).strip()[-7:]
                #use lspci and grep to get nicbrand
                brand = subprocess.Popen("sudo lspci | grep %s"%didout, stdout=subprocess.PIPE, shell=True)
                (brandout,err) = brand.communicate()
                nic_brand = str(brandout).strip()[29:]
                if(nic_brand == ''):
                    nic_brand = 'Unknown'
                try:
                    speed = open("/sys/class/net/%s/speed"%o,'r')
                    if(int(speed.read()) < 0 or int(speed.read())):
                        nic.append({'nic_name':o,'nic_speed':0,'nic_brand':nic_brand,'text':'NIC not recommended'})
                    elif(int(speed.read()) > 0):
                        nic_speed = int(speed.read())
                        if(nic_speed == 1000):
                            nic.append({'nic_name':o,'nic_speed':nic_speed,'nic_brand':nic_brand,'text':'NIC minimum config'})
                        elif(nic_speed >= 10000):
                            nic.append({'nic_name':o,'nic_speed':nic_speed,'nic_brand':nic_brand,'text':'NIC recommended config'})
                except Exception as e:
                    nic.append({'nic_name':o,'nic_speed':'Unknown','nic_brand':nic_brand,'text':'NIC Unknown'})
            out = {'result':'Pass','optional':False,'out':nic,'text':'System Nic Info'}
        except Exception as e:
            out = {'result':e,'optional':False,'out':nic,'text':'System Nic Info'}

        return out

    def nic_configured(self):
        #check if the nic is configured and up
        con_out = []
        out = {'out':'Host Not Connected','result':'Fail','optional':False,'text':'NIC UP','nic_out':con_out}
        try:
            output = self._list_nics()
            link = 0
            for o in output:
                proc = subprocess.Popen("ip link show | grep %s"%o, stdout=subprocess.PIPE, shell=True)
                (output,err) = proc.communicate()
                con = str(output).strip().split()
                if(con[8] == 'UP'):
                    link +=1
                con_out.append({'nic':con[1],'state':con[8],'mtu':con[4],'mode':con[10]})
        except Exception as e:
            out = {'out':'Unknown','result':e,'optional':False,'text':'NIC UP','nic_out':con_out}

        if(len(con_out) >= 1 and link >= 1):
            out = {'out':'Host Connected','result':'Pass','optional':False,'text':'NIC UP','nic_out':con_out}
        else:
            out = {'out':'Host Not Connected','result':'Fail','optional':False,'text':'NIC UP','nic_out':con_out}

        return out

    def connected_to_network(self):
        #get the local IP config, and if connected to the local network
        #ping the gateway
        #ping the local IP
        con_out = []
        out = {'out':'Local Net Down','result':'Fail','optional':False,'text':'Local Net Comm','nic_out':con_out}
        nics = self._list_nics()
        try:
            link = False
            for n in nics:
                ip_info = self._get_nic_ip_info(n)
                #ping the local ip
                ping = {'nic':n,'gateway':'Down','local':'Down'}
                gateway = os.system("ping -c 1 " + ip_info['gateway'] + "> /dev/null 2>&1")
                local = os.system("ping -c 1 " + ip_info['ip'] + "> /dev/null 2>&1")
                if gateway == 0:
                    ping['gateway'] = 'Up'
                if local == 0:
                    ping['local'] = 'Up'
                if(ping['local'] == 'Up' and ping['gateway'] == 'Up'):
                    link = True
                con_out.append(ping)
        except Exception as e:
            con_out.append(e)
            out = {'out':'Local Net Unknown','result':'Fail','optional':False,'text':'Local Net Comm','nic_out':con_out}

        if(len(con_out) >= 1 and link == True):
            out = {'out':'Local Net Up','result':'Pass','optional':False,'text':'Local Net Comm','nic_out':con_out}

        return out

    def connected_to_internet(self):
        #check to see if host connected to internet
        con_out = []
        out = {'out':'Local Net Down','result':'Fail','optional':False,'text':'Local Net Comm','nic_out':con_out}
        nics = self._list_nics()
        try:
            link = False
            for n in nics:
                ip_info = self._get_nic_ip_info(n)

        except Exception as e:
            con_out.append(e)
            out = {'out':'Internet Down','result':'Fail','optional':False,'text':'Local Net Comm','nic_out':con_out}

####Internal functions
    def _list_nics(self):
        #return list of nic cards
        try:
            proc = subprocess.Popen("sudo ls -I br* -I lo -I vir* /sys/class/net/", stdout=subprocess.PIPE, shell=True)
            (output,err) = proc.communicate()
            output = str(output).strip().split()
        except Exception as e:
            output = []

        return output

    def _get_nic_ip_info(self,nic):
        try:
            proc = subprocess.Popen("ip addr | grep '%s' -A2 | grep 'inet' | head -1 | awk '{print $2}' | cut -f1  -d'/'"%nic, stdout=subprocess.PIPE, shell=True)
            (output,err) = proc.communicate()
            ip = str(output).strip()
        except Exception as e:
            ip = e

        try:
            proc2 = subprocess.Popen("/sbin/ip route | awk '/default/ { print $3 }'", stdout=subprocess.PIPE, shell=True)
            (output2,err2) = proc2.communicate()
            gateway = str(output2).strip()
        except Exception as e:
            gateway = e

        return {'ip':ip,'gateway':gateway}