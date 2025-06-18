from fastapi import APIRouter, HTTPException, Query
from tortoise.exceptions import DoesNotExist

from core.pagination import PaginatedResult
from .schemas import UserOut, UserIn
from db.models.user_model import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
async def create_user(data: UserIn):
    existing = await User.get_or_none(external_id=data.external_id)
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")
    user = await User.create(**data.model_dump())
    return user


@router.get("/{external_id}", response_model=UserOut)
async def get_user_by_external_id(external_id: str):
    user = await User.get_or_none(external_id=external_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=PaginatedResult[UserOut])
async def list_users(page: int = Query(1, ge=1), rows: int = Query(20, ge=1, le=100)):
    total = await User.all().count()
    offset = (page - 1) * rows
    users = await User.all().order_by("-created_at").offset(offset).limit(rows)
    users_resp = [UserOut.model_validate(u) for u in users]
    return PaginatedResult[UserOut](total=total, rows=rows, page=page, items=users_resp)
