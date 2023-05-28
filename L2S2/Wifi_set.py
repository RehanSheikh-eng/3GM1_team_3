from L2S2 import boot_L2S2,spiToL2S2

boot_L2S2()

#Set WiFI name and password
payload_set_wifi = bytearray('AndroidAP|wtdm1984'.encode("utf-8"))
L2S2.spiToL2S2(5, payload_set_wifi)


