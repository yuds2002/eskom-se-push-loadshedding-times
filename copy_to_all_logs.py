log = open("log.txt","r")
log_lines = log.readlines()

all_logs = open("all_logs.txt", "a")
all_logs.writelines(log_lines)

log.close()
all_logs.close()

