from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

app.config['SESSION_COOKIE_SECURE'] = True  # Only if ALB is using HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
