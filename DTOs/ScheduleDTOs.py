from pydantic import BaseModel, field_validator
from datetime import date, time
from typing import Optional

class CreateScheduleRegularDTO(BaseModel):
    doctor_id: int
    start_date: date
    weekday: int
    time_from: Optional[time] = None  # none means day off
    time_to: Optional[time] = None
    room_id: Optional[int] = None

    @field_validator('weekday')
    @classmethod
    def weekday_must_be_valid(cls, v):
        if not 1 <= v <= 7:
            raise ValueError('weekday must be between 1 and 7')
        return v

    @field_validator('time_to')
    @classmethod
    def time_to_must_be_after_time_from(cls, v, info):
        if 'time_from' in info.data and v <= info.data['time_from']:
            raise ValueError('time_from must be before time_to')
        return v

class CreateScheduleModificationDTO(BaseModel):
    doctor_id: int
    date: date
    time_from: Optional[time] = None  # none means day off
    time_to: Optional[time] = None
    room_id: Optional[int] = None

    @field_validator('time_to')
    @classmethod
    def time_to_must_be_after_time_from(cls, v, info):
        if 'time_from' in info.data and v <= info.data['time_from']:
            raise ValueError('time_from must be before time_to')
        return v