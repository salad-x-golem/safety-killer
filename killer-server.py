import psutil

STARTS_WITH = ["yagna", "ya-provider"]


for proc in psutil.process_iter():
    # check whether the process name matches
    for prefix in STARTS_WITH:
        if proc.name().startswith(prefix):
            print("Killing {}".format(proc.name()))
            proc.kill()

