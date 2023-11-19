from pydantic import BaseModel, Field, ConfigDict


class ToDoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(..., min_length=2, max_length=25)
    description: str | None = None


class ToDoRead(ToDoBase):
    id: int


class ToDoCreate(ToDoBase):
    pass


class ToDoUpdate(ToDoBase):
    title: str | None = Field(None, min_length=2, max_length=25)
