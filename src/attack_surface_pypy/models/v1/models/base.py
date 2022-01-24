import pydantic


class BaseModel(pydantic.BaseModel):
    # TODO: why ujson is so slow
    class Config:
        frozen = True

    #     json_dumps = ujson.dumps
    #     json_loads = ujson.loads
