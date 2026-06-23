import asyncio
import sys

from fastapi import FastAPI
import Controllers.AppointmentController as Ac
import Controllers.DoctorController as Dc
import Controllers.SpecialityController as Sc
import Controllers.RoomController as Rc
import Controllers.ClinicController as Cc
import Controllers.TreatmentController as Tc
import Controllers.ScheduleController as Scc

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()

app.include_router(Ac.router)
app.include_router(Dc.router)
app.include_router(Sc.router)
app.include_router(Rc.router)
app.include_router(Cc.router)
app.include_router(Tc.router)
app.include_router(Scc.router)

@app.get("/ping")
def ping():
    return {"status": "ok"}