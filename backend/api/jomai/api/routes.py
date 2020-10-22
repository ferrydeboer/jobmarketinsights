from fastapi import APIRouter

from jomai.api import jobs

router = APIRouter()
router.include_router(jobs.router,
                      prefix="/jobs",
                      tags=["jobs"])
