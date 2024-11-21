from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb+srv://punk:qvJKsKM1hQSWxVzH@cluster0.compr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client["product_database"]
product_collection = database["products"]