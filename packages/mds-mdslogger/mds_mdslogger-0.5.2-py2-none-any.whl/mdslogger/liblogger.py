# -*- coding: utf-8 -*-

# konfigurierbarer logger


import sys, traceback, logging, copy
from logging.handlers import RotatingFileHandler

try :
  from logging.handlers import SysLogHandler
except :
  SysLogHandler = none
try :
  from logging.handlers import NTEventLogHandler
except :
  NTEventLogHandler = none
  


def formatExceptionInfo(maxTBlevel=5):
    """ erstellt eine formatierte ausgabe für exceptions
    """
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
        excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)
# ende formatExceptionInfo


def formatLogRecord(msg1, anzleer):
    """ ändert die formatierung des textes im record
    """
    if '\n' in msg1:
        t2 = ''.zfill(anzleer).replace('0',' ')
        msg1 = '\n%s+- ' % t2 + msg1.replace('\n', '\n%s|- ' % t2) + '\n%s--' % t2
    return msg1
# ende formatLogRecord

  
class MyStreamHandler(logging.StreamHandler):
    """ angepaßte Behandlung von Zeilenumbrüchen in den Texten
    """
    def __init__(self, anzleer=0):
        """ speichert voreinstellungen
        """
        super(self.__class__, self).__init__()
        self.anzleer = anzleer
    
    def emit(self, rec1):
        """ text anpassen
        """
        rec2 = copy.deepcopy(rec1)
        rec2.msg = formatLogRecord(rec2.msg, self.anzleer)
        super(self.__class__, self).emit(rec2)
# MyStreamHandler


class MyRotatingFileHandler(RotatingFileHandler):
    """ angepaßte Behandlung von Zeilenumbrüchen in den Texten
    """
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0, anzleer=0):
        """ klasse starten
        """
        super(self.__class__, self).__init__(filename, mode=mode, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding, delay=delay)
        self.anzleer = anzleer
    
    def emit(self, rec1):
        """ text anpassen
        """
        rec2 = copy.deepcopy(rec1)
        rec2.msg = formatLogRecord(rec2.msg, self.anzleer)
        super(self.__class__, self).emit(rec2)

# ende MyRotatingFileHandler


class MyFileHandler(logging.FileHandler):
    """  angepaßte Behandlung von Zeilenumbrüchen in den Texten
    """
    def __init__(self, filename, mode='a', encoding=None, delay=False, anzleer=0):
        """
        """
        super(self.__class__, self).__init__(filename, mode=mode, encoding=encoding, delay=delay)
        self.anzleer = anzleer
    
    def emit(self, rec1):
        """ text anpassen
        """
        rec2 = copy.deepcopy(rec1)
        rec2.msg = formatLogRecord(rec2.msg, self.anzleer)
        super(self.__class__, self).emit(rec2)
    
# ende MyFileHandler


