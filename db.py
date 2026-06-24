from psycopg2.pool import ThreadedConnectionPool
import itertools
import asyncio

primary_pool = ThreadedConnectionPool(
    minconn=1,
    maxconn=5000,
    database='MedicalApptApp',
    user='zbd-user',
    password='zbd-user',
    host='localhost',
    port=5432
)

# replica_pools = [
#     ThreadedConnectionPool(
#         minconn=1,
#         maxconn=5000,
#         database='MedicalApptApp',
#         user='zbd-user',
#         password='zbd-user',
#         host='localhost',
#         port=port
#     )
#     for port in [5433, 5434]
# ]

# _replica_cycle = itertools.cycle(replica_pools)

def get_write_conn():
    return primary_pool.getconn(), primary_pool

def get_read_conn():
    # pool = next(_replica_cycle)
    # return pool.getconn(), pool
    return None

def release_conn(conn, pool):
    pool.putconn(conn)

async def run_in_threadpool(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)