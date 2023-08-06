#!/usr/bin/python
import subprocess
import socket
import os

class host_check():
    def __init__(self):
        pass

    def host_ipmi(self):
        #check if the host has IPMI
        try:
            proc = subprocess.Popen("sudo dmidecode --type 38", stdout=subprocess.PIPE, shell=True)
            (output,err) = proc.communicate()
            output = str(output).strip()
            output = output.split('\n')
            out = {'out':False,'result':'Fail','optional':True,'text':'Host IPMI'}
            if ('IPMI Device Information' in output):
                out = {'out':True,'result':'Pass','optional':True,'text':'Host IPMI'}
        except Exception as e:
            out = {'out':None,'result':e,'optional':True,'text':'Host IPMI'}

        return out

    def host_usb(self):
        #check if the host has usb ports
        #if so how many
        try:
            proc = subprocess.Popen("sudo lspci | grep 'USB2'", stdout=subprocess.PIPE, shell=True)
            (output,err) = proc.communicate()
            output = str(output).strip()
            output = len(output.split('\n'))
            out = {'out':0,'result':'Fail','optional':False,'text':'Host USB2 Ports'}
            if(output > 0):
                out = {'out':output,'result':'Pass','optional':False,'text':'Host USB2 Ports'}
        except Exception as e:
            out = {'out':None,'optional':False,'result':e,'text':'Host USB2 Ports'}

        return out

    def host_disks(self):
        #check if there are any disks in the host
        #if so are they attached to a raid controller
        try:
            proc = subprocess.Popen("sudo lsblk -d -o name", stdout=subprocess.PIPE, shell=True)
            (output,err) = proc.communicate()
            output = str(output).strip()
            output = output.split('\n')
            output.pop(0)
            out = {'out':0,'result':'Fail','optional':False,'text':'Host Disks'}
            if(output > 0):
                out = {'out':output,'result':'Pass','optional':False,'text':'Host Disks'}
        except Exception as e:
            out = {'out':None,'optional':False,'result':e,'text':'Host Disks'}

        return out

    def host_memory(self):
        #how much ram in gig does the host have
        #make sure it is more than 32GB
        out = {'out':0,'result':'Fail','optional':False,'text':'Host Memory'}
        try:
            mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
            mem_gib = mem_bytes/(1024.**3)
            if(int(mem_gib) == 64):
                out = {'out':str(int(mem_gib))+'GB'+' - minimum, 96GB recommended.','result':'Pass','optional':False,'text':'Host Memory'}
            elif(int(mem_gib) >= 96):
                out = {'out':str(int(mem_gib))+'GB'+' - recommended amount of memory','result':'Pass','optional':False,'text':'Host Memory'}
            else:
                out = {'out':str(int(mem_gib))+'GB'+' - minimum memory, 64GB, not available','result':'Fail','optional':False,'text':'Host Memory'}
        except Exception as e:
            out = {'out':None,'optional':False,'result':e,'text':'Host Memory'}

        return out

    def host_name(self):
        hostname = socket.gethostname()
        return {'out':hostname,'result':'Pass','optional':True,'text':'Host Name'}