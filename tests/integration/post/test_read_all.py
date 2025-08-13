import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from src.schemas.post import PostIn
    from src.services.post import PostService
    
    service = PostService()
    await service.create(PostIn(title="Post 1", content="Some content", published=True))
    await service.create(PostIn(title="Post 2", content="Some content", published=True))
    await service.create(PostIn(title="Post 3", content="Some content", published=False))
    

@pytest.mark.parametrize("published,total", [(True, 2), (False, 1)])
async def test_read_posts_by_status_success(
    client: AsyncClient,
    access_token: str,
    published: str,
    total: int
):
    params = {"published": published, "limit": 10}
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = await client.get("/posts/", params=params, headers=headers)
    
    content = response.json()
    
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == total
    

async def test_read_posts_limit_success(client: AsyncClient, access_token: str):
    params = {"published": "True", "limit": 1}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/", params=params, headers=headers)
    
    content = response.json()
    
    assert response.status_code == status.HTTP_200_OK
    assert len(content) == 1
    

async def test_read_posts_not_authenticated_fail(client: AsyncClient):
    params = {"published": "on", "limit": 1}

    response = await client.get("/posts/", params=params, headers={})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    

async def test_read_posts_empty_parameters_fail(client: AsyncClient, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/posts/", params={}, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY