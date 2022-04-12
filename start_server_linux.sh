#!/bin/sh
/bin/sh -ec 'python server.py &'
/bin/sh -ec 'python catch_phishing.py'