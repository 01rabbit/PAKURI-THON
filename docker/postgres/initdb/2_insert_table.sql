INSERT INTO t_command_list (cmd_name,display_name,value,cmd_type,description) VALUES
    ('Ping_scan','Ping Scan','nmap -sn','nmap','Perform ping scan (scan by ICMP) (-sn). No port scan is performed'),
    ('Quick_scan','Quick Scan','nmap -T4 -F','nmap','Perform a fast scan with fewer target ports than usual (-F)'),
    ('Nikto_to_http','Nikto to http','nikto -h http://','nikto','Perform Nikto scan for http (80 by default)
    e.g nikto -h http://<Target> or nikto -h http://<Target>:[Port]'),
    ('Nikto_to_https','Nikto to https','nikto -h https://','nikto','Perform Nikto scan (443 by default) for https'),
    ('TCP_Top_1000','TCP Top 1000','nmap -sC -sV -v','nmap','nmap TCP top port 1000'),
    ('UDP_Top_100','UDP Top 100','nmap -sU --top-ports 100 -v','nmap','nmap UDP top port 100'),
    ('All_TCP_Ports','All TCP Port','nmap -sC -sV -n -sT -O -v -p-','nmap','nmap All TCP ports'),
    ('Intense_Scan','Intense Scan','nmap -T4 -A -v','nmap','Speed up scan timing (-T4), enable OS detection, version detection, script scanning, traceroute (-A), and display detailed information (-v)'),
    ('Intense_scan_plus_UDP','Intense scan + UDP','nmap -sS -sU -T4 -A -v ','nmap','In addition to Intense scan, do SYN scan (-sS) and UDP scan (-sU)'),
    ('Intense_scan_all_TCP_ports','Intense scan all TCP ports','nmap -p 1-65535 -T4 -A -v','nmap','Perform Intense scan, but scan for all TCP ports (-p 1-65535)'),
    ('Intense_scan_no_ping','Intense scan no ping','nmap -T4 -A -v -Pn','nmap','Perform Intense scan without ping (-Pn)'),
    ('Quick_scan_plus','Quick scan +','nmap -sV -T4 -O -F --version-light','nmap','Do a fast scan, but also detect the OS (-O) and look at the service version for open ports (-sV , --version-light)'),
    ('Quick_Traceroute','Quick Traceroute','nmap -sn --traceroute','nmap','Do a ping scan (-sn) with traceroute included (--traceroute) (normal ping scans do not use traceroute)'),
    ('Regular_scan','Regular scan','nmap','nmap','Normal Nmap scan. Run a regular Nmap against the target.'),
    ('Vuln_scan','Vuln scan', 'nmap -Pn -sV --script vuln', 'nmap', 'Use Nmap''s script to probe for vulnerabilities.'),
    ('Vuln_scan_All_TCP','Vuln scan All TCP', 'nmap -Pn -sV -p- --script vuln', 'nmap', 'Use Nmap''s script to probe for vulnerabilities. All TCP Ports.'),
    ('AutoRecon','Autorecon','python3 ~/PAKURI-THON/tools/AutoRecon/autorecon.py --output tmp/ --only-scans-dir --no-port-dir','tools','Automatically perform recon on a target');