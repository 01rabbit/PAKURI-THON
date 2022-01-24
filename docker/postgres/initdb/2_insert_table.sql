INSERT INTO t_command_list (cmd_name,value,cmd_type,description) VALUES
    ('Ping_scan','nmap -sn','nmap','Perform ping scan (scan by ICMP) (-sn). No port scan is performed'),
    ('Quick_scan','nmap -T4 -F','nmap','Perform a fast scan with fewer target ports than usual (-F)'),
    ('Nikto_to_http','nikto -h http://','nikto','Perform Nikto scan for http (80 by default)
    e.g nikto -h http://<Target> or nikto -h http://<Target>:[Port]'),
    ('Nikto_to_https','nikto -h https://','nikto','Perform Nikto scan (443 by default) for https'),
    ('TCP_Top_1000','nmap -sC -sV -v','nmap','nmap TCP top port 1000'),
    ('UDP_Top_100','nmap -sU --top-ports 100 -v','nmap','nmap UDP top port 100'),
    ('All_TCP_Ports','nmap -sC -sV -n -sT -O -v -p-','nmap','nmap All TCP ports'),
    ('Intense_Scan','nmap -T4 -A -v','nmap','Speed up scan timing (-T4), enable OS detection, version detection, script scanning, traceroute (-A), and display detailed information (-v)'),
    ('Intense_scan_plus_UDP','nmap -sS -sU -T4 -A -v ','nmap','In addition to Intense scan, do SYN scan (-sS) and UDP scan (-sU)'),
    ('Intense_scan_all_TCP_ports','nmap -p 1-65535 -T4 -A -v','nmap','Perform Intense scan, but scan for all TCP ports (-p 1-65535)'),
    ('Intense_scan_no_ping','nmap -T4 -A -v -Pn','nmap','Perform Intense scan without ping (-Pn)'),
    ('Quick_scan_plus','nmap -sV -T4 -O -F --version-light','nmap','Do a fast scan, but also detect the OS (-O) and look at the service version for open ports (-sV , --version-light)'),
    ('Quick_Traceroute','nmap -sn --traceroute','nmap','Do a ping scan (-sn) with traceroute included (--traceroute) (normal ping scans do not use traceroute)'),
    ('Regular_scan','nmap','nmap','Normal Nmap scan. Run a regular Nmap against the target.'),
    ('Slow_comprehensive_scan','nmap -sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 --script "default or (discovery and safe)"','nmap','Perform a slow but extensive scan. Specifically.
    Perform a SYN scan (-sS) and a UDP scan (-sU).
    Speed up the scan timing (-T4)
    Enable OS detection, version detection, script scanning, and traceroute (-A)
    Improve the display of detailed information (-v)
    Perform detection using ICMP Echo request (-PE)
    Perform detection using ICMP timestamp request (-PP)
    Specify the port for SYN scan (-PS80, 443)
    Specifies the port for ACK scan (-PA3389).
    Specify the port for UDP scan (-PU40125).
    Perform SCTP scan (-PY)
    Specify the source port (-g 53)
    Specify the source port (-g 53) Execute scripts belonging to the default category or the discovery and safe categories.
    Execute scripts belonging to the default category or the discovery and safe categories (--script default or (discovery and safe))');