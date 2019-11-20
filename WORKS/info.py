import psutil

file_read_temp = open("/sys/class/thermal/thermal_zone0/temp", "r")
temp = file_read_temp.readline ()

cpu_temp =int(temp)/1000

# gives a single float value
cpu_percent=psutil.cpu_percent()

# gives an object with many fields
memory=psutil.virtual_memory().percent
# you can convert that object to a dictionary
print(cpu_percent)
print("********")
print(memory)
print("********")
print(str(cpu_temp))
