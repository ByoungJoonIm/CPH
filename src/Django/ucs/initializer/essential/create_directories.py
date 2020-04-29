import os

assignment_cache_path = os.path.join(os.path.expanduser('~'), "assignment_cache")

if not os.path.exists(assignment_cache_path):
    os.mkdir(assignment_cache_path)
