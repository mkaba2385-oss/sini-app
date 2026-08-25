from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SeasonBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    year: int = Field(..., ge=2000)
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self) -> "SeasonBase":
        if self.end_date < self.start_date:
            raise ValueError("La date de fin doit être postérieure à la date de début.")
        return self


class SeasonCreate(SeasonBase):
    pass


class SeasonUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    year: int | None = Field(default=None, ge=2000)
    start_date: date | None = None
    end_date: date | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> "SeasonUpdate":
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.end_date < self.start_date
        ):
            raise ValueError("La date de fin doit être postérieure à la date de début.")
        return self


class SeasonResponse(SeasonBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
