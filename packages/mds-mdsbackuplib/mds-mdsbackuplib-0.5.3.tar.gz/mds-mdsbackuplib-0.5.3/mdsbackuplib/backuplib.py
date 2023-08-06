# -*- coding: utf-8 -*-

import os, datetime, time
from mdslogger import MdsLogger, formatExceptionInfo
from mdsshellcommand import ShellCommandRun
from mdslibvirt import MdsVirtlib


class TarGpgBackup:
    """ library to backup and encrypt qemu/kvm-instances
    """
    def __init__(self, vmname, targfoldr, vmfoldr, filelist=[], \
                targetserver=None, targetserverlogin=None, \
                targetserverprotocol='sftp',\
                packbackup=False, encryptfile=None, workonthefly=True, \
                tempfolder=None, logfile='', insertfilepara=None, doppelshutdown=False):
        """ settings
            'vmname' = name of the VM to save,
            'targfoldr' = folder in which the result is stored,
            'vmfoldr' = folder where the volume-files of VM are stored,
            'filelist' = list of VM-volume-files without path: ['<datei-1>', '<datei-2>', ('<datei-3>', False), ('datei-4', True)]
               string oder Tuple, Tuple: (<datei>, True|False), True = file is proccessed separate
            'targetserver' = server as backup-target, if used: 'targfoldr' is server-path,
            'targetserverlogin' = user:password for the upload-server,
            'targetserverprotocol' = protocol to connet to upload-server (default: sftp, allowed: http, https, ftp, sftp, ftps, smb), 
            'packbackup' = True enables compression of the out-file,
            'encryptfile' = if used, out-file is gpg-encrypted using the key from file,
            'workonthefly' = if True: proccessing without temp-files, 
                             set to False if the VM must be restartet fast,
            'tempfolder' = if used, source files are collected there as tar-file,  
                           and the VM is restarted, compress, encrypt followed afterwards
            'logfile' = file to store logs (or None),
            'doppelshutdown' = schickt das Kommando 'virsh shutdown ---' 2x an die VM (braucht Windows manchmal)
        """
        self.__vmname = vmname
        self.__insertfilepara = insertfilepara
        self.__multishutdown = doppelshutdown
        self.__lvirt = MdsVirtlib()

        # create logger
        self.__logobj = MdsLogger('tarbk', conlogger=True, \
              filelogger=True, maxlogsize=5000, logfilebackups=2, logfilename=logfile,\
              loglev='debug', loglevcon='info', loglevfile='debug')
        self.__log = self.__logobj.getLogObj()

        # create shell-command
        self.__cmd = ShellCommandRun('tarbk', self.__log)

        # store targetserver
        self.__targetserver = None
        self.__targetserverprotocol = 'sftp'
        if not isinstance(targetserver, type(None)):
            self.__targetserver = targetserver
        
        if isinstance(targetserverprotocol, type('')):
            self.__targetserverprotocol = targetserverprotocol
      
        # Logindata
        self.__targetserverlogin = None
        if not isinstance(targetserverlogin, type(None)):
            self.__targetserverlogin = targetserverlogin
      
        # on-the-fly-modus speichern
        if workonthefly in [True, False]:
            self.__workonthefly = workonthefly
        else :
            self.__log.warning('Parameter "workonthefly"=%s invalid (True/False)' % workonthefly)
      
        # save tempfolder
        self.__tempfolder = None
        if not isinstance(tempfolder, type(None)):
            self.__setTempDir(tempfolder)
    
        # store folder of vm-volumes
        self.__vmfolder = None
        self.__setVmDir(vmfoldr)
    
        # store target-folder for backup
        self.__targetfolder = None
        self.__setTargFoldr(targfoldr)

        # filelist erstellen
        self.__filelst = []
        self.__filelst_separat = []
        if isinstance(filelist, type([])):
            for i in filelist:
                if isinstance(i, type('')):
                    self.__addBackupfile(i)
                elif isinstance(i, type((1,))):
                    (d1, b1) = i
                    self.__addBackupfile(d1)
                    if b1 == True:
                        self.__filelst_separat.append(d1)
                else :
                    self.__log.warning("parameter 'filelist'=%s invalid, must string or tuple" % str(i))
        
        if packbackup in [True, False]:
            self.__packbackup = packbackup
        else :
            self.__log.warning("parameter 'packbackup'=%s invalid (True/False)" % packbackup)
    
        self.__enaencryptfile = None
        if not isinstance(encryptfile, type(None)):
            self.__setBackupEncrypt(encryptfile)
        
        self.waitsec = 120   # waiting time after start of VM
        self.__tarfile = ''    # file name used by 'packFiles'
        self.__filestem = ''
  
    def __del__(self):
        """ cleanup memory
        """
        self.__log = None
        del self.__logobj
        del self.__cmd
        del self.__lvirt

    def __setTempDir(self, dirname):
        """ stores temp-dir, if it exists
        """
        try :
            if os.path.exists(dirname):
                self.__tempfolder = dirname
            else :
                self.__tempfolder = None
                self.__log.warning('temp-directory "%s" dont exists' % dirname)
        except :
            self.__log.error(str(formatExceptionInfo()))
    
    def __setVmDir(self, dirname):
        """ store VM-directory, if it exists
        """
        try :
            if os.path.exists(dirname):
                self.__vmfolder = dirname
            else :
                self.__vmfolder = None
                self.__log.warning('VM-directory "%s" dont exists' % dirname)
        except :
            self.__log.error(str(formatExceptionInfo()))  

    def __setTargFoldr(self, dirname):
        """ store target folder, if exists
        """
        self.__targetfolder = None
        try :
            # dont check folder-exist if upload to server
            if isinstance(self.__targetserver, type(None)): 
                if os.path.exists(dirname):
                    self.__targetfolder = dirname
                else :
                    self.__targetfolder = None
                    self.__log.warning('target folder "%s" dont exist' % dirname)
            else :
                if isinstance(dirname, type('')):
                    if len(dirname) > 0:
                        self.__targetfolder = dirname
                    else :
                        self.__log.warning('no target folder given')
                else :
                    self.__log.warning('no target folder given')
        except :
            self.__log.error(str(formatExceptionInfo()))  

    def __addBackupfile(self, dateiname):
        """ add a file to the list of backup-files
        """
        try :
            if isinstance(self.__vmfolder, type(None)):
                self.__log.warning('VM-directory not set')
                return False
            fname = os.path.join(self.__vmfolder, dateiname)
            if os.path.exists(fname):
                self.__filelst.append(dateiname)
            else :
                self.__log.warning('file "%s" dont exists' % fname)
                return False
            return True 
        except :
            self.__log.error(str(formatExceptionInfo()))
            return False

    def __setBackupEncrypt(self, keyfile):
        """ switch encryption of backup on/off
        """
        if os.path.exists(keyfile):
            self.__enaencryptfile = keyfile
        else :
            self.__log.warning("key-file '%s' dont exists, encryption not active" % keyfile)
            self.__enaencryptfile = None

    def __getDateFilename(self, schema):
        """ create filename with date
        """
        try :
            dt1 = datetime.datetime.now()
            t1 = dt1.strftime('%Y%m%d_%H%M')
            t2 = '%s_%s' % (t1, schema)
            return t2
        except :
            self.__log.error(str(formatExceptionInfo()))

    def paraCheck(self):
        """ check parameter for backup
        """
        retval = True
        try :
            self.__log.info('+- checking parameter:')
            if not isinstance(self.__tempfolder, type(None)):
                self.__log.info('|- temp-folder: "%s"' % self.__tempfolder)
            else :
                self.__log.warning('|- temp-folder not set')
                retval = False
                
            if not isinstance(self.__targetfolder, type(None)):
                self.__log.info('|- target-folder: "%s"' % self.__targetfolder)
            else :
                self.__log.warning('|- target-folder not set')
                retval = False

            if not isinstance(self.__vmfolder, type(None)):
                self.__log.info('|- VM-folder: "%s"' % self.__vmfolder)
            else :
                self.__log.warning('|- VM-folder not set')
                retval = False

            if len(self.__filelst) > 0:
                self.__log.info('|- VM-filelist: "%s"' % str(self.__filelst))
            else :
                self.__log.warning('|- VM-filelist not set')
                retval = False
                
            if not isinstance(self.__targetserver, type(None)):
                if not self.__targetserverprotocol in ['http', 'https', 'ftp', 'sftp', 'ftps', 'smb']:
                    retval = False
                    self.__log.warning('|- Invalid protocol for uoload-server')
                else :
                    self.__log.info('|- backup will be uploaded to %s-server "%s"' % \
                        (self.__targetserverprotocol.upper(), self.__targetserver))
                    if isinstance(self.__targetserverlogin, type(None)):
                        self.__log.warning('|- no login data given for %s-server' % self.__targetserverprotocol.upper())
                        retval = False
                    else :
                        self.__log.info('|- %s-login data given' % self.__targetserverprotocol.upper())
                
            if self.__workonthefly == True:
                self.__log.info('|- onthefly-mode active, VM pauses longer')
            else :
                self.__log.info('|- no onthefly-mode, VM pauses short')
                
            if self.__packbackup == True:
                self.__log.info('|- backup will be compressed')
            else :
                self.__log.info('|- backup not compressed')
                
            if not isinstance(self.__enaencryptfile, type(None)):
                self.__log.info('|- backup will be encrypted with key from %s' % self.__enaencryptfile)
            else :
                self.__log.info('|- backup not encrypted')
                
            self.__log.info('-- finished parameter check, result: %s' % retval)
        except:
            self.__log.error(str(formatExceptionInfo()))
            retval = False
        return retval
      
    def __packFilesStep1(self, filelist):
        """ copies/compresses input-files to tar-file in temp-folder
        """
        try :
            flst = ''
            for i in filelist:
                flst += ' %s' % i
              
            # set target folder
            targetfolder = self.__tempfolder
            if isinstance(self.__enaencryptfile, type(None)) and \
                isinstance(self.__targetserver, type(None)):
                targetfolder = self.__targetfolder
        
            if self.__packbackup == False:
                self.__filestem = '%s.tar' % self.__getDateFilename(self.__vmname)
                self.__tarfile = os.path.join(targetfolder, self.__filestem)
                cmd1 = 'tar cvf %s %s' % (self.__tarfile, flst)
            else :
                self.__filestem = '%s.tar.gz' % self.__getDateFilename(self.__vmname)
                self.__tarfile = os.path.join(targetfolder, self.__filestem)
                cmd1 = 'tar cvzf %s %s' % (self.__tarfile, flst)
        
            # show filelist
            for i in filelist:
                cmd2 = 'ls -lGgha ' + i
                (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd2)
                self.__log.info('|-  +  %s' % tx1[12:].strip())
            self.__log.info('|- --> %s' % self.__tarfile)
              
            # copy processing
            (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
            if stat1 == False:
                self.__log.error('Error rc1!=0 (%s, %s, %s)' % (rc1, tx1, cmd1))
                return False
        
            # show out-file
            cmd1 = 'ls -lGgha ' + self.__tarfile
            (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
            self.__log.info('-- done: %s' % tx1[12:].strip())
        
            return True
        except :
            self.__log.error(str(formatExceptionInfo()))
            return False

    def __packFilesStep2(self):
        """ runs after the VM is restartet,
            tar-file is stored in self.__tarfile
            will now evtl. encrypted and/or uploaded
        """
        try :
            cmd1 = ''
            txt1 = '+- '
            targetfile = os.path.join(self.__targetfolder, self.__filestem)
            if not isinstance(self.__enaencryptfile, type(None)):
                txt1 += 'encrypting'
                pack1 = ''
                if self.__packbackup == True: # no compression by gpg, if its done by tar
                    pack1 = '-z 0'
                cmd1 += 'gpg --batch --no-tty --no-use-agent --passphrase-file %s %s ' % \
                          (self.__enaencryptfile, pack1)
                # if targetfile is local, the out-file is set
                targetfile += '.gpg'
                if isinstance(self.__targetserver, type(None)): 
                    cmd1 += '-o %s' % targetfile
                else :
                    cmd1 += '-o -'
                cmd1 += ' -c %s' % self.__tarfile

            # upload
            if not isinstance(self.__targetserver, type(None)):
                if not isinstance(self.__enaencryptfile, type(None)):
                    txt1 += '+ upload'
                else :
                    txt1 += 'upload'
                
                fname = self.__tarfile
                if len(cmd1) > 0: # if using gpg, we use pipe as in-file
                    cmd1 += ' | '
                    fname = '-'
                cmd1 += 'curl --upload-file %s --insecure --user %s %s://%s%s' % \
                          (fname, self.__targetserverlogin, self.__targetserverprotocol, \
                           self.__targetserver, targetfile)

            txt1 += '...'
            self.__log.info(txt1)
        
            # show tar-file
            cmd2 = 'ls -lGgha ' + self.__tarfile
            (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd2)
            self.__log.info('|-  +  %s' % tx1[12:].strip())
        
            # targetfile
            if isinstance(self.__targetserver, type(None)):
                self.__log.info('|- --> %s' % targetfile)
            else :
                self.__log.info('|- --> %s://%s%s' % (self.__targetserverprotocol, self.__targetserver, targetfile))
        
            # run action
            (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
            if stat1 == False:
                self.__log.error('Error rc1!=0 (%s, %s, %s)' % (rc1, tx1, cmd1))
                return False
        except :
            self.__log.error(str(formatExceptionInfo()))
            return False

    def __packOnTheFly(self, packdateien, filenumber=None):
        """ stores files from origin-place and creates backup-file,
            packdateien = ['</path/to/file>', ...]
            filenumber = current number of out-file
        """
        self.__log.info('+- saving files')
        try :
            # show file list
            for i in packdateien:
                cmd2 = 'ls -lGgha ' + i
                (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd2)
                self.__log.info('|-  +  %s' % tx1[12:].strip())
              
            # set file counter
            if isinstance(filenumber, type(None)):
                txtcnt = ''
            else :
                txtcnt = '-%02d' % filenumber

            if self.__packbackup == True:
                targetfile = '%s.tar.gz' % self.__getDateFilename(self.__vmname + txtcnt)
            else :
                targetfile = '%s.tar' % self.__getDateFilename(self.__vmname + txtcnt)
              
            if not isinstance(self.__enaencryptfile, type(None)):
                targetfile += '.gpg'

            ziel1 = ''
            if not isinstance(self.__targetserver, type(None)):
                ziel1 = '%s://%s' % (self.__targetserverprotocol.upper(), self.__targetserver)
            ziel1 = '%s%s' % (ziel1, os.path.join(self.__targetfolder, targetfile))
            self.__log.info('|- --> %s' % ziel1)
        
            # create comand chain
            cmd1 = ''
              
            # pack files using TAR to archive
            if self.__packbackup == True:
                cmd1 = 'tar cz'
            else :
                cmd1 = 'tar c'
            # if no encryption or upload: append out-file
            if isinstance(self.__enaencryptfile, type(None)) and \
                isinstance(self.__targetserver, type(None)):
                cmd1 += 'f %s' % os.path.join(self.__targetfolder, targetfile)
            for i in packdateien:
                cmd1 += ' ' + i
              
            # encryption
            if not isinstance(self.__enaencryptfile, type(None)):
                pack1 = ''
                if self.__packbackup == True: # no compression by gpg, if tar already compresses
                    pack1 = '-z 0' 
                cmd1 += '| gpg --batch --no-tty --no-use-agent --passphrase-file %s %s ' % \
                          (self.__enaencryptfile, pack1)
                # if file-target is local, append out-file
                if isinstance(self.__targetserver, type(None)):
                    cmd1 += '-o %s' % os.path.join(self.__targetfolder, targetfile)
                cmd1 += ' -c -' # data input from pipe

            # upload
            if not isinstance(self.__targetserver, type(None)):
                cmd1 += '| curl --upload-file - --insecure --user %s %s://%s%s' % \
                          (self.__targetserverlogin, self.__targetserverprotocol, \
                            self.__targetserver, \
                            os.path.join(self.__targetfolder, targetfile))
            (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
            if stat1 == False:
                self.__log.error('Error rc1!=0 (%s, %s, %s)' % (rc1, tx1, cmd1))
                return False
        except :
            self.__log.error(str(formatExceptionInfo()))
        self.__log.info('-- save files done')

    def __insertFile(self, image_file, part_nr, mountpos, sourcefile, targetfile):
        """ copy a file into the filesystem of a VM,
            - possible only if VM is stopped,
            - fdisk-drive only,
            image_file = volume-file of the VM
            part_nr = No. of partition (results to device name: /dev/nbd0p[1...]),
            mountpos = folder in host filesystem, where the imagefile is mounted,
            sourcefile = file in host filesystem
            targetfile = file in guest filesystem
        """
        self.__log.info('+- insertFile Start')
        disconn_nbd = False
        umount_nbd = False
        try :
            if isinstance(image_file, type('')):
                if not os.path.exists(image_file):
                    raise Exception('file dont exist: %s' % image_file)
            else :
                raise Exception('parameter error: image_file must be filename (is: %s)' % str(image_file))
            if not isinstance(part_nr, type(1)):
                raise Exception('parameter part_nr must be integer (is: %s)' % str(part_nr))
            if not isinstance(sourcefile, type('')):
                raise Exception('parameter error: sourcefile must bei filename (is: %s)' % str(sourcefile))
            if not os.path.exists(sourcefile):
                raise Exception('file dont exist: %s' % image_file)
            if not isinstance(targetfile, type('')):
                raise Exception('parameter error: targetfile must be filename (is: %s)' % str(targetfile))
            if targetfile.startswith('/'):
                raise Exception('filename must be relative (is: %s)' % targetfile)
            self.__log.info('|- parameter ok')
        
            # check if vm is stopped
            if self.__lvirt.isVmAktiv(self.__vmname) == True:
                raise Exception('VM still running - Stop!')
            self.__log.info('|- VM is stopped')
              
            # check if kernel-module 'nbd' is already loaded
            cmd1 = 'lsmod'
            (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
            if stat1 == False:
                ft1 = 'Error rc1!=0 (%s, %s, %s)' % (rc1, tx1, cmd1)
                raise Exception(ft1)
            if not 'nbd' in tx1:
                # load module 'nbd'
                cmd1 = 'modprobe nbd'
                (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
                if stat1 == False:
                    ft1 = 'Error rc1!=0 (%s, %s, %s)' % (rc1, tx1, cmd1)
                    raise Exception(ft1)
                self.__log.info("Module 'nbd' loaded")

            nbd_devname = ''
            # trying to connect max 4x nbd-device names
            for k in range(4):
                nbd_devname = '/dev/nbd%d' % k

                # access volume-file using 'nbd'
                cmd1 = 'qemu-nbd --connect=%s %s' % (nbd_devname, image_file)
                (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
                if stat1 == False:
                    self.__log.warning('|- Error to connect %s' % nbd_devname)
                    self.__disconnNbdImage(nbd_devname)
                    continue
                else :
                    self.__log.info("|- volume-file connected: '%s' --> '%s'" % (image_file, nbd_devname))
                    disconn_nbd = True

                # mounten
                cmd1 = 'mount %sp%d %s' % (nbd_devname, part_nr, mountpos)
                (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
                if stat1 == False:
                    self.__log.warning('Error when mounting: %sp%d --> %s' % \
                                      (nbd_devname, part_nr, mountpos))
                    self.__disconnNbdImage(nbd_devname)
                    disconn_nbd = False
                    continue
                else :
                    self.__log.info('|- device mounted: %sp%d --> %s' % (nbd_devname, part_nr, mountpos))
                    umount_nbd = True
                    break
        
            if disconn_nbd == False:
                raise Exception('Error rc1!=0 (%s, %s, %s)' % (rc1, tx1, cmd1))
              
            # copy file
            fn1 = os.path.join(mountpos, targetfile)
            self.__log.info('|- copying %s --> %s' % (sourcefile, fn1))
            cmd1 = 'cp %s %s' % (sourcefile, fn1)
            (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
            if stat1 == False:
                ft1 = 'Error rc1!=0 (%s, %s, %s)' % (rc1, tx1, cmd1)
                raise Exception(ft1)
            self.__log.info('|- successful copied')
        except :
            self.__log.error(str(formatExceptionInfo()))
    
        try :
            # unmount
            if umount_nbd == True:
                cmd1 = 'umount %s' % mountpos
                (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
                if stat1 == False:
                    ft1 = 'Error rc1!=0 (%s, %s, %s)' % (rc1, tx1, cmd1)
                    raise Exception(ft1)
        except :
            self.__log.error(str(formatExceptionInfo()))
          
        try :
            # disconnect volume-file
            if disconn_nbd == True:
                self.__disconnNbdImage(nbd_devname)
        except :
            self.__log.error(str(formatExceptionInfo()))
        self.__log.info('-- insertFile done')    
    
    def __disconnNbdImage(self, devname):
        """ disconnects qemu-imagefile
        """
        try :
            cmd1 = 'qemu-nbd -d %s' % devname
            (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
            if stat1 == False:
                self.__log.warning('Error rc1!=0 (%s, %s, %s)' % (rc1, tx1, cmd1))
            else :
                self.__log.info('QEMU-NBD-Device %s unmounted' % devname)
        except :
            self.__log.error(str(formatExceptionInfo()))
      
    def runBackup(self):
        """ proccess backup
        """
        try :
            # show message
            self.__log.info('+- Backup of VM %s' % self.__vmname)

            # show file sizes
            self.__log.info('+- volume files to save:')
            for i in self.__filelst:
                cmd1 = 'ls -lGgha ' + os.path.join(self.__vmfolder, i)
                (stat1, tx1, rc1) = self.__cmd.runShellCmd(cmd1)
                self.__log.info('|- %s' % tx1[12:].strip())
                if stat1 == False:
                    return
      
            # instance must be running
            try :
                if self.__lvirt.isVmActive(self.__vmname) == True:
                    self.__log.info('+- State of instance %s: active, stopping...' % (self.__vmname))
                else :
                    self.__log.info('+- Instance not running - Stop')
                    rungo = False
                    return
            except :
                self.__log.error(str(formatExceptionInfo()))
                return
 
            bkgo = True
            delfiles = []
    
            # stop VM
            shtdncnt = 1
            if self.__multishutdown == True:
                shtdncnt = 3  # fire shutdown command 3x
            try :
                if self.__lvirt.stopVm(self.__vmname, cmdcnt=shtdncnt) == False:
                    bkgo = False
                    self.__log.warning("|- VM '%s' not stopped" % self.__vmname)
            except :
                self.__log.error(str(formatExceptionInfo()))
                bkgo = False
            time.sleep(2)
      
            # list of files to store
            packfiles = []
            for i in self.__filelst:
                packfiles.append(os.path.join(self.__vmfolder, i))
            separatfiles = []
            for i in self.__filelst_separat:
                separatfiles.append(os.path.join(self.__vmfolder, i))      

            # export VM-xml
            fn1 = os.path.join(self.__tempfolder, '%s.xml' % self.__vmname)
            delfiles.append(fn1)
            packfiles.append(fn1)
      
            try :
                fhdl = file(fn1, 'w')
                fhdl.write(self.__lvirt.getDomainXML(self.__vmname))
                fhdl.close()
                self.__log.info('+- VM-XML exported %s' % fn1)
            except :
                self.__log.error(str(formatExceptionInfo()))
                bkgo = False
      
            # export snapshots
            try :
                snaplst = self.__lvirt.getListOfSnapshots(self.__vmname)
            except :
                self.__log.error(str(formatExceptionInfo()))
                snaplst = []
        
            if len(snaplst) > 0:
                for i in snaplst:
                    fn1 = os.path.join(self.__tempfolder, '%s-snapshot-%s.xml' % (self.__vmname, i))
                    delfiles.append(fn1)
                    packfiles.append(fn1)
              
                    # export snapshot
                    fhdl = file(fn1, 'w')
                    try :
                        fhdl.write(self.__lvirt.getSnapshotXML(self.__vmname, i))
                        self.__log.info('+- VM-Snapshot-XML exported %s' % fn1)
                    except :
                        self.__log.error('Error: %s' % str(formatExceptionInfo()))
                        bkgo = False
                    fhdl.close()
    
            time.sleep(8)

            # XML-files are ready to backup
            # choose backup strategy
            if bkgo == True:
                if self.__workonthefly == True:
                    # pack files and store at target place
                    p_lst = []
                    for i in packfiles:
                        if not i in separatfiles:
                            p_lst.append(i)
                    fcnt = 0
                    if len(separatfiles) == 0:
                        self.__packOnTheFly(p_lst)
                    else :
                        self.__packOnTheFly(p_lst, fcnt)
                        fcnt += 1
                    # store files which must be proccessed separate
                    for i in separatfiles:
                        self.__packOnTheFly([i], fcnt)
                        fcnt += 1
                else :
                    # classic method - using temp-directory
                    self.__packFilesStep1(packfiles)
            else :
                self.__log.info("|- backup not active!")

            # write a file to volume file
            if isinstance(self.__insertfilepara, type({})):
                self.__insertFile(image_file=self.__insertfilepara['image_file'], \
                    part_nr=self.__insertfilepara['part_nr'], \
                    mountpos=self.__insertfilepara['mountpos'], \
                    sourcefile=self.__insertfilepara['sourcefile'], \
                    targetfile=self.__insertfilepara['targetfile'])
        
            # restart VM
            self.__log.info('+- starting VM %s...' % self.__vmname)
            try :
                self.__lvirt.startVm(self.__vmname)
            except :
                self.__log.error('Error: %s' % str(formatExceptionInfo()))
                bkgo = False
    
            if (not isinstance(self.__enaencryptfile, type(None))) and \
                (self.__workonthefly == False):
                self.__log.info('-- VM %s started (wait %s seconds)' % (self.__vmname, self.waitsec))
                time.sleep(self.waitsec)
            else :
                self.__log.info('-- VM %s started' % self.__vmname)

            # encrypting
            if self.__workonthefly == False:
                if bkgo == True:
                    if (not isinstance(self.__enaencryptfile, type(None))) or \
                        (not isinstance(self.__targetserver, type(None))):
                        self.__packFilesStep2()
                        delfiles.append(self.__tarfile)

            # delete temp-files
            self.__log.info('+- delete temp-file')
            for i in delfiles:
                self.__log.info('|- %s' % i)
                os.remove(i)
            self.__log.info('-- delete temp-files done')
            self.__log.info('+- backup of VM %s done' % self.__vmname)
        except :
            self.__log.error(str(formatExceptionInfo()))

# end TarGpgBackup
