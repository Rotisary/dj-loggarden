from typing import Annotated

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from .config.db import get_db
from .config.settings import settings
from . import crud, schemas


app = FastAPI(title="LogGarden Viewer")


@app.get("/logs", response_model=list[schemas.LogEntryResponse])
async def list_logs(
    filters:  Annotated[schemas.LogEntryFilterParams, Depends()],
    limit: Annotated[int, Query()] = settings.DEFAULT_LIMIT,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: Session = Depends(get_db),
):
    limit = min(limit, settings.MAX_LIMIT)
    return crud.get_logs(db, filters.model_dump(exclude_unset=True), limit, offset)



@app.get("/logs/{log_id}", response_model=schemas.LogEntryResponse)
async def get_log(log_id: int, db: Session = Depends(get_db)):
    return crud.get_log_by_id(db, log_id)


@app.get("/stats/levels")
async def level_stats(db: Session = Depends(get_db)):
    return crud.get_level_stats(db)