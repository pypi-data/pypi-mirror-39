import ftplib
##function##
def Get(ip,user,pw,dir="",type='.',save=''):
    try:
        ftp=ftplib.FTP(ip,user,pw)
        files=[]
        for name in ftp.nlst(dir):
            if type in name:
                date = ftp.sendcmd('MDTM '+name)
                files.append((name,date.split(" ")[1]))
        if files:
            new_file=((sorted(files,key=lambda f:f[1],reverse=True)[0])[0])
            localfile = open(save+new_file.replace(dir+'/',' '),'wb')
            ftp.retrbinary('RETR ' + new_file, localfile.write, 1024)
            ftp.quit()
            return True
        else:
            ftp.quit()
            return False
    except:
        return False
