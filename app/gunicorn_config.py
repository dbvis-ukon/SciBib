import os

pidfile = "scibib.pid"
worker_tmp_dir = "/dev/shm"
worker_class = "gthread"
workers = 2
worker_connections = 1000
timeout = 30
keepalive = 2
threads = 4
proc_name = "scibib"
bind = "{0}:8080".format(os.getenv('SCIBIB_BIND_ADDRESS', '0.0.0.0'))
backlog = 2048
accesslog = "-"
errorlog = "-"
user = "www-data"
group = "www-data"
