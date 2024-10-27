from fastapi import APIRouter, HTTPException, status
from app.models import BlogPost, UpdateBlogPost
from app.database import blog_collection
from bson import ObjectId

router = APIRouter()

# Helper function to format MongoDB documents
def blog_helper(blog) -> dict:
    return {
        "id": str(blog["_id"]),
        "title": blog["title"],
        "content": blog["content"],
        "author": blog["author"],
        "published": blog["published"],
        "created_at": blog["created_at"]
    }

# Create a new blog post
@router.post("/", response_model=BlogPost)
async def create_blog(blog: BlogPost):
    new_blog = await blog_collection.insert_one(blog.dict())
    created_blog = await blog_collection.find_one({"_id": new_blog.inserted_id})
    return blog_helper(created_blog)

# Read all blog posts
@router.get("/", response_model=list[BlogPost])
async def get_blogs():
    blogs = []
    async for blog in blog_collection.find():
        blogs.append(blog_helper(blog))
    return blogs

# Read a single blog post
@router.get("/{id}", response_model=BlogPost)
async def get_blog(id: str):
    blog = await blog_collection.find_one({"_id": ObjectId(id)})
    if blog:
        return blog_helper(blog)
    raise HTTPException(status_code=404, detail="Blog not found")

# Update a blog post
@router.put("/{id}", response_model=BlogPost)
async def update_blog(id: str, blog: UpdateBlogPost):
    update_data = {k: v for k, v in blog.dict().items() if v is not None}
    result = await blog_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count:
        updated_blog = await blog_collection.find_one({"_id": ObjectId(id)})
        return blog_helper(updated_blog)
    raise HTTPException(status_code=404, detail="Blog not found")

# Delete a blog post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: str):
    result = await blog_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
