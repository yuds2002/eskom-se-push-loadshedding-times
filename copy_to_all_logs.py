log = open("/home/yuds/esp/log.txt","r")
log_lines = log.readlines()

all_logs = open("/home/yuds/esp/all_logs.txt", "a")
all_logs.writelines(log_lines)
all_logs.write("\n")
log.close()
all_logs.close()

