from pydantic import BaseModel, conint
from datetime import datetime


class SCouponInfo(BaseModel):
    id: int
    code: str
    valid_from: datetime
    valid_to: datetime
    discount: conint(ge=0, le=100)
    active: bool = True
