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

"""FastAPI app exposing the live physics simulation and the learned world model.

On first startup (no checkpoint yet), the lifespan trains the world model
synchronously before serving -- so `run.sh`'s single `uvicorn` command
transparently trains-then-serves the first time and just loads-then-serves
after that.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.models import FieldRequest, FieldResponse, LearnedRequest
from app.path_integral import GRID_SIZE, compute_field
from app.train_world_model import train
from app.world_model import CHECKPOINT_PATH, load_model, predict


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not CHECKPOINT_PATH.exists():
        train()
    app.state.model = load_model()
    yield


app = FastAPI(title="Path Integral Visualizer", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/field", response_model=FieldResponse)
def field(req: FieldRequest) -> dict:
    result = compute_field(req.start, req.end, req.num_paths, req.hbar)
    return {"field": result.tolist(), "grid_size": GRID_SIZE}


@app.post("/api/learned", response_model=FieldResponse)
def learned(req: LearnedRequest, request: Request) -> dict:
    result = predict(request.app.state.model, req.start, req.end, req.hbar)
    return {"field": result.tolist(), "grid_size": GRID_SIZE}
