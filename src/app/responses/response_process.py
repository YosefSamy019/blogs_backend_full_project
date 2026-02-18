from fastapi import HTTPException, status

from src.shared.either import Right, Left
from src.shared.env import Env

from src.data.failure import Failure

from src.app.responses.response import *


class ResponseProcess:
    def __init__(self, env: Env):
        self.env = env

    def process(self, obj: object):

        if isinstance(obj, Right):
            return self.process(obj.value)

        elif isinstance(obj, Left):
            return self.process(obj.value)

        elif isinstance(obj, Failure):
            raise HTTPException(
                status_code=obj.error_code,
                detail=obj.error_msg,
            )

        elif isinstance(obj, BaseResponseModel):
            return obj

        else:
            return self._get_unhandled_exception(obj)

    def _get_unhandled_exception(self, obj: object) -> HTTPException:
        if self.env.is_debug():
            return_msg = f"Return model is not encapsulated, type: {type(obj)}"
        else:
            return_msg = "Return model is not encapsulated"

        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=return_msg,
        )
