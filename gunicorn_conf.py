from multiprocessing import cpu_count

bind = '0.0.0.0:5000'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = 'access_log'
errorlog =  'error_log'
