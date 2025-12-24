from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from database.model import Snippet

async def get_snippets_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Snippet).where(Snippet.user_id == user_id))
    return result.scalars().all()

async def get_snippet_by_name(db: AsyncSession, user_id: int, name: str):
    result = await db.execute(
        select(Snippet).where(Snippet.user_id == user_id, Snippet.name == name)
    )
    return result.scalar_one_or_none()

async def create_snippet(db: AsyncSession, user_id: int, name: str, content: str):
    snippet = Snippet(user_id=user_id, name=name, content=content)
    db.add(snippet)
    await db.commit()
    await db.refresh(snippet)
    return snippet

async def delete_snippet_by_name(db: AsyncSession, user_id: int, name: str):
    await db.execute(
        delete(Snippet).where(Snippet.user_id == user_id, Snippet.name == name)
    )
    await db.commit()