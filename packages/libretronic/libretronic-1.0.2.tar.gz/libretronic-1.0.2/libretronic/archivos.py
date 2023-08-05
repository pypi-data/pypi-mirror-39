
import paramiko

def archivo2folios(ruta,archivo,salida):   
    archivo_salida = salida
    with open(ruta+'\\'+archivo,'r') as inp,open(ruta+'\\'+archivo_salida,'w') as out:        
        datos = inp.readlines()
        i = 1
        for linea in datos:
            if (i != 1) and (i != len(datos) and any(linea)):
                if i != len(datos)-1:
                    out.write(linea)
                else:
                    out.write(linea.strip())
            i+=1
    inp.close()
    out.close()
    return archivo_salida


def subirArchivo(hostname,username,password,file,rutal,rutar):
    local = rutal+"\\"+file
    remoto = rutar+file
    port = 22
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local,remoto)

    finally:
        t.close()

def bajarArchivo(hostname,username,password,file,rutal,rutar):
    local = rutal+"\\"+file
    remoto = rutar+file
    port = 22
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remoto,local)

    finally:
        t.close()        