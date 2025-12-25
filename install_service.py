# install_service.py

import os

def install_service():
    working_directory = os.path.dirname(os.path.abspath(__file__))
    service_content = f"""[Unit]
Description=Killer Server Service
After=network.target

[Service]
WorkingDirectory={working_directory}
ExecStart={working_directory}/venv/bin/python -u {working_directory}/killer-server.py
User=ubuntu

# CPU / scheduling priority
Nice=-20
CPUSchedulingPolicy=rr
CPUSchedulingPriority=80

# IO priority
IOSchedulingClass=best-effort
IOSchedulingPriority=7

# Make the process less likely to be OOM-killed
OOMScoreAdjust=-1000

[Install]
WantedBy=multi-user.target
"""
    service_path = '/etc/systemd/system/killer-server.service'
    with open(service_path, 'w') as service_file:
        service_file.write(service_content)
    os.system('systemctl daemon-reload')
    os.system('systemctl enable killer-server.service')
    os.system('systemctl start killer-server.service')
    print("Killer server service installed and started.")

if __name__ == '__main__':
    install_service()