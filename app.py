from fastapi import FastAPI
from fastapi_cloud_cli.commands import login
import Controllers.AppointmentController as Ac
import Controllers.DoctorController as Dc
import Controllers.SpecialitiesController as Sc

app = FastAPI()

app.include_router(Ac.router)
app.include_router(Dc.router)
app.include_router(Sc.router)