# -*- coding: utf-8 -*-
import os

from django.conf import settings as s

# Pathes
VAR_DIR = os.path.join(s.BASE_DIR, "var")
VAR_LOCK_DIR = os.path.join(VAR_DIR, "lock")
VAR_LOG_DIR = os.path.join(VAR_DIR, "log")
TMP_DIR = os.path.join(VAR_DIR, "tmp")

BACKUP_DIR = os.path.join(VAR_DIR, "backup")
DB_BACKUP_DIR = os.path.join(BACKUP_DIR, "db")
