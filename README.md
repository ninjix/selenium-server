Selenium Server
===============

Selenium is an automated web application testing system. This set of scripts, files and instructions provide the tools necessary to setup a headless test server on CentOS 6.5 server. All browser tests are performed using the Xvfb display server. 

## Installation 

Make yourself root.

```bash
sudo bash
```

Install the IUS Community Project repo

```bash
rpm -Uvh http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/epel-release-6-5.noarch.rpm
yum -y update
```

Install required packages.

```bash
yum -y install firefox Xvfb libXfont Xorg jre
```

Create a user account named *selenium* to run the services. 

```bash
useradd selenium
```

Create a directory where Selenium will live.

```bash
mkdir -p /opt/selenium
```

Download the latest version of the Selenium 

```bash
cd /opt/selenium
wget http://selenium-release.storage.googleapis.com/2.43/selenium-server-standalone-2.43.1.jar
```

Copy the init scripts to the /etc/init.d directory.

```bash
cp centos/initd/* /etc/init.d/
```

Set the Selenium and Xvfb daemons to start on boot.

```bash
chkconfig --add seleniumd
chkconfig --add xvfbd
chkconfig seleniumd on
chkconfig xvfbd on
```

Start the services.

```bash
service seleniumd start
service xvfbd start
```

## Setup Log Rotation

Copy the logrotate configuration files to the /etc/logroate.d directory.

```bash
cp centos/logrotate.d/* /etc/logrotate.d/
```

## Firewall Configuration

You'll need to modify the CentOS firewall to accept connections on port 4444.

Insert this into the /etc/sysconfig/iptables file.

```
-A INPUT -m state --state NEW -m tcp -p tcp --dport 4444 -j ACCEPT
```

Add this line before the INPUT -j REJECT statements.

Here's a working example:

```
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 4444 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
COMMIT
```

## Testing (Optional)

Here is a quick way to test if the system is working correctly using Python.

```bash
yum -y python-pip
python-pip install -U selenium
```

Create a file named *test_selenium.py* and add the following lines of code.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Quick test of the headless Selenium server """

from selenium import webdriver

browser = webdriver.Remote(
    command_executor='http://127.0.0.1:4444/wd/hub',
    desired_capabilities={
        'browserName': 'firefox'
        }
)
browser.get('http://python.org')
browser.save_screenshot('test.png')
browser.quit()
```
 
Start a tail of the /var/log/selenium/selenium.log file.

```bash
tail -f /var/log/selenium/selenium.log
```

Now execute the script and you should see test.png screenshot file appear as output. The Selenium log should show the job request without errors.

```bash
python test_selenium.py
```
