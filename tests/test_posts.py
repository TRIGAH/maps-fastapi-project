from app import schemas
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

def test_create_post(authorized_client,test_user,test_posts):

