from app import schemas
import pytest
def test_get_posts(authorized_client,test_posts):
    res=authorized_client.get("/posts")

    def validate(post):
        return schemas.PostVotes(**post)

    posts_map = map(validate,res.json())   
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_posts(client,test_posts):    
    res = client.get("/posts")
    assert res.status_code == 401

def test_unauthorized_user_get_post(client,test_posts):    
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/888")
    assert res.status_code == 404

def test_authorized_user_get_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")   
    post = schemas.PostVotes(**res.json())
    print(post)
    assert post.Post.id == test_posts[0].id

@pytest.mark.parametrize("title,content,published",[
    ("Awesome new title","awesome new content",True),
    ("Barrchef","We connect Bachelors to Chefs",True),
    ("Remote","We are our brothers keepers",False),
])
def test_create_post(authorized_client,test_user,test_posts,title,content,published):
    res = authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
    created_post = schemas.PostRespone(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_published_is_true(authorized_client,test_user,test_posts):
    res = authorized_client.post("/posts/",json={"title":"The Title","content":"The Content"})
    created_post = schemas.PostRespone(**res.json())
    assert res.status_code == 201
    assert created_post.title == "The Title"
    assert created_post.content == "The Content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client,test_user,test_posts):    
    res = client.post("/posts/",json={"title":"The Title","content":"The Content"})
    assert res.status_code == 401
