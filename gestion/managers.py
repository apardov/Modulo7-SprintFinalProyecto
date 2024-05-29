from django.contrib.auth.base_user import BaseUserManager


class CustomEmailUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        # si no ingresa un correo le indica que es debe ingresar uno
        if not email:
            raise ValueError('Debe ingresar un correo electronico')
        # normalize convierte el email a minusculas si es que el usuario lo ingresa con alguna mayuscula
        email = self.normalize_email(email)
        # en base al modelos que estoy trabajando obtengo la informacion del email y los argumentos
        # adiconales que vengan
        user = self.model(email=email, **extra_fields)
        # hago un hash de la password entregada en los argumentos de forma segura para encriptarla
        user.set_password(password)
        # guardo el usuario en la base de datos
        user.save()
        # retorno el usuario por si lo necesito para alguna accion adicional
        return user

    def create_superuser(self, email, password, **extra_fields):
        # en base a los argumentos extra_fields utilizo el metodo setdefault para generar estos atributos por
        # por defecto en caso de generar un superuser y tenga los permisos necesarios
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # verifica que en los extra_fields se envie que is_staff y is_superuser esten en True
        # en caso contrario envia una excepcion adecuada para cada caso
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El super usuario debe pertenecer al staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El super usuario debe pertenecer a superuser')

        # utiliza el metodo creado anteriromente pero con los extras de este suoper usuario y luego hace todo
        # el proceso de guardado en la bd
        return self.create_user(email, password, **extra_fields)
