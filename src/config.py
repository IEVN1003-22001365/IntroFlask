class DevelopmentConfig():
    DEBUG=True
    MYSQL_HOST='localhost'
    MYSQL_USER='israel'
    MYSQL_PASSWORD='root'
    MYSQL_DB='api_utl'
    MYSQL_CURSORCLASS='Cursor'
    MYSQL_PORT = 3306
    
    MYSQL_UNIX_SOCKET = None
    MYSQL_CONNECT_TIMEOUT = None
    MYSQL_READ_DEFAULT_FILE = None
    MYSQL_WRITE_DEFAULT_FILE = None
    MYSQL_CUSTOM_OPTIONS = None
    MYSQL_USE_UNICODE = True
    MYSQL_CLIENT_FLAGS = None

config={
    'development': DevelopmentConfig
}