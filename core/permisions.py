from typing import Literal, Optional
from models.role import ActionEnum, LevelEnum, RoleElementAccess, Role, UserRole
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from sqlalchemy import select, and_
from models.resourse import ResourseElement

Action = Literal["create", "read", "update", "delete"]
_level_rank = {LevelEnum.none: 0,
               LevelEnum.own: 1,
               LevelEnum.all: 2}


def _to_action(action: Action) -> ActionEnum:
    try:
        return ActionEnum(action)
    except Exception:
        raise HTTPException(status_code=400, detail="Неверное действие")


async def get_effective_level(db: AsyncSession, user: User, element_name: str, action: Action) -> LevelEnum:
    if not user or not user.is_active:
        return LevelEnum.none

    elem_id = await db.scalar(select(ResourseElement.id).where(ResourseElement.name == element_name))

    if elem_id is None:
        return LevelEnum.none

    action_enum = _to_action(action)

    q = (
        select(RoleElementAccess.level)
        .join(UserRole, UserRole.role_id == RoleElementAccess.role_id)
        .join(ResourseElement, ResourseElement.id == RoleElementAccess.element_id)
        .where(and_(UserRole.user_id == user.id,
                    ResourseElement.id == elem_id,
                    RoleElementAccess.action == action_enum)
               )
    )
    rows = (await db.scalars(q)).all()
    if not rows:
        return LevelEnum.none
    return max(rows, key=lambda lv: _level_rank[lv])


async def has_read_all(db: AsyncSession, user: User, element_name: str) -> bool:
    return await get_effective_level(db, user, element_name, "read") == LevelEnum.all


async def check_permission(
        db: AsyncSession,
        user: User,
        element_name: str,
        action: Action,
        object_owner_id: Optional[int] = None,
) -> None:
    if action == "create":
        return

    lvl = await get_effective_level(db, user, element_name, action)
    if lvl == LevelEnum.none:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    if object_owner_id is None:
        raise HTTPException(status_code=400, detail="No recourse owner")

    if lvl == LevelEnum.all:
        return

    if lvl == LevelEnum.own and object_owner_id == user.id:
        return

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
