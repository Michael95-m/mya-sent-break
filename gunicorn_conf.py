bind = '0.0.0.0:5000'
worker_class = 'sync'
loglevel = 'debug'
accesslog = 'logfile'
acceslogformat ="%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog =  'errorlog'