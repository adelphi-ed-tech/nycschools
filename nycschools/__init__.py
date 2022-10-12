import os
import os.path
import json
from types import SimpleNamespace

from platformdirs import PlatformDirs
dirs = PlatformDirs("nycschools", "mxc")

config_file = "nycschools.config"
config_paths = [
    os.path.join(dirs.site_config_dir, config_file),
    os.path.join(dirs.user_config_dir, config_file)
]

data_paths = [
    dirs.site_data_dir,
    dirs.user_data_dir
]



def get_config():

    print("loading config from file system")

    for path in config_paths:
        if os.path.exists(path):
            with open(path,"r") as f:
                config = json.loads(f.read())
                return SimpleNamespace(**config)

    # create a new config in the user space
    path = os.path.join(dirs.user_config_dir, config_file)
    os.makedirs(os.path.dirname(path))
    config = {
        "config_file": path,
        "data_dir": find_data_dir()
    }
    with open(path,"w") as f:
        f.write(json.dumps(config, indent=2))

    return SimpleNamespace(**config)





def find_data_dir():
    """Finds a writeable data directory"""
    for path in data_paths:
        if check_write_edit_delete(path):
            return path
    # raise Exception(f"No valid data dir found in: {data_paths}")
    return None




def check_write_edit_delete(path):
    """Checks if path can be a suitable data dir"""

    print("Checking data dir at:", path)
    if os.path.exists(path):
        files = os.listdir(path)
        if len(files) > 0:
            # if the path exists and is not empty, assume it works
            return True
    else:
        try:
            print("trying to make", path)
            os.makedirs(path)
        except:
            return False


    f = os.path.join(path, ".temp")
    msg = "testing data dir"
    with open(f, "w") as temp:
        try:
            temp.write(msg)
        except:
            return False

    with open(f, "r") as temp:
        try:
            assert temp.read() == msg
        except:
            return False

    with open(f, "a") as temp:
        try:
            temp.write("\nmore data")
        except:
            return False
    try:
        os.remove(f)
    except:
        return False

    return True



config = get_config()
