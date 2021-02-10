import os
import re
from ftplib import FTP
import ftplib
import zipfile
from ftplib import FTP_TLS
import threading
import signal
from datetime import datetime, timedelta
#from concurrent.futures import TimeoutError
import socket
from contextlib import contextmanager
from google.cloud import storage
import sys

lista_timeouts=[]

now =datetime.now()
job=""
dia=now.strftime("_%d_%m_%Y")

carga=job+dia

#variaveis que sao usadas na funcao file_exists
bucket_name = ''
prefix = ''

dt_dia_anterior=now - timedelta(days=1)
dt_hist_dia=dt_dia_anterior.strftime("%Y_%-m") #formato ex:2020_5

def raise_timeout(signum, frame):
    raise TimeoutError
    
@contextmanager
def timeout(time,arquivo):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except Exception as e:
        print("erro timeout",arquivo)
        lista_timeouts.append(arquivo)
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)

def downloadFile(filename):
    with timeout(30,filename):

        ftp.set_debuglevel(2)
        sock = ftp.transfercmd('RETR ' + filename)
        def background():
            f = open("ftp/"+filename,"wb")
            while True:
                block = sock.recv(1024*1024)
                if not block:
                    break
                f.write(block)
                
            sock.close()
            print("Downloaded " + filename)
        t = threading.Thread(target=background)
        t.start()
        while t.is_alive():
            t.join(60)
            ftp.voidcmd('NOOP') 
            
def _download_ftp_file(ftp_handle, name, dest, overwrite):
    
    """ downloads a single file from an ftp server """
    #_make_parent_dir(dest.lstrip("/"))
    if not os.path.exists(dest) or overwrite is True:
        try:
            #print("RETR {0}".format(name))
            with open("ftp/"+dest, 'wb') as f:
                try:
                    ftp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 75)
                    ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
                    #ftp.set_debuglevel(2)
                    with timeout(20,dest):
                        
                        ftp_handle.retrbinary("RETR {0}".format(name), f.write)
                except Exception as e:
                    print("deu ruim aqui em retrbinary",e)
                #print(ftp_handle.set_debuglevel(2))
            print("download: {0}".format(dest))
        except FileNotFoundError:
            print("FAILED: {0}".format(dest))
    else:
        print("already exists: {0}".format(dest))

def DownloadAllFiles_old(lista):
    #lista_timeouts=[]
    

    for i in lista:
        
        ftp =FTP(mysite)
        ftp.login(username,password)
        ftp.set_pasv(False)
        if i[0] =="/":



            _download_ftp_file(ftp,i[1:],i,True)


        else:


            _download_ftp_file(ftp,i,i,True)


def DownloadAllFiles(lista):
    #lista_timeouts=[]
    for i in lista:
        ftp =FTP(mysite)
        ftp.login(username,password)
        ftp.set_pasv(False)
        if i[0] =="/":
            downloadFile(i[1:])
        else:
            downloadFile(i)
            
def file_exists(bucket_name, prefix, file):
    
    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(
        bucket_name, prefix=prefix, delimiter=None
    )
    
    stats = False #Variavel que vai dizer se o arquivo ja existe no bucket
    for blob in blobs:
        if file in blob.name:
            stats = True 
            break
    return stats

if __name__ == "__main__":


    os.system("mkdir ftp/")
    #os.system("mkdir ftp/historico/")
    os.system("mkdir ftp/geral/")
    os.system("mkdir ftp/duplicatas/")
    os.system("mkdir ftp/comissao/")
    os.system("mkdir ftp/historico_diario/")

    mysite = ""
    username = ""
    password = ""
    ftp =FTP(mysite,timeout=240)
    ftp.connect(mysite,port=21)
    ftp.login(username,password)
    ftp.set_pasv(False)
    

    files_aux= ftp.nlst("file_*.zip".format(dt_hist_dia)) #arquivos hist_estoque_*_*.zip
    stats = True
    for i in files_aux:
        if not(file_exists(bucket_name,prefix,i[1:])):
               stats = False

    if not stats:#Se o arquivo nao existir no bucket executa o download dos arquivos
        lista_tabela_faixa_comissao = ftp.nlst('file_*.zip')  #arquivotabela_tx_comissao_frn_*.zip


        DownloadAllFiles(lista_geral)

        if len(lista_timeouts)>0:
            print("fazendo upload novamente dos arquivos que deu timeout")
            DownloadAllFiles(lista_timeouts)


        os.system("gsutil -m cp -r ftp gs://{bucket}/{}".format(carga))
    else:
        sys.exit('Nao ha novos arquivos no FTP')
