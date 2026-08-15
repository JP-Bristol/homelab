#!/bin/bash
find /mnt/backup -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;
