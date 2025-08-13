from fastapi import status, APIRouter, Depends
from src.models.post import posts

from src.services.post import PostService
from src.security import login_required

from src.schemas.post import PostIn, PostUpdateIn
from src.views.post import PostOut
from src.database import database


router = APIRouter(prefix="/posts", dependencies=[Depends(login_required)])
service = PostService()


@router.get("/", response_model=list[PostOut])
async def read_posts(
    published: bool,
    limit: int,
    skip: int = 0
):
    return await service.read_all(published=published, limit=limit, skip=skip)


@router.get("/{id}", response_model=PostOut)
async def read_post(id: int):
    return await service.read(id)
    # query = posts.select().where(posts.c.id == post_id)
    # result = await database.fetch_one(query)
    
    # if result is None:
    #     raise HTTPException(status_code=404, detail="Nenhuma postagem encontrada!")
    # return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(post: PostIn):
    return {**post.model_dump(), "id": await service.create(post)}
    # command = posts.insert().values(
    #     title=post.title,
    #     content=post.content,
    #     published_at=post.published_at,
    #     published=post.published
    # )
    # last_id = await database.execute(command)
    # return {**post.model_dump(), "id": last_id}


@router.patch("/{id}", response_model=PostOut)
async def update_post(id: int, post: PostUpdateIn):
    return await service.update(id=id, post=post)
    # has_post = await read_post(post_id)
    
    # if has_post is None:
    #     raise HTTPException(status_code=404, detail="Nenhuma postagem encontrada!")
    
    # update_data = post.model_dump(exclude_unset=True)  # pega só campos enviados
    
    # if update_data is None:
    #     raise HTTPException(status_code=404, detail="Nenhum dado para atualizar!")
    
    # query = posts.update().where(posts.c.id == post_id).values(**update_data)
    
    # await database.execute(query)
    # updated_post = await read_post(post_id)
    # return updated_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_post(id: int):
    await service.delete(id)
    # has_post = await read_post(post.id)
    
    # if has_post is None:
    #     raise HTTPException(status_code=404, detail="Nenhuma postagem encontrada!")
    
    # query = posts.delete().where(posts.c.id == post.id)
    # result = await database.execute(query)
    
    # if result > 0:
    #     return {"message": "Postagem deletada com sucesso!"}
    
    # return {"message": "Não foi possível deletar a postagem!"}