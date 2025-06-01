from fastapi import FastAPI
import asyncio
import time

app = FastAPI()
@app.get("/ancom")
async def an_com():
    print("Dang an com")
    await asyncio.sleep(3)
    print( "An com xong")

@app.get("/docsach")
async def doc_sach():
    print("Dang doc sach")
    await asyncio.sleep(5)
    print( "Doc sach xong")


async def do_rac():
    print("Dang di do rac")
    await asyncio.sleep(4)
    print( "Di do rac xong")

async def running():
    await asyncio.gather(an_com(),doc_sach(),do_rac())

if __name__ == "__main__":
    start = time.time()

    asyncio.run(running())

    end = time.time()
    print('Thời gian chạy: ', end - start)
