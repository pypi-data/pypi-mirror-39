
from . import manager

Manager = manager.Manager

# Create a defaults
manager = Manager()

# Shortcut to default methods
get_path = manager.get_path  # deprecated
is_downloaded = manager.is_downloaded  # deprecated
get = manager.get
isdownloaded = manager.isdownloaded

# DEPRECATED Only to keep compatibility with version 1
LATEST = "master"

