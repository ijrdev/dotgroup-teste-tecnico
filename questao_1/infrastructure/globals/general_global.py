from infrastructure.repositories.livros_repository import LivrosRepository

class GeneralGlobal():
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(GeneralGlobal, cls).__new__(cls)
            
        return cls.instance

    def __init__(self):
        try:
            LivrosRepository().create_table()
        except Exception:
            raise
