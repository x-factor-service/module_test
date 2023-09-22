import pandas as pd

def seperateTable(df) :
    # disk 테이블
    # create_disk_df(df)
    one_to_one(df)
    one_to_many(df)

def one_to_one(df) :
    df_computer_info = df[['computer_id', 'computer_name', 'os_platform', 'is_virtual', 
                        'chassis_type', 'cpu_details_system_type', 'manufacturer', 'collection_date']]
    df_session_ip = df[['computer_id', 'session_ip']]
    df_ad_query = df[['computer_id','last_logged_in_user', 'ad_query_-_last_logged_in_user_date',
                      'ad_query_-_last_logged_in_user_name', 'ad_query_-_last_logged_in_user_time']]
    df_installed_applications = df[['computer_id', 'installed_applications_name', 'installed_applications_version',
                                    'installed_applications_silent_uninstall_string', 'installed_applications_uninstallable',
                                    'collection_date']]
    df_open_shared_details = df[['computer_id', 'open_ssh_name', 'open_ssh_path', 'open_ssh_status',
                                 'open_ssh_type','open_ssh_permissions','collection_date']]
    df_cpu_info = df[['computer_id', 'cpu_details_cpu', 'cpu_details_cpu_speed',
                      'cpu_details_total_physical_processors', 'cpu_details_total_logical_processors',
                      'cpu_details_total_cores', 'cpu_consumption', 'collection_date']]
    df_listen_port = df[['computer_id', 'listen_port_process', 'listen_port_name', 'listen_port_local_port',
                         'collection_date']]
    df_memory_info = df[['computer_id', 'used_memory', 'total_memory', 'collection_date']]
    df_running_process_service = df[['computer_id', 'running_processes', 'running_service', 'collection_date']]
    df_personal_device_info = df[['computer_id', 'last_reboot', 'tanium_client_ip_address', 'tanium_client_nat_ip_address',
                                  'tanium_client_subnet', 'last_system_crash', 'primary_owner_name', 'uptime',
                                  'usb_write_protected', 'nvidia-smi_#1', 'online', 'wired/wireless', 'listen_port_count',
                                  'established_port_count', 'collection_date']]
    df_open_port = df[['computer_id', 'open_port', 'collection_date']]
    df_ip_address = df[['computer_id', 'ip_address', 'collection_date']]
    df_mac_address = df[['computer_id', 'mac_address', 'collection_date']]
    
    return [df_computer_info, df_session_ip, df_ad_query, df_installed_applications, df_open_shared_details, df_cpu_info, 
            df_listen_port, df_memory_info, df_running_process_service, df_personal_device_info, df_open_port, df_ip_address, df_mac_address]

def extract_data(df):
    
    return ''

def one_to_many(df):
    extract_data()
    print(df['disk_free_space'])
    print("+++++++++++++++++++++++++++")
    print(df['disk_used_space'])
    print("+++++++++++++++++++++++++++")
    print(df['disk_total_space'])
    df_disk_info = ''
    df_high_process = ''

def create_disk_df(df):
    location_list = []
    size_gb_list = []
    computer_id_list = [] # 컴퓨터 ID를 저장할 리스트
    classification_list = [] # 분류(used/total)를 저장할 리스트

    computer_ids = df['cid'] # 새롭게 추가: ComputerID 컬럼
    total_disk = df['disk_total_space']
    used_disk = df['disk_used_space']
    

    for comp_id, i, j in zip(computer_ids, total_disk, used_disk):
        if not isinstance(i, list):
            i = [i]
        if not isinstance(j, list):
            j = [j]
        
        for total, used in zip(i, j):
            location_total, byte_in_total = total.split(":")
            location_used, byte_in_used = used.split(":")
            
            if location_total.strip() != location_used.strip():
                print(f"Error: Mismatch in locations {location_total} and {location_used}")
                continue
            
            # used 정보 추가
            computer_id_list.append(comp_id)
            classification_list.append('used')
            location_list.append(location_used.strip())
            size_gb_list.append(convert_to_gb(byte_in_used.strip()))

            # total 정보 추가
            computer_id_list.append(comp_id)
            classification_list.append('total')
            location_list.append(location_total.strip())
            size_gb_list.append(convert_to_gb(byte_in_total.strip()))

    new_df = pd.DataFrame({
        'ComputerID': computer_id_list,
        'Classfication': classification_list,
        'Location': location_list,
        'Size_GB': size_gb_list
    })
    print(new_df)

    return new_df

import re
def convert_to_gb(size_str):
    match = re.match(r"([0-9.]+)\s*([A-Za-z]*)", size_str)
    if match:
        size_val, size_unit = match.groups()
        size_val = float(size_val)
    else:
        print(f"Unknown format: {size_str}")
        return None
    
    size_unit = size_unit.upper()

    # 단위에 따른 변환
    if size_unit == "TB" or size_unit == "T":
        size_val = size_val * 1024
    elif size_unit == "MB" or size_unit == "M":
        size_val = size_val / 1024
    elif size_unit == "KB" or size_unit == "K":
        size_val = size_val / (1024*1024)
    elif size_unit == "G" or size_unit == "GB":
        pass  # 이미 GB 단위
    else:
        print(f"Unknown unit: {size_unit}")
        return None  # 알 수 없는 단위

    return size_val