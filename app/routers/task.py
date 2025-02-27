from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete


router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    query = select(Task)
    result = db.execute(query)
    tasks = result.scalars().all()
    return tasks


@router.get('/task_id')
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    query = select(Task).where(Task.id == task_id)
    task = db.execute(query).scalar()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')
    else:
        return task


@router.post('/create')
async def create_task(task_create: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    username_exist = db.execute(select(User).where(User.id == user_id)).scalar()
    if username_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    query = insert(Task).values(
        title=task_create.title,
        content=task_create.content,
        priority=task_create.priority,
        completed=False,
        user_id=user_id,
    )
    db.execute(query)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_task(task_id: int, task_update: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    task_exist = db.execute(select(Task).where(Task.id == task_id)).scalar()
    if task_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')
    query = update(Task).where(Task.id == task_id).values(**task_update.dict())
    db.execute(query)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.delete('/delete')
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task_exist = db.execute(select(Task).where(Task.id == task_id)).scalar()
    if task_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')
    query = delete(Task).where(Task.id == task_id)
    db.execute(query)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
