<template>
  <div class="whole-screen" ref="graph" />
</template>

<script setup lang="ts">
import * as d3 from 'd3';
import { forceSimulation, forceCenter } from 'd3-force';

const graph = ref<HTMLBodyElement | null>(null);

interface Node extends d3.SimulationNodeDatum {
  id: number;
  question: string;
  x: number;
  y: number;
};

interface NodeLink extends d3.SimulationLinkDatum<Node> {
  source: Node;
  target: Node;
};

const nodes: Node[] = [
  {
    id: 1,
    question: "What is five plus five?",
    x: 0,
    y: 0,
  },
  {
    id: 2,
    question: "What is ten plus five?",
    x: 0,
    y: 0,
  },
  {
    id: 3,
    question: "What is life?",
    x: 0,
    y: 0,
  }
];

const links: d3.SimulationLinkDatum<Node>[] = [
  {
    source: 1,
    target: 2,
  },
];

const linkArc = (d: NodeLink) => {
  const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
  return `
    M${d.source.x},${d.source.y}
    A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
  `;
};

onMounted(() => {
  const container = d3.select(graph.value);

  const svg = container
    .append("svg")
    .attr("width", 1000)
    .attr("height", 500);

  const simulation = forceSimulation(nodes)
    .force("link", d3.forceLink<Node, d3.SimulationLinkDatum<Node>>(links).id(d => d.id))
    .force("charge", d3.forceManyBody().strength(-400))
    .force("x", d3.forceX())
    .force("y", d3.forceY());

  const link = svg.append("g")
    .attr("fill", "none")
    .attr("stroke-width", 1.5)
    .selectAll("path")
    .data(links)
    .join("path")
    .attr("stroke", "black");

  const node = svg.append("g")
    .attr("fill", "currentColor")
    .attr("stroke-linecap", "round")
    .attr("stroke-linejoin", "round")
    .selectAll("g")
    .data(nodes)
    .join("g")

  node.append("circle")
    .attr("stroke", "white")
    .attr("stroke-width", 1.5)
    .attr("r", 4);

  node.append("text")
    .attr("x", 8)
    .attr("y", "0.31em")
    .text(d => d.question)
    .clone(true).lower()
    .attr("fill", "none")
    .attr("stroke", "white")
    .attr("stroke-width", 3);

  simulation.on("tick", () => {
    link.attr("d", (d: d3.SimulationLinkDatum<Node>) => linkArc(d as NodeLink));
    node.attr("transform", d => `translate(${d.x},${d.y})`);
  });

  const resize = () => {
    var width = parseInt(container.style("width"));
    var height = parseInt(container.style("height"));
    svg.attr("width", width);
    svg.attr("height", height);

    svg.attr("viewBox", `0 0 ${width} ${height}`)
      .attr("preserveAspectRatio", "xMinYMid meet");

    simulation.force("center", forceCenter(width / 2, height / 2));
    simulation.restart();
  }

  resize();
  d3.select(window).on(`resize.${container.attr("id")}`, resize);
});
</script>

<style>
.whole-screen {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

html {
  overflow: hidden;
}

.svg-container {
  display: inline-block;
  position: relative;
  width: 100%;
  padding-bottom: 100%;
  vertical-align: top;
  overflow: hidden;
}

.svg-content {
  display: inline-block;
  position: absolute;
  top: 0;
  left: 0;
}
</style>
