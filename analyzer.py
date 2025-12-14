logs = [
    "LOGIN SUCCESS user=yusuf ip=10.0.0.5",
    "LOGIN FAILED user=root123 ip=10.0.0.8",
    "PORT SCAN DETECTED ip=10.0.0.9",
    "ERROR 404 path=/admin",
    "LOGIN FAILED user=guest45 ip=10.0.0.7",
    "LOGIN FAILED user=mehmet ip=10.0.0.6",
]

users = ["yusuf", "mehmet", "root123", "guest45", "admin", "ayse"]

ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3389]
danger_ports = [21, 23, 25, 110, 135, 139, 445, 3389]

#log kaydından kullanıcı ve ip bilgilerini ayıklama

def logdan_kullanici_ip(log):
    kullanici=None
    ip=None

    parcalar=log.split(" ")

    for p in parcalar:
        if "user=" in p:
            kullanici=p.split("=")[1]
        if "ip=" in p:
            ip=p.split("=")[1]
    return kullanici,ip
#failed logları bulacak
def failed_detaylar(logs):
    bulunan_list=[]
    
    for l in logs:
        if "FAILED" in l:
            kullanici,ip=logdan_kullanici_ip(l)
            #Log formatı bozulursa kullanici adi None kontrolü
            if kullanici is not None and ip is not None:
                bulunan_list.append((kullanici,ip))
    
    return bulunan_list
            
      
#Şüpheli kullanıcıları bulma
def supheli_kullanicilar(users):
    supheli_list=[]
    for user in users:
        for ch in user:
            if ch.isdigit():
                supheli_list.append(user)
                break
    return supheli_list

#Port risk raporu

def port_raporu(ports,danger_ports):
    supheli_ports=[]
    guvenli_ports=[]
    for p in ports:
        if p in danger_ports:
            supheli_ports.append(p)
        else:
            guvenli_ports.append(p)
    
    return {
        "risky":supheli_ports,
        "safe":guvenli_ports
    }

#Yetkili kullanıcı kontrolü
def yetkili_mi(users):
    for user in users:
        if user=="admin" or user=="root":
            return True
        
    return False
   



def main():
    print("=== Seclog Mini Analyzer ===")

    print("\nFAILED girişler:")
    print(failed_detaylar(logs))

    print("\nŞüpheli kullanıcılar:")
    print(supheli_kullanicilar(users))

    print("\nYetkili kullanıcı var mı? (True=Var, False=Yok)")
    print(yetkili_mi(users))

    print("\nRiskli Portlar:")
    rapor=port_raporu(ports,danger_ports)
    print("Riskli:",rapor["risky"])
    print("Güvenli:",rapor["safe"])


if __name__=="__main__":
    main()
