from ninja import NinjaAPI, Schema
from madr.routers.contas.api import router as contas_router
from madr.routers.livros.api import router as livros_router
from madr.routers.romancistas.api import router as romancistas_router
from madr.routers.auths.api import router as auth_router
from madr.routers.auths.schemas import InvalidToken



api = NinjaAPI(csrf=True)

api.add_router('/contas', contas_router)
api.add_router('/livros', livros_router)
api.add_router('/romancistas', romancistas_router)
api.add_router('/auth', auth_router)



@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    __import__('ipdb').set_trace()
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)