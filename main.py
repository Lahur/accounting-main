from fastapi import FastAPI
from controller.bill_controller import router as bill_router

app = FastAPI()

app.include_router(bill_router)

