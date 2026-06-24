import asyncio
import sys
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.set_default_executor(ThreadPoolExecutor(max_workers=5000))
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(Ac.router)
app.include_router(Dc.router)
app.include_router(Sc.router)
app.include_router(Rc.router)
app.include_router(Cc.router)
app.include_router(Tc.router)
app.include_router(Scc.router)

@app.get("/ping")
async def ping():
    return {"status": "ok"}