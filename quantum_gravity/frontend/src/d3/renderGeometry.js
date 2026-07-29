import * as d3 from "d3";
import { S_EDGE_MAX } from "../constants.js";

const WIDTH = 520;
const HEIGHT = 520;
const TRANSITION_MS = 500;

// Sequential blue ramp (dataviz skill), reversed for a dark surface: low
// entropy recedes toward the dark background, high entropy glows outward.
const edgeColor = d3
  .scaleLinear()
  .domain([0, S_EDGE_MAX / 3, (2 * S_EDGE_MAX) / 3, S_EDGE_MAX])
  .range(["#0d366b", "#256abf", "#6da7ec", "#cde2fb"])
  .interpolate(d3.interpolateRgb)
  .clamp(true);

const edgeWidth = d3.scaleLinear().domain([0, S_EDGE_MAX]).range([1.5, 6]).clamp(true);

const bulkPolygonLine = d3
  .line()
  .x((d) => d.x)
  .y((d) => d.y)
  .curve(d3.curveLinearClosed);

/**
 * Imperative D3 render/update of the boundary + bulk geometry. D3 owns this
 * whole <svg> subtree (see GeometryCanvas.jsx) so it never fights React for
 * the same DOM nodes; call this again with new data to transition smoothly.
 */
export function renderGeometry(svgEl, geometry, handlers = {}) {
  if (!svgEl || !geometry) return;
  const { onNodeEnter, onNodeMove, onNodeLeave } = handlers;

  const svg = d3
    .select(svgEl)
    .attr("viewBox", `${-WIDTH / 2} ${-HEIGHT / 2} ${WIDTH} ${HEIGHT}`);

  let scene = svg.select("g.scene");
  if (scene.empty()) {
    scene = svg.append("g").attr("class", "scene");
    scene.append("circle").attr("class", "boundary-guide");
    scene.append("path").attr("class", "bulk-polygon");
    scene.append("g").attr("class", "legs");
    scene.append("g").attr("class", "boundary-edges");
    scene.append("g").attr("class", "bulk-nodes");
    scene.append("g").attr("class", "boundary-nodes");
    scene.append("g").attr("class", "boundary-labels");
  }

  const { boundary_nodes: bNodes, boundary_edges: bEdges, bulk_nodes: kNodes } = geometry;

  const boundaryRadius = Math.max(...bNodes.map((n) => Math.hypot(n.x, n.y)), 1);
  scene
    .select("circle.boundary-guide")
    .attr("r", boundaryRadius)
    .attr("fill", "none")
    .attr("stroke", "#2c2c2a")
    .attr("stroke-width", 1);

  scene
    .select("path.bulk-polygon")
    .datum(kNodes)
    .transition()
    .duration(TRANSITION_MS)
    .attr("d", bulkPolygonLine)
    .attr("fill", "#d95926")
    .attr("fill-opacity", 0.16)
    .attr("stroke", "#d95926")
    .attr("stroke-width", 2);

  const legData = kNodes.map((k, i) => ({
    id: i,
    x1: k.x,
    y1: k.y,
    x2: bNodes[i].x,
    y2: bNodes[i].y,
  }));
  scene
    .select("g.legs")
    .selectAll("line")
    .data(legData, (d) => d.id)
    .join((enter) =>
      enter
        .append("line")
        .attr("stroke", "#383835")
        .attr("stroke-width", 1)
        .attr("x1", (d) => d.x1)
        .attr("y1", (d) => d.y1)
        .attr("x2", (d) => d.x2)
        .attr("y2", (d) => d.y2),
    )
    .transition()
    .duration(TRANSITION_MS)
    .attr("x1", (d) => d.x1)
    .attr("y1", (d) => d.y1)
    .attr("x2", (d) => d.x2)
    .attr("y2", (d) => d.y2);

  const edgeData = bEdges.map((e) => ({
    id: e.index,
    x1: bNodes[e.source].x,
    y1: bNodes[e.source].y,
    x2: bNodes[e.target].x,
    y2: bNodes[e.target].y,
    entropy: e.entropy,
  }));
  scene
    .select("g.boundary-edges")
    .selectAll("line")
    .data(edgeData, (d) => d.id)
    .join((enter) =>
      enter
        .append("line")
        .attr("stroke-linecap", "round")
        .attr("x1", (d) => d.x1)
        .attr("y1", (d) => d.y1)
        .attr("x2", (d) => d.x2)
        .attr("y2", (d) => d.y2)
        .attr("stroke", (d) => edgeColor(d.entropy))
        .attr("stroke-width", (d) => edgeWidth(d.entropy)),
    )
    .transition()
    .duration(TRANSITION_MS)
    .attr("x1", (d) => d.x1)
    .attr("y1", (d) => d.y1)
    .attr("x2", (d) => d.x2)
    .attr("y2", (d) => d.y2)
    .attr("stroke", (d) => edgeColor(d.entropy))
    .attr("stroke-width", (d) => edgeWidth(d.entropy));

  scene
    .select("g.bulk-nodes")
    .selectAll("circle")
    .data(kNodes, (d) => d.index)
    .join((enter) =>
      enter
        .append("circle")
        .attr("r", 5)
        .attr("fill", "#d95926")
        .attr("cx", (d) => d.x)
        .attr("cy", (d) => d.y),
    )
    .transition()
    .duration(TRANSITION_MS)
    .attr("cx", (d) => d.x)
    .attr("cy", (d) => d.y);

  const boundaryGroup = scene
    .select("g.boundary-nodes")
    .selectAll("g.boundary-node")
    .data(bNodes, (d) => d.index)
    .join((enter) => {
      const g = enter
        .append("g")
        .attr("class", "boundary-node")
        .attr("transform", (d) => `translate(${d.x},${d.y})`);
      // Hit target sized well past the visible dot, per the interaction spec.
      g.append("circle").attr("class", "hit").attr("r", 16).attr("fill", "transparent");
      g.append("circle")
        .attr("class", "dot")
        .attr("r", 9)
        .attr("fill", "#3987e5")
        .attr("stroke", "#ffffff")
        .attr("stroke-width", 1.5);
      return g;
    });

  boundaryGroup
    .transition()
    .duration(TRANSITION_MS)
    .attr("transform", (d) => `translate(${d.x},${d.y})`);

  boundaryGroup
    .style("cursor", "pointer")
    .on("pointerenter", function (event, d) {
      d3.select(this).select("circle.dot").transition().duration(120).attr("r", 11);
      onNodeEnter?.(d, event);
    })
    .on("pointermove", function (event, d) {
      onNodeMove?.(d, event);
    })
    .on("pointerleave", function (event, d) {
      d3.select(this).select("circle.dot").transition().duration(120).attr("r", 9);
      onNodeLeave?.(d, event);
    });

  // Boundary angle/radius are fixed, so labels never need to transition —
  // just keep them pinned just outside each node, numbered 1-6 for readers.
  const labelRadius = boundaryRadius + 20;
  scene
    .select("g.boundary-labels")
    .selectAll("text")
    .data(bNodes, (d) => d.index)
    .join((enter) =>
      enter
        .append("text")
        .attr("class", "boundary-label")
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "middle")
        .attr("fill", "#c3c2b7")
        .attr("font-size", 12)
        .attr("font-weight", 600)
        .attr("pointer-events", "none"),
    )
    .attr("x", (d) => labelRadius * Math.cos(d.angle))
    .attr("y", (d) => labelRadius * Math.sin(d.angle))
    .text((d) => d.index + 1);
}
