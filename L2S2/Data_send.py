from L2S2 import boot_L2S2,data_send

boot_L2S2()

_record_id = '126'    # Steve Real Rogers
_plate_id = 'adb357d6-e4f2-4149-8ad1-3ab0702f9822'
_control_id = '25'
_type = 1 #Datatype: 1 = bool; 2 = int; 3 = double; 4 = datetime; 5 = string
_content = False
_units = 'oC'

#data_send(_record_id, _plate_id, _control_id, _type, _content, _units)

_control_id = '3'
_type = 2
_content = 39

#data_send(_record_id, _plate_id, _control_id, _type, _content, _units)

_control_id = '24'
_type = 3
_content = 24.11

#data_send(_record_id, _plate_id, _control_id, _type, _content, _units)

_control_id = '19'
_type = 4
_content = int(123456)

#data_send(_record_id, _plate_id, _control_id, _type, _content, _units)

_control_id = '22'
_type = 5
_content = "test message 8"

#data_send(_record_id, _plate_id, _control_id, _type, _content, _units)