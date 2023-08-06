#!/usr/bin/python


# tests
if __name__ == '__main__':
  ob1 = MdsVirtlib()
  print 'aktiv:',ob1.getDomainsAktiv()
  print 'inaktiv:',ob1.getDomainsInaktiv()
  print 'isaktiv:',ob1.isVmAktiv('vm18-kubuntu-15.10')
  #print 'shutdown:',ob1.stopVm(['vm18-kubuntu-15.10','vm17-ubu-1510'])
  #print 'start vm17:',ob1.startVm('vm17-ubu-1510')
  #print 'getSnapshotXML:',ob1.getSnapshotXML('vm17-ubu-1510', 'nach-install')
  del ob1


