import motor.motor_asyncio
from decouple import config

MONGO_URL = config("MONGO_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.school_blog
blog_collection = database.get_collection("blogs")
