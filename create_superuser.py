import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TallerMecanico.settings')
django.setup()

User = get_user_model()

# Cambia estos valores
USERNAME = 'admin'
EMAIL = 'eymi.casas1336@alumnos.udg.mx'
PASSWORD = '12345'

if not User.objects.filter(username=USERNAME).exists():
    print('⚙️  Creando superusuario...')
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
else:
    print('✅ Superusuario ya existe, no se crea de nuevo.')
