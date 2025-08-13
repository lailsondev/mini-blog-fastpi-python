class NotFoundPostError(Exception):
    def __init__(self, message: str = "Postagem não encontrada!") -> None:
        self.message = message