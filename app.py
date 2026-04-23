from fastapi import FastAPI
from fastapi_cloud_cli.commands import login
import Controllers.AppointmentController as Ac
import Controllers.DoctorController as Dc
import Controllers.SpecialityController as Sc
import Controllers.RoomController as Rc
import Controllers.ClinicController as Cc
import Controllers.TreatmentController as Tc
import Controllers.ScheduleController as Scc
import mock

app = FastAPI()

app.include_router(Ac.router)
app.include_router(Dc.router)
app.include_router(Sc.router)
app.include_router(Rc.router)
app.include_router(Cc.router)
app.include_router(Tc.router)
app.include_router(Scc.router)

mock.generate_mock_data()