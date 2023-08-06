#!/usr/bin/python

from mdsbackuplib import TarGpgBackup


if __name__ == '__main__':
    # example
    ob1 = TarGpgBackup(vmname='name-der-vm', \
                       targfoldr='/path/to/targetfolder',\
                       vmfoldr='/path/to/vm-volumes', \
                       filelist=['volumefile1','volumefile2',...],\
                       tempfolder='/path/to/tempfolder',\
                       targetserver='sftp-server:port',\
                       targetserverlogin='user:password',\
                       packbackup=False,\
                       encryptfile='/path/to/backup.secret',\
                       logfile='/path/to/backup.log')
    if ob1.paraCheck():
        ob1.runBackup()
    del ob1