class MdsLogger:
    """ eine Loggingklasse mit verschiedenen vorbereiteten handlern
    """
    def __init__(self, jobname, conlogger=True, filelogger=False, ntlogger=False, syslogger=False, \
          maxlogsize=0, logfilebackups=0, logfilename='', \
          loglev='info', loglevcon=None, loglevfile=None, loglevnt=None, loglevsys=None, \
          minNameLen=0):
        """ einstellungen
            jobname: Name des Loggers
            conlogger: True = Textausgabe in der Konsole
            filelogger: False = keine Logdatei, True = schreibt in Logdatei
            maxlogsize: maximale dateigröße der logdatei in KB, wenn größer --> neue Datei wird begonnen
                        0 = größe unbegrenzt
            logfilebackups: Anzahl Backup-Logdateien, 0 = keine
            logfilename: Name der Logdatei
            loglev: level der Ausgabemeldungen, gesamt
            loglevcon: Level für Meldungen für Konsole
            loglevfile: Level für Meldungen für Datei
            loglevnt: Level für Meldungen für WindowsLog
            loglevsys: Level für Meldungen für syslog
            ntlogger: True = schreibt auch in den Eventlog von Windows
            syslogger: True = schreibt auch in den syslog von linux
            minNameLen: Mindestlänge des Funktionsnamens in der Textausgabe der Logzeile
        """
        self.version = '0.5.1'
        self.__jobname = jobname
        if isinstance(logfilename, type('')):
            self.__logfilename = logfilename
        else :
            self.__logfilename = ''
          
        if conlogger in [True, False]:
            self.__conlogger = conlogger
        else :
            self.__conlogger = True
          
        if filelogger in [True, False]:
            self.__filelogger = filelogger
        else :
            self.__filelogger = False
          
        if isinstance(maxlogsize, type(1)):
            self.__maxlogsize = maxlogsize * 1024
        else :
            self.__maxlogsize = 0
          
        if isinstance(logfilebackups, type(1)):
            self.__logfilebackups = logfilebackups
        else :
            self.__logfilebackups = 0
          
        if ntlogger in [True, False]:
            self.__ntlogger = ntlogger
        else :
            self.__ntlogger = False
          
        if syslogger in [True, False]:
            self.__syslogger = syslogger
        else :
            self.__syslogger = False

        if loglev in ['debug','info','warning','error','critical']:
            self.__loglev = loglev
        else :
            self.__loglev = 'info'
        
        if loglevcon in ['debug','info','warning','error','critical']:
            self.__loglevcon = loglevcon
        else :
            self.__loglevcon = self.__loglev
        
        if loglevfile in ['debug','info','warning','error','critical']:
            self.__loglevfile = loglevfile
        else :
            self.__loglevfile = self.__loglev
          
        if loglevnt in ['debug','info','warning','error','critical']:
            self.__loglevnt = loglevnt
        else :
            self.__loglevnt = self.__loglev
          
        if loglevsys in ['debug','info','warning','error','critical']:
            self.__loglevsys = loglevsys
        else :
            self.__loglevsys = self.__loglev

        self.__logobj = self.__setupLogger(minNameLen)

    def __del__(self):
        """ aufräumen
        """
        del self.__logobj
    
    def getLogObj(self):
        """ liefert das logobjekt
        """
        return self.__logobj
    
    def __getLogLevel(self, loglev):
        """ liefert den korrekten loglevel
        """
        if loglev == 'debug':
            return logging.DEBUG
        elif loglev == 'info':
            return logging.INFO
        elif loglev == 'warning':
            return logging.WARNING
        elif loglev == 'error':
            return logging.ERROR
        elif loglev == 'critical':
            return logging.CRITICAL
        else :
            return logging.INFO

    def __setupLogger(self, minbreite=0):
        """ logger einstellen
            'minbreite: gibt die mindestbreite für den funktionsnamen an'
        """
        if len(self.__jobname) > 0:
            logger = logging.getLogger(self.__jobname)
        else :
            logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(self.__getLogLevel(self.__loglev))
  
        # darstellung der ausgabe
        if minbreite == 0:
            formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)08s %(funcName)s: %(message)s')
        else :
            formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)08s %(funcName)' + '%d' % minbreite + 's: %(message)s')
    
        # leerzeichen vor der einrückung bei mehrzeiligen texten
        anzleerzeichen = 10
        
        # ausgabe in console
        if self.__conlogger == True:
            streamhandle = MyStreamHandler(anzleer = anzleerzeichen)  #logging.StreamHandler()
            streamhandle.setLevel(self.__getLogLevel(self.__loglevcon))
            streamhandle.setFormatter(formatter)
            logger.addHandler(streamhandle)
            
        # dateiausgabe
        if self.__filelogger == True:
            logdatei = '%s.log' % self.__jobname
            if len(self.__logfilename) > 0:
                logdatei = self.__logfilename
            if self.__maxlogsize > 0:      
                filehandle = MyRotatingFileHandler(logdatei, maxBytes=self.__maxlogsize, backupCount=self.__logfilebackups, anzleer = anzleerzeichen)
            else :
                filehandle = MyFileHandler(logdatei, anzleer = anzleerzeichen)
            filehandle.setLevel(self.__getLogLevel(self.__loglevfile))
            filehandle.setFormatter(formatter)
            logger.addHandler(filehandle)

        # ausgabe in windows-eventlog
        if self.__ntlogger == True:
            if isinstance(NTEventLogHandler, type(None)):
                ntlog = NTEventLogHandler(self.__jobname, logtype='Application')
                ntlog.setLevel(self.__getLogLevel(self.__loglevnt))
                ntlog.setFormatter(formatter)
                logger.addHandler(ntlog)

        # ausgabe in unix-syslog
        if self.__syslogger == True:
            if isinstance(SysLogHandler, type(None)):
                formatter2 = logging.Formatter('%(name)s %(levelname)s %(funcName)s: %(message)s')
                syslogr = SysLogHandler(address='/dev/log')
                syslogr.setLevel(self.__getLogLevel(self.__loglevsys))
                syslogr.setFormatter(formatter2)
                logger.addHandler(syslogr)
        return logger

# ende class MdsLogger
