from subprocess import call
import config

# Get conexion a base de datos
db_url = config.db_url

# Setup versioning para la base de datos
cmd_version = "python db_repository/manage.py version_control --url=" + \
    db_url + " --repository=db_repository"
call(cmd_version, shell=True)

# Crear shortcut para los commands de migrate
cmd_shortcuts = "migrate manage manage.py --repository=db_repository --url=" + \
    db_url
call(cmd_shortcuts, shell=True)
