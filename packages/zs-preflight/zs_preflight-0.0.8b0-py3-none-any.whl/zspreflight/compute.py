#!/usr/bin/python
import subprocess

class compute_check():
    def __init__(self):
        self.cpuinfo = self._get_cpu_info()

    def cpu_architecture(self):
        #cpu x86-64 or not
        #output - result true/false
        #       - optional true/false
        #       - cpu - cpu architecture
        if(self.cpuinfo['Architecture'] == 'x86_64'):
            return {'result':'Pass','optional':False,'out':self.cpuinfo['Architecture'],'text':'CPU Architecture'}
        else:
            return {'result':'Fail','optional':False,'out':self.cpuinfo['Architecture'],'text':'CPU Architecture'}

    def cpu_type(self):
        #cpu family
        #cpu manufacturer
        if(self.cpuinfo['Vendor ID'] == 'GenuineIntel' or self.cpuinfo['Vendor ID'] == 'AuthenticAMD'):
            return {'result':'Pass','optional':False,'out':self.cpuinfo['Vendor ID'],'text':'CPU Vendor'}
        else:
            return {'result':'Fail','optional':False,'out':self.cpuinfo['Vendor ID'],'text':'CPU Vendor'}

    def cpu_core_count(self):
        #cpu count
        #how many cpu cores
        #is it hyperthreading
        out = {}
        if(int(self.cpuinfo['Thread(s) per core']) >= 2):
            self.cpuinfo['hyperthreading'] = True
            self.htcores = int(self.cpuinfo['Thread(s) per core']) * int(self.cpuinfo['Core(s) per socket'])
            out = {
                    'cpu_sockets':self.cpuinfo['CPU(s)'],
                    'cpu_cores':self.cpuinfo['Core(s) per socket'],
                    'hyperthreading':self.cpuinfo['hyperthreading'],
                    'out':self.htcores,
                    'result':'Fail',
                    'optional':False,
                    'text':'Physical CPU Cores + HT'
                    }
        elif(int(self.cpuinfo['Thread(s) per core']) == 1):
            self.cpuinfo['hyperthreading'] = False
            self.htcores = int(self.cpuinfo['Core(s) per socket'])
            out = {
                    'cpu_sockets':self.cpuinfo['CPU(s)'],
                    'cpu_cores':self.cpuinfo['Core(s) per socket'],
                    'hyperthreading':self.cpuinfo['hyperthreading'],
                    'out':self.htcores,
                    'result':'Fail',
                    'optional':False,
                    'text':'Physical CPU Cores'
                    }
        else:
            out = {
                'cpu_cores':1,
                'cpu_sockets':1,
                'hyperthreading':False,
                'out':1,
                'result':'Fail',
                'optional':False,
                'text':'Physical CPU Cores'
                }
        if(int(self.cpuinfo['Core(s) per socket']) >= 4):
            out['result'] = 'Pass'
            out['text'] = 'Physical cores'
        if(int(self.cpuinfo['Core(s) per socket']) >= 8):
            out['result'] = 'Pass'
            out['text'] = 'Physical cores'

        return out

    def cpu_virt_extensions(self):
        #check if the host is physical or virtual
        if('Virtualization' not in self.cpuinfo):
            return {'result':'Fail',
                    'optional':False,
                    'cpuvendor':self.cpuinfo['Vendor ID'],
                    'out':'Unknown',
                    'text':'Virtual extensions'
                    }

        if(self.cpuinfo['Vendor ID'] == 'GenuineIntel'):
            if(self.cpuinfo['Virtualization'] == 'VT-x'):
                return {'result':'Pass',
                        'optional':False,
                        'cpuvendor':self.cpuinfo['Vendor ID'],
                        'out':self.cpuinfo['Virtualization'],
                        'text':'Virtual extensions'
                        }

        elif(self.cpuinfo['Vendor ID'] == 'AuthenticAMD'):
            if(self.cpuinfo['Virtualization'] == 'AMD-V'):
                return {'result':'Pass',
                        'optional':False,
                        'cpuvendor':self.cpuinfo['Vendor ID'],
                        'out':self.cpuinfo['Virtualization'],
                        'text':'Virtual extensions'
                        }
        else:
            return {'result':'Fail',
                    'optional':False,
                    'cpuvendor':self.cpuinfo['Vendor ID'],
                    'out':None,
                    'text':'Virtual extensions'
                    }

    def cpu_virtualized(self):
        if('Hypervisor vendor' in self.cpuinfo):
            self.virtcpu = True
            self.hypervisor = self.cpuinfo['Hypervisor vendor']
            self.virttype = self.cpuinfo['Virtualization type']
            self.result = 'Fail'
        else:
            self.virtcpu = False
            self.hypervisor = None
            self.virttype = None
            self.result = 'Pass'

        return {'text':'CPU Not Virtualized','result':self.result,'optional':False,'virtualcpu':self.virtcpu,'out':self.hypervisor,'virtualization':self.virttype}


    def _get_cpu_info(self):
        #Convert a comand line string type output to a dict and clean up everything
        try:
            proc = subprocess.Popen("lscpu", stdout=subprocess.PIPE, shell=True)
            (output, err) = proc.communicate()
            output = str(output).strip()
            output = output.split('\n')
            cpu_dict = {}
            for out in output:
                split = out.split(':')
                cpu_dict[split[0]] = str(split[1]).strip()
            return cpu_dict
        except Exception as e:
            return e

    """
    #coming soon
    def _get_cpu_family(self,cpu_type,cpu_model):
        if(cpu_type == 'AuthenticAMD'):
            self.cpus = [{'cpu_model':}]
            pass
        else:
            #intel
            self.cpus = [{}]
            pass

        for cpu in cpus:
            if cpu_model == cpu['cpu_model']:
                return cpu
    """
