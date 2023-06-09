'''
FOR PYTHON (TO BE RUN ON LAPTOP)
'''

from datetime import datetime, timedelta
import requests
import inspect
from pprint import pprint

# CUED dev server
API_URI = 'https://apicued.l2s2.com/internalapi'
API_KEY = 'mb6AXX2bjzva7urembLZTkWwGFHPQcZi'
test_plate_template_name = 'Raw Medical'        # E.g. 'Key Plate'
_record_id = 57     # Tony Stark



_cert = None
test_patient_username = 'TestPatient'
test_patient_password = 'Escape78BrightLight'

_user_api_key = API_KEY
_key_plate_template_id = None
_key_plate_data_id = None
_user_id = None
LONG_TIME_EPOCH: datetime = datetime(1800, 1, 1)


def get_api_key_header(api_key):
    return {'Authorization': f'X-API-KEY {api_key}'}



def from_long_time(long_date_time: int) -> datetime:
    return LONG_TIME_EPOCH + timedelta(seconds=long_date_time)


def to_long_time(date_time: datetime) -> int:
    return int((date_time - LONG_TIME_EPOCH).total_seconds())


def print_status(resp) -> bool:
    if resp.status_code == 200: return False

    print(f"{inspect.stack()[1][0].f_code.co_name}  Status={resp.status_code}  Reason={resp.reason}")

    return True


