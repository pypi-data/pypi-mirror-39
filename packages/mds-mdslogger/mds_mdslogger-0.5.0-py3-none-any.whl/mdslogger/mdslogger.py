#!/usr/bin/python

from liblogger import MdsLogger

#***********
# beispiel *
#***********

class Test1:
  def test2(self):
    """ test
    """
    ob1 = MdsLogger('Duplicati', conlogger=True, filelogger=True, maxlogsize=5000, logfilebackups=2, loglev='debug', loglevcon='info', loglevfile='debug')
    ob1.getLogObj().debug('ein Info-Text ein Info-Text ein Info-Text ein Info-Text ein Info-Text ein Info-Text')
    ob1.getLogObj().info('ein Info-Text ein Info-Text ein Info-Text ein Info-Text ein Info-Text ein Info-Text')
    ob1.getLogObj().warning('ein Info-Text ein Info-Text ein Info-Text ein Info-Text ein Info-Text ein Info-Text')
    ob1.getLogObj().error('ein Info-Text ein Info-Text ein Info-Text ein Info-Text ein Info-Text ein Info-Text')
    ob1.getLogObj().critical('ein Info-Text ein Info-Text ein Info-Text ein Info-Text ein Info-Text ein Info-Text')
    del ob1

if __name__ == '__main__':
#   ob1 = MdsLogger('testlog', conlogger=True, filelogger=True, maxlogsize=5000, logfilebackups=2, loglev='debug')
#   ob1.getLogObj().info('ein Info-Text')
#   ob1.getLogObj().debug('ein Debug-Text')
#   del ob1
  ob2 = Test1()
  ob2.test2()
  del ob2
