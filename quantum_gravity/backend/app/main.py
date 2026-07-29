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

"""FastAPI app exposing the quantum-derived and classical-baseline geometry endpoints."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.baseline import classical_geometry
from app.happy_code import quantum_geometry
from app.models import GeometryRequest, GeometryResponse

app = FastAPI(title="Quantum Gravity POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/geometry", response_model=GeometryResponse)
def geometry(req: GeometryRequest) -> dict:
    return quantum_geometry(req.strengths)


@app.get("/api/baseline", response_model=GeometryResponse)
def baseline(seed: int = 42) -> dict:
    return classical_geometry(seed)
