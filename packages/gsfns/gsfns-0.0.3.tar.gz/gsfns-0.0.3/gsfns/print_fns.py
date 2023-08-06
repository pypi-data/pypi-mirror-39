import os
import shutil

def print_logs(i_dst_path=None,i_str = None):
    assert i_dst_path is not None
    assert i_str is not None
    if os.path.isfile(i_dst_path):
       dst_path,_ = os.path.split(i_dst_path)
    else:
       dst_path  = i_dst_path
    save_log_path = os.path.join(dst_path,'logs.txt')
    with open(save_log_path,'a+') as file:
        file.write('{}\n'.format(i_str))
    return True

def move_logs(i_dst_path = None,i_dst_name=None):
    assert i_dst_path is not None
    assert i_dst_name is not None
    if os.path.isfile(i_dst_path):
       dest_path,_ = os.path.split(i_dst_path)
    else:
       dest_path  = i_dst_path
    dst_logs = os.path.join(dest_path,i_dst_name)
    src_logs  = os.path.join(os.getcwd(),'Logs.txt')
    shutil.move(src_logs,dst_logs)
    return True

def del_logs(i_dst_full_path = None):
    assert i_dst_full_path is not None
    if os.path.isfile(i_dst_full_path):
        if os.path.exists(i_dst_full_path):
            os.remove(i_dst_full_path)
        else:
            pass
    else:
        raise Exception('Input a path to a file that you want to delete!')
    return True