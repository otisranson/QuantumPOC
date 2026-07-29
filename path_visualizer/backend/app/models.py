# Copyright 2026 Otis Ranson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Pydantic request/response schemas for the field API."""

from typing import Annotated

from pydantic import BaseModel, Field

from app.path_integral import HBAR_MAX, HBAR_MIN, NUM_PATHS_MAX, NUM_PATHS_MIN

Coord = Annotated[float, Field(ge=-1.0, le=1.0)]
Point = Annotated[list[Coord], Field(min_length=2, max_length=2)]
Hbar = Annotated[float, Field(ge=HBAR_MIN, le=HBAR_MAX)]


class FieldRequest(BaseModel):
    start: Point
    end: Point
    num_paths: Annotated[int, Field(ge=NUM_PATHS_MIN, le=NUM_PATHS_MAX)]
    hbar: Hbar


class LearnedRequest(BaseModel):
    start: Point
    end: Point
    hbar: Hbar


class FieldResponse(BaseModel):
    field: list[list[float]]
    grid_size: int
