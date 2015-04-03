#!/bin/bash

# Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

pip install --upgrade -r /opt/iris/requirements.txt

cp /opt/iris/build-scripts/viewpoint.conf /etc/httpd/conf.d

chmod 600 /opt/iris/config/*
chown -R apache:apache /opt/iris/config
chown -R apache:apache /var/log/httpd
