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
 
