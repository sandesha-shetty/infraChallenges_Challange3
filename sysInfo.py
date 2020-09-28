# Submitted by Sandesha Shetty
# import the required modules to get the required information
import cpuinfo
import psutil
import json

# JSON initial structure to which the data will be appended
systemInfo = [{"CPUs": [], "Memory":[], "Storage":[], "Network":[]}]


cpuInformationObject = {}
# Get CPU related information
cpuInformationObject["Description"] = cpuinfo.get_cpu_info()["brand_raw"]
# Get Number of cores
cpuInformationObject["NumberOfCores"] = psutil.cpu_count(logical=False)
# Append to JSON
systemInfo[0]["CPUs"].append(cpuInformationObject)

memoryInformationObject = {}
memInfo = psutil.virtual_memory()
# Get Installed RAM in bytes and converted to GB
memoryInformationObject["InstalledGB"] = round(
    (memInfo.total / (1024 ** 3)), 2)
# Get Available RAM in bytes and converted to GB
memoryInformationObject["AvailableGB"] = round(
    (memInfo.available / (1024 ** 3)), 2)
# Append the information to JSON
systemInfo[0]["Memory"].append(memoryInformationObject)

partitions = psutil.disk_partitions()
# Get Each storage related information of the device
for partition in partitions:
    try:
        storgeInformationObject = {}
        storgeInformationObject["Description"] = partition.device
        partition_usage = psutil.disk_usage(partition.mountpoint)
        storgeInformationObject["CapacityGB"] = round(
            (partition_usage.total / (1024 ** 3)), 2)
        storgeInformationObject["AvailableGB"] = round(
            (partition_usage.free / (1024 ** 3)), 2)
        storgeInformationObject["Type"] = partition.fstype
        systemInfo[0]["Storage"].append(storgeInformationObject)
    except PermissionError:
        continue

# Get Each Network related information of the device
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        if str(address.family) == 'AddressFamily.AF_INET' and address.netmask != 'None':
            networkInformationObject = {}
            networkInformationObject["Description"] = interface_name
            networkInformationObject["IP"] = address.address
            networkInformationObject["Netmask"] = address.netmask
            systemInfo[0]["Network"].append(networkInformationObject)

jsonResult = json.dumps(systemInfo)
print(jsonResult)
