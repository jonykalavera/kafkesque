from ninja import NinjaAPI
from consumers.api import router as consumers_router

api = NinjaAPI()

api.add_router("/consumers/", consumers_router)
