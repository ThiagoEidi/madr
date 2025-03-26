from ninja import NinjaAPI, Schema
from madr.routers.contas.api import router as contas_router
from madr.routers.livros.api import router as livros_router
from madr.routers.romancistas.api import router as romancistas_router


api = NinjaAPI(csrf=True)

api.add_router('/contas', contas_router)
api.add_router('/livros', livros_router)
api.add_router('/romancistas', romancistas_router)
