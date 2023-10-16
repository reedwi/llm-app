from app.core.logger import setup_applevel_logger
logger = setup_applevel_logger()
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Header, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.models.supa import SupaChatbotTrainingHook, SupaPersonalChatbotHook
import json
from typing import Optional
from app.utils.process_training import process_training_request, do_something, personal_process_training_request, personal_process_training_request_dev
import os


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_STR}/openapi.json"
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



@app.post('/start-task')
async def start_task(supa_webhook: SupaChatbotTrainingHook, request: Request):
    # task = process_training_request.apply_async(args=[supa_webhook.dict()])
    authorization = request.headers.get('Authorization')
    if not authorization or authorization != os.getenv('SUPABASE_AUTH'):
        raise HTTPException(status_code=401, detail="Unauthorized")
    logger.debug(f'START_TASK: Webhhok received: {supa_webhook}')

    supa_dict = supa_webhook.dict()
    supa_dict['schema'] = supa_dict['schema_name']
    del supa_dict['schema_name']
    if supa_webhook.record['status'] == 'READY':
        task = process_training_request.delay(supa_dict)
    else:
        task = do_something.delay()

    try:
        task_id = str(task.id)
    except:
        task_id = None

    return {"task_id": task_id}

@app.post('/personal-start-task')
async def personal_start_task(supa_webhook: SupaPersonalChatbotHook, request: Request):
    authorization = request.headers.get('Authorization')
    logger.debug('PERSONAL_START_TASK: In the personal-start-task route')
    if not authorization or authorization != os.getenv('SUPABASE_AUTH'):
        raise HTTPException(status_code=401, detail="Unauthorized")
    logger.debug(f'PERSONAL_START_TASK: Webhhok received: {supa_webhook}')
    supa_dict = supa_webhook.dict()
    supa_dict['schema'] = supa_dict['schema_name']
    del supa_dict['schema_name']
    if supa_webhook.record['status'] == 'READY':
        task = personal_process_training_request.delay(supa_dict)

    try:
        task_id = str(task.id)
    except:
        task_id = None

    return {"task_id": task_id}

@app.post('/personal-start-task-dev')
async def personal_start_task_dev(supa_webhook: SupaPersonalChatbotHook, request: Request):
    authorization = request.headers.get('Authorization')
    logger.debug('PERSONAL_START_TASK_DEV: In the personal-start-task route')
    if not authorization or authorization != os.getenv('SUPABASE_AUTH'):
        raise HTTPException(status_code=401, detail="Unauthorized")
    logger.debug(f'PERSONAL_START_TASK_DEV: Webhhok received: {supa_webhook}')
    supa_dict = supa_webhook.dict()
    supa_dict['schema'] = supa_dict['schema_name']
    del supa_dict['schema_name']
    if supa_webhook.record['status'] == 'READY':
        task = personal_process_training_request_dev.delay(supa_dict)

    try:
        task_id = str(task.id)
    except:
        task_id = None

    return {"task_id": task_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)