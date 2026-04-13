from fastapi import FastAPI
from fastapi_cloud_cli.commands import login
import Controllers.AppointmentController as Ac

app = FastAPI()

app.include_router(Ac.router)