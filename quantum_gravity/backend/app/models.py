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

"""Pydantic request/response schemas for the geometry API."""

from typing import Annotated

from pydantic import BaseModel, Field

from app.happy_code import NUM_QUBITS

Strengths = Annotated[
    list[Annotated[float, Field(ge=0, le=1)]],
    Field(min_length=NUM_QUBITS, max_length=NUM_QUBITS),
]


class GeometryRequest(BaseModel):
    strengths: Strengths


class BoundaryNode(BaseModel):
    index: int
    angle: float
    x: float
    y: float
    entropy: float


class BoundaryEdge(BaseModel):
    index: int
    source: int
    target: int
    entropy: float


class BulkNode(BaseModel):
    index: int
    angle: float
    x: float
    y: float
    radius: float


class BulkEdge(BaseModel):
    source: int
    target: int


class GeometryResponse(BaseModel):
    boundary_nodes: list[BoundaryNode]
    boundary_edges: list[BoundaryEdge]
    bulk_nodes: list[BulkNode]
    bulk_edges: list[BulkEdge]
