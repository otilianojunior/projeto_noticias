from app.config import settings
from fastapi import APIRouter, status, Response
from server.consultas.noticias.Noticias import NoticiasConsulta
from server.model.params.BasicParamConsulta import BasicParamConsulta


noticias = APIRouter()


@noticias.post(settings.API_V1 + "diarias", status_code=status.HTTP_200_OK)
async def Noticias(params: BasicParamConsulta):
    try:
        consulta = NoticiasConsulta(params.url)
        return consulta.noticias()
    except Exception as ex:
        print(ex)
        return Response(status_code=500)
