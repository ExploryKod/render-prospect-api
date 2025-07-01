# Configuration Gunicorn pour la production
import multiprocessing
import os

# Nombre de workers (processus)
workers = multiprocessing.cpu_count() * 2 + 1

# Type de workers
worker_class = 'sync'

# Adresse de binding
bind = '0.0.0.0:5000'

# Timeout pour les workers
timeout = 60

# Nombre maximum de requêtes par worker avant redémarrage
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Préchargement de l'application
preload_app = True

# Nombre de threads par worker (si worker_class = 'gthread')
threads = 2

# Configuration pour la sécurité
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuration pour les performances
keepalive = 2
worker_connections = 1000

# Configuration pour le reload automatique (désactivé en production)
reload = False

# Configuration pour les logs
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Configuration pour les timeouts
graceful_timeout = 30
worker_tmp_dir = '/dev/shm'

# Configuration pour les headers
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
} 