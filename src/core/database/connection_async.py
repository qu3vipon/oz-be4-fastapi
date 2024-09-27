from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "mysql+aiomysql://root:ozcoding@127.0.0.1:3306/ozcoding"

async_engine = create_async_engine(DATABASE_URL)
AsyncSessionFactory = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=async_engine
)

async def get_async_db():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()
