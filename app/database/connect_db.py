




async def get_session():
    async with session() as new_session:
        yield new_session




