from django.apps import AppConfig

class CursosConfig(AppConfig):
    name = 'cursos'
    verbose_name = 'Aplicacion de los cursos'

    def ready(self):
        import cursos.signals