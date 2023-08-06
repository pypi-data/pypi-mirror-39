# -*- coding: utf-8 -*-


import libvirt
from time import sleep
from datetime import datetime


class MdsVirtlib:
    """ get access to functions of libvirt
    """
    def __init__(self, uri='qemu:///system'):
        """ uri = URI to host
        """
        self.__conn = libvirt.open(uri)
        if isinstance(self.__conn, type(None)):
            raise Exception('no connection to "%s"' % uri)

    def __del__(self):
        """ cleanup
        """
        self.__conn.close()
        del self.__conn
    
    def getDomainsActive(self):
        """ get list of running domains
        """
        l1 = []
        for i in self.__conn.listDomainsID():
            d1 = self.__conn.lookupByID(i)
            l1.append(d1.name())
            del d1
        return l1
    
    def getDomainsInactive(self):
        """ get list of not running domains
        """
        return self.__conn.listDefinedDomains()
    
    def isVmActive(self, vmname):
        """ get True if domain is running
        """
        d1 = self.__conn.lookupByName(vmname)
        if d1.isActive():
            del d1
            return True
        else :
            del d1
            return False
      
    def startVm(self, vmname):
        """ starts a VM
        """
        if not isinstance(vmname, type('')):
            raise ValueError('vmname != string')
        d1 = self.__conn.lookupByName(vmname)
        if not d1.isActive():
            d1.create()
        del d1
      
    def stopVm(self, vmname, cmdcnt=1, waiting=600, cmdrepeat=60):
        """ stops a/a few VMs
            'vmname' = name of the VM or list of the VMs,
            'cmdcnt' = number of repeats of the shutdown-command - Windows: 2...3x,
            'waiting' = function waits ...seconds for the inactive-state of the VM
            'cmdrepeat' = waiting time [sec] until the shutdown command is repeated,
            returnwert: True if stopped, False if still running
        """
        # check parameters
        if not isinstance(vmname, (type(''), type([]))):
            raise ValueError('vmname must be string or list')
        if not isinstance(cmdcnt, type(1)):
            raise ValueError('cmdcnt must be integer')
        if (cmdcnt < 1) or (cmdcnt > 10):
            raise ValueError('cmdcnt: 1...10, (is: %d)' % cmdcnt)
    
        if not isinstance(waiting, type(1)):
            raise ValueError('waiting must be integer')
        if (waiting < 10) or (waiting > 1200):
            raise ValueError('waiting: 10...1200, (is: %d)' % waiting)
    
        if not isinstance(cmdrepeat, type(1)):
            raise ValueError('cmdrepeat must be integer')
        if (cmdrepeat < 20) or (cmdrepeat > 1200):
            raise ValueError('cmdrepeat: 20...1200, (is: %d)' % cmdrepeat)
          
        if isinstance(vmname, type('')):
            vmname = [vmname]
        vmlst = []
        for i in vmname:
            vmlst.append(self.__conn.lookupByName(i))
    
        # check active
        isakt = lambda i1: i1.isActive()
        
        dt1 = datetime.now()
        # request VMs which are still active
        while (map(isakt, vmlst).count(1) > 0) and \
            ((datetime.now() - dt1).seconds < waiting):
    
            # send shutdown command
            cntwdh = 0
            while cntwdh < cmdcnt:
                # shutdown command to all VMs in list
                for i in vmlst:
                    if i.isActive():
                        i.shutdown()
                cntwdh += 1
                if cntwdh < cmdcnt:
                    sleep(3.0)
    
            # wait for command-repeat and max period
            dt2 = datetime.now()
            while (map(isakt, vmlst).count(1) > 0) and \
                ((datetime.now() - dt2).seconds < cmdrepeat) and \
                ((datetime.now() - dt1).seconds < waiting):
                sleep(1.5)

            if map(isakt, vmlst).count(1) > 0:
                for i in vmlst:
                    del i
                del vmlst
                return False
            else :
                for i in vmlst:
                    del i
                del vmlst
                return True

    def getDomainXML(self, vmname):
        """ get XML-definition of the domain
        """
        b1 = self.__conn.lookupByName(vmname)
        t1 = b1.XMLDesc(0)
        del b1
        return t1
    
    def getSnapshotXML(self, vmname, snapshot):
        """ get xml-code of a snapshot
        """
        b1 = self.__conn.lookupByName(vmname)
        sn1 = b1.snapshotLookupByName(snapshot, 0)
        t1 = sn1.getXMLDesc(0)
        del sn1
        del b1
        return t1
    
    def getListOfSnapshots(self, vmname):
        """ get list of snapshots of the VMs
        """
        b1 = self.__conn.lookupByName(vmname)
        l1 = b1.snapshotListNames(0)
        del b1
        return l1

# end MdsVirtlib
