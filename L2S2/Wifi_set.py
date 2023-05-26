from L2S2 import boot_L2S2,spiToL2S2

boot_L2S2()

#Set WiFI name and password
payloadsetwifi = bytearray('Galaxy A51 E473|cqxh1791'.encode("utf-8"))
spiToL2S2(5, payloadsetwifi)