def record_read(record_id):
    resp = requests.get(f'{API_URI}/record/read?record_id={record_id}',
                        headers=get_api_key_header(API_KEY),
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    pprint(response_json)

    
def record_search():
    filters = [
            {'operator': 1, 'property': 'Surname', 'value': 'Stark'}
        ]

    resp = requests.post(f'{API_URI}/record/search',
                        json={'filters': filters},
                        headers=get_api_key_header(API_KEY),
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    pprint(response_json)


def record_search2():
    filters = [
            #{'operator': 1, 'property': '__ExternalStatus', 'value': '2'}
            {'operator': 1, 'property': 'RecordId', 'value': _record_id}
        ]

    resp = requests.post(f'{API_URI}/record/search',
                        json={'filters': filters},
                        headers=get_api_key_header(API_KEY),
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    pprint(response_json)

    
def record_update():
    payload = {'id': _record_id,
               'custom2': "Boo!"}

    resp = requests.post(f'{API_URI}/record/update',
                        json={'record': payload, 'ignore_conflicts': True},
                        headers=get_api_key_header(API_KEY),
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    pprint(response_json)    

    
def data_create(record_id, template_id, control_values: list):
    payload = {'record_id': record_id,
               'plate_template_id': template_id,
               'control_values': control_values}

    resp = requests.post(f'{API_URI}/data/create',
                        json={'data': payload, 'ignore_conflicts': True},
                        headers=get_api_key_header(_user_api_key),
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    status = response_json['PlateDataCreateResult']['status']

    print(f"data_create Status={status}")

    if status != 0:
        pprint(response_json['PlateDataCreateResult'], width=120)


def data_read_newest(record_id, template_id, track_id):
    resp = requests.get(f'{API_URI}/data/read/newest?record_id={record_id}&plate_id={template_id}&track_id={track_id}',
                        headers=get_api_key_header(_user_api_key),
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    pprint(response_json, width=120)


def data_read(record_id, plate_data_id):
    resp = requests.get(f'{API_URI}/data/read/id?record_id={record_id}&plate_data_id={plate_data_id}',
                        headers=get_api_key_header(_user_api_key),
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    pprint(response_json, width=180)


def template_read_full(plate_template_name, version):
    resp = requests.get(f'{API_URI}/template/read/full?plate_name={plate_template_name}&version={version}',
                        headers=get_api_key_header(_user_api_key),
                        cert=_cert)
    
    if print_status(resp): return

    response_json = resp.json()

    #pprint(response_json, width=120)

    pprint(response_json['PlateTemplateReadByIdNameVersionResult']['plate_template']['controls'], width=120)

    return response_json['PlateTemplateReadByIdNameVersionResult']['plate_template']


def template_read_active_full(plate_template_name):
    resp = requests.get(f'{API_URI}/template/read/active/full?plate_name={plate_template_name}',
                        headers=get_api_key_header(_user_api_key),
                        cert=_cert)
    
    if print_status(resp): return

    response_json = resp.json()

    status = response_json['PlateTemplateReadActiveByIdNameResult']['status']

    if status != 0: 
        print(f"Failed, status={status}")
        return

    #pprint(response_json['PlateTemplateReadActiveByIdNameResult']['plate_template']['controls'], width=160)
    # pprint(response_json['PlateTemplateReadActiveByIdNameResult']['plate_template'], width=160)

    return response_json['PlateTemplateReadActiveByIdNameResult']['plate_template']


def template_list_active():
    resp = requests.get(f'{API_URI}/template/list/active',
                        headers=get_api_key_header(_user_api_key),
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    pprint(response_json['PlateTemplateReadAllActiveResult'], width=120)




def file_create(file_content, content_type):
    headers = get_api_key_header(_user_api_key)
    headers['Content-Type'] = content_type

    resp = requests.post(f'{API_URI}/file/create',
                        #files={'file': file_content},  # Can't currently use multipart file encoding
                        data=file_content,
                        headers=headers,
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    return response_json['FileCreateResult']['file_id']
    

def user_authenticate(username, password):

    resp = requests.get(f'{API_URI}/user/authenticate?user_name={username}&password={password}',
                        headers=get_api_key_header(API_KEY),
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    status = response_json['UserAuthenticateResult']['status']
    print(f"UserAuthenticate Status={status}")

    if status != 0: return

    # pprint(response_json['UserAuthenticateResult'])

    global _user_api_key
    _user_api_key = response_json['UserAuthenticateResult']['api_key']

    global _key_plate_template_id
    _key_plate_template_id = response_json['UserAuthenticateResult']['key_plate_template_id']

    global _key_plate_data_id
    _key_plate_data_id = response_json['UserAuthenticateResult']['key_plate_data_id']

    global _record_id
    _record_id = response_json['UserAuthenticateResult']['record_id']

    global _user_id
    _user_id = response_json['UserAuthenticateResult']['user_id']

    #print(f'User API Key = {_user_api_key}')


def user_update_set_password(user_id, password):
    payload = {'id': user_id,
               'password': password}

    resp = requests.post(f'{API_URI}/internal/user/update',
                        headers=get_api_key_header(API_KEY),
                        json={'user': payload},
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    status = response_json['UserUpdateResult']['status']
    print(f"UserUpdate Status={status}")

    if status != 0: return

    pprint(response_json['UserUpdateResult'])



def user_change_password(user_id, old_password, new_password):
    payload = {'user_id': user_id,
               'old_password': old_password,
               'new_password': new_password}

    resp = requests.post(f'{API_URI}/user/change_password',
                        headers=get_api_key_header(_user_api_key),
                        json=payload,
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    status = response_json['UserChangePasswordResult']['status']
    print(f"ChangePassword Status={status}")

    if status != 0: return

    pprint(response_json['UserChangePasswordResult'])


def user_read(user_id):
    resp = requests.get(f'{API_URI}/internal/user/read?user_id={user_id}',
                        headers=get_api_key_header(API_KEY),
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    status = response_json['UserReadResult']['status']
    #print(f"UserRead Status={status}")

    if status != 0: return

    pprint(response_json['UserReadResult'])


def user_read_for_portal_record(record_id):
    resp = requests.get(f'{API_URI}/internal/user/read/portal_record?record_id={record_id}',
                        headers=get_api_key_header(API_KEY),
                        cert=_cert)

    if print_status(resp): return

    response_json = resp.json()

    status = response_json['UserReadForPortalRecordResult']['status']
    print(f"UserReadForPortalRecord Status={status}")

    if status != 0: return

    pprint(response_json['UserReadForPortalRecordResult'])


#template_list_active()
GPS_longitude = 69 # Test data
record_id = "110" # Patient: Minnie Mouse
plate_template_id = "6e0485b5-cd17-4438-aff8-afe0578ed71f" # Plate: Group_3_Production
control_id = [{'name' : 'GPSLongitude', 'value' : str(GPS_longitude)}]
data_create(record_id, plate_template_id, control_id)

# record_search()

# Commented-out parts below will need to be modified to run OK....

# template = template_read_active_full(test_plate_template_name)
# # pprint(template)
# template_id = template["id"]

# with open('C:\Temp\somefile.json', 'rb') as content_file:
#     content = content_file.read()

#     file_key = file_create(content, 'application/octet-stream')

#     print(f'File key = {file_key}')

# values = [
#         {'name': 'Date1', 'value': to_long_time(datetime.now())},
#         {'name': 'Time1', 'value': to_long_time(datetime.now())},

#         {'name': 'Status', 'value': 'x42'},
#         # {'name': 'flowrate', 'value': ??},
#         # {'name': 'mass', 'value': ??},
#         # {'name': 'turbidity', 'value': ??},
#         # {'name': 'urinecolour', 'value': ??},

#         {'name': 'FileUpload1', 'value': 'somefile.json', 'attachments': [{'description': 'Some description', 'key': file_key, 'original_file_name': 'somefile.json', 'saved_date_time': to_long_time(datetime(2018, 3, 7))}]},
#     ]
# data_create(_record_id, template_id, values)

# data_read_newest(_record_id, template_id, "")

