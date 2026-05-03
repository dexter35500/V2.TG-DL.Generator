class FIleNotFound(Exception):
    """Excepción lanzada cuando el archivo no existe en Telegram."""
    def __init__(self, message="Archivo no encontrado."):
        self.message = message
        super().__init__(self.message)

class InvalidHash(Exception):
    """Excepción lanzada cuando el hash de seguridad no coincide."""
    def __init__(self, message="Hash inválido o vencido."):
        self.message = message
        super().__init__(self.message)