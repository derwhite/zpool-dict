import json
import subprocess


def get_zpool():
    zpool = subprocess.run(
        "/sbin/zpool status", check=True, shell=True, stdout=subprocess.PIPE, universal_newlines=True, text=True
    )
    return zpool.stdout.split("\n")


def fake_zpool():
    with open("out.txt", "r") as f:
        return f.readlines()


def parse_text_to_dict(text):
    data = {}
    current_key = None
    current_value = None
    lines = text
    for line in lines:
        if ":" in line:
            if current_key:
                data[current_key.strip()] = current_value.strip()
            current_key, current_value = line.split(":", 1)
        else:
            current_value += "\n" + line.strip()
    if current_key:
        data[current_key.strip()] = current_value.strip()
    return data


def remove_empty_lines(strings_list):
    return [line for line in strings_list if line.strip()]


def parse_storage_info(storage_info_str, poolname):
    storage_info = {}
    current_pool = None

    lines = storage_info_str
    for line in lines[1:]:
        tokens = line.split()
        if tokens[0] == poolname:
            current_pool = tokens[0]
            storage_info[current_pool] = {}
            status = tokens[1]
            read = int(tokens[2])
            write = int(tokens[3])
            checksum = int(tokens[4])
            storage_info[current_pool] = {
                "Status": status,
                "Read": read,
                "Write": write,
                "Checksum": checksum,
            }
        elif "raidz" in tokens[0]:
            current_raid = tokens[0]
            storage_info[current_pool][current_raid] = {}
            status = tokens[1]
            read = int(tokens[2])
            write = int(tokens[3])
            checksum = int(tokens[4])
            storage_info[current_pool][current_raid] = {
                "Status": status,
                "Read": read,
                "Write": write,
                "Checksum": checksum,
            }
        else:
            disk_id = tokens[0]
            status = tokens[1]
            read = int(tokens[2])
            write = int(tokens[3])
            checksum = int(tokens[4])

            storage_info[current_pool][current_raid][disk_id] = {
                "Status": status,
                "Read": read,
                "Write": write,
                "Checksum": checksum,
            }

    return storage_info


def get_zpool_dict():
    pool_text = get_zpool()
    pool_status = parse_text_to_dict(pool_text)
    pool_status["config"] = remove_empty_lines(pool_status["config"].split("\n"))
    pool_status["action"] = remove_empty_lines(pool_status["action"].split("\n"))
    pool_status["status"] = remove_empty_lines(pool_status["status"].split("\n"))
    pool_status["config"] = parse_storage_info(pool_status["config"], pool_status["pool"])
    return pool_status


def main():
    test = get_zpool_dict()
    print(json.dumps(test, indent=4))


if __name__ == "__main__":
    main()
