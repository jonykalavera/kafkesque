from ninja import NinjaAPI
from consumers.api import router as consumers_router

api = NinjaAPI(title="Kafkesque")

api.add_router("/consumers/", consumers_router)
