from fastapi import FastAPI
from fastapi_cloud_cli.commands import login
import Controllers.AppointmentController as Ac
import Controllers.DoctorController as Dc
import Controllers.SpecialityController as Sc
import Controllers.RoomController as Rc
import Controllers.ClinicController as Cc

app = FastAPI()

app.include_router(Ac.router)
app.include_router(Dc.router)
app.include_router(Sc.router)
app.include_router(Rc.router)
app.include_router(Cc.router)