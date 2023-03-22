from datetime import datetime
from server.consultas.Abstract.AbstractConsultas import AbstractConsultas


class NoticiasConsulta(AbstractConsultas):
    def __init__(self, url):
        super().__init__(url)
        self.url = url

    def noticias(self):
        try:
            response = self.get_noticia()
            return response
        except Exception as ex:
            print(ex)
            raise Exception

    def get_noticia(self):
        try:
            self.download_and_parse()
            noticia = {
                'data_hora_consulta': datetime.now(),
                'titulo': self.get_title(),
                'data_publicacao': self.get_publish_date(),
                'autores': self.get_authors(),
                'texto': self.get_text()
            }
            return noticia
        except Exception:
            raise Exception
