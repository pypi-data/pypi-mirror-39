#!/usr/bin/python
import subprocess
import fnmatch

class storage_check():
    def __init__(self):
        self.drives = self._get_drives()
        self.controllers = self._get_storage_controllers()

    def internal_drive_count(self):
        #how many total drives
        ssd = self.drives['ssd_host_disks']
        hdd = self.drives['hdd_host_disks']

        total = ssd + hdd
        out = {'out':ssd + hdd,'result':'Fail','optional':False,'text':'Drive Count'}
        if(total >= 2):
            out = {'out':ssd + hdd,'result':'Pass','optional':False,'text':'Drive Count'}
        return out

    def check_disk_size(self):
        #are the disks in the system the right size
        #out = {'valid':False,'size':0,'name':None}
        drive = []
        for disk in self.drives['disks']:
            size = float(disk['size'][:-1])
            #convert size to MB
            if(disk['size'][-1:] == 'G'):
                size = size * 1000
            elif(disk['size'][-1:] == 'T'):
                size = size * 1000000
            if(size >= 512):
                self.valid_size = 'Pass'
            else:
                self.valid_size = 'Fail'
            disk['size_valid'] = self.valid_size
            drive.append(disk)
        self.drives['out'] = drive
        self.drives['text'] = 'Disk Specs'
        return self.drives

    """
    Coming soon
    def check_disk_controller(self):
        #Are disks attached to a raid controller

        for controller in self.controllers['storage_controllers']
    """

    def get_disk_controllers(self):
        out = {'out':[],'optional':True,'result':'Pass','text':'Storage Controllers'}
        if(len(self.controllers['storage_controllers'])):
            out = {'out':self.controllers['storage_controllers'],'optional':True,'result':'Pass','text':'Storage Controllers'}
        return out

    def get_disk_IO(self):
        #check the generic disk IO for the discovered disks
        drive_out = self._get_drive_stats()
        return drive_out


    ###########Internal
    def _get_drive_stats(self):
        """
        Return an array of dictionaries
        """
        drives = self._get_drives()
        drive_out = []
        for drive in drives['disks']:
            #get drive reads
            try:
                proc = subprocess.Popen("sudo hdparm -Tt /dev/%s"%(drive['name']), stdout=subprocess.PIPE, shell=True)
                (output,err) = proc.communicate()
                outputs = str(output).strip().split('\n')
                outputs.pop(0)
            except Exception as e:
                print e

            #get the drive writes
            try:
                spec2 = {}
                proc2 = subprocess.check_output(['sudo', 'dd', 'if=/dev/zero', 'of=/dev/%s'%(drive['name']),'bs=1024','count=1000','oflag=dsync'], stderr=subprocess.STDOUT)
                outputs2 = str(proc2).strip().split('\n')
                spec2['name'] = drive['name']
                spec2['test'] = 'Write 1024KB, Count 1000'
                outputs2 = str(outputs2[2]).split(',')
                spec2['speed'] = str(outputs2[3]).strip()
                spec2['throughput'] = "1024kb in %s"%str(outputs2[2]).strip()
                drive_out.append(spec2)
            except Exception as e:
                print e

            #Build the drive read formatted out
            for output in outputs:
                spec = {}
                split = output.split(':')
                spec['name'] = drive['name']
                spec['test'] = str(split[0]).strip()
                for s in split:
                    speed = s.split('=')
                spec['speed'] = str(speed[1]).strip()
                spec['throughput'] = str(speed[0]).strip()
                drive_out.append(spec)

        return drive_out

    def _get_drives(self):
        try:
            proc = subprocess.Popen("lsblk -d -o name,rota,size", stdout=subprocess.PIPE, shell=True)
            (output,err) = proc.communicate()
            output = str(output).strip()
            output = output.split('\n')
            output.pop(0)
            disks = []
            ssd_count = 0
            hdd_count = 0
            out = {'ssd_host_disks':ssd_count,'hdd_host_disks':hdd_count,'disks':disks,'result':False,'optional':False}
            for o in output:
                disk = {}
                split = o.split()
                disk['name'] = split[0]
                if(fnmatch.fnmatch(disk['name'], 'sr*')):
                    continue
                if(split[1] == '1'):
                    hdd_count += 1
                    disk['type'] = 'hdd'
                else:
                    ssd_count += 1
                    disk['type'] = 'ssd'
                disk['size'] = split[2]
                disks.append(disk)
            out = {'ssd_host_disks':ssd_count,'hdd_host_disks':hdd_count,'disks':disks,'result':True,'optional':False}
        except Exception as e:
            out = {'ssd_host_disks':None,'hdd_host_disks':None,'disks':None,'result':e,'optional':False}

        return out

    def _get_storage_controllers(self):
        #Get the storage controllers and return them
        try:
            proc = subprocess.Popen("lspci | grep 'IDE\|SATA\|RAID\|SCSI'", stdout=subprocess.PIPE, shell=True)
            (output,err) = proc.communicate()
            output = str(output).strip()
            output = output.split('\n')
            sc_count = len(output)
            controllers = []
            out = {'storage_controller_count':0,'storage_controller_type':controllers,'result':False}
            if(sc_count > 0):
                for o in output:
                    split = o.split(': ')
                    controllers.append({'controller':split[1],'pci':split[0][0:7],'type':split[0][8:]})
                out = {'storage_controller_count':len(controllers),'storage_controllers':controllers,'result':True}
        except Exception as e:
            out = {'storage_controller_count':None,'storage_controllers':[],'result':e}

        return out