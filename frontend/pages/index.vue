<template>
  <div
    class="whole-screen"
    ref="graph"
    @click="modifyNode"
    @mousemove="mouseMove"
  />
</template>

<script setup lang="ts">
import * as d3 from 'd3'
import { forceSimulation, forceCenter } from 'd3-force'

const graph = ref<HTMLBodyElement | null>(null)

const linkRadius = 100
const deleteRadius = 10

interface Node extends d3.SimulationNodeDatum {
  id: number
  question: string
  x: number
  y: number
}

interface NodeLink extends d3.SimulationLinkDatum<Node> {
  source: Node
  target: Node
}

const nodes: Node[] = reactive([
  {
    id: 1,
    question: 'What is five plus five?',
    x: 0,
    y: 0,
  },
  {
    id: 2,
    question: 'What is ten plus five?',
    x: 0,
    y: 0,
  },
  {
    id: 3,
    question: 'What is life?',
    x: 0,
    y: 0,
  },
])

const links: d3.SimulationLinkDatum<Node>[] = reactive([
  {
    source: 1,
    target: 2,
  },
])

let simulation: d3.Simulation<Node, NodeLink>
let link: d3.Selection<
  d3.BaseType | SVGPathElement,
  d3.SimulationLinkDatum<Node>,
  SVGGElement,
  unknown
>
let node: d3.Selection<d3.BaseType | SVGGElement, Node, SVGGElement, unknown>
let linkForce: d3.ForceLink<Node, d3.SimulationLinkDatum<Node>>

let mouseX = 0
let mouseY = 0

const getId = (nodeRepresentation: number | string | Node) =>
  typeof nodeRepresentation === 'number'
    ? nodeRepresentation
    : typeof nodeRepresentation === 'string'
    ? parseInt(nodeRepresentation)
    : nodeRepresentation.id

const modifyNode = (event: MouseEvent) => {
  const [x, y] = d3.pointer(event)
  const node = simulation.find(x, y, deleteRadius)
  if (node) {
    links.splice(
      0,
      links.length,
      ...links.filter(
        (link) =>
          getId(link.source) !== node.id && getId(link.target) !== node.id
      )
    )
    nodes.splice(nodes.indexOf(node), 1)
  } else {
    const newId = nodes.length + 1
    const node = simulation.find(x, y, linkRadius)

    nodes.push({
      id: newId,
      question: `Node ${newId}`,
      x: x,
      y: y,
    })

    if (node) {
      links.push({
        source: getId(node),
        target: newId,
      })
    }
  }
}

const mouseMove = (event: MouseEvent) => {
  ;[mouseX, mouseY] = d3.pointer(event)
}

const updateNodes = () => {
  link = link.data(links).join('path').attr('stroke', 'black')

  node = node.data(nodes).join(
    (enter) => {
      const output = enter.append('g')

      output
        .append('circle')
        .attr('stroke', 'white')
        .attr('stroke-width', 1.5)
        .attr('r', 4)

      output
        .append('text')
        .attr('x', 8)
        .attr('y', '0.31em')
        .text((d) => d.question)
        .clone(true)
        .lower()
        .attr('fill', 'none')
        .attr('stroke', 'white')
        .attr('stroke-width', 3)

      return output
    },
    (update) => update,
    (exit) => exit.remove()
  )

  simulation.nodes(nodes)
  linkForce.links(links)

  simulation.alpha(1).restart()
}

watch(nodes, updateNodes)

const linkArc = (d: NodeLink) => {
  const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y)
  return `
    M${d.source.x},${d.source.y}
    A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
  `
}

onMounted(() => {
  const container = d3.select(graph.value)

  const svg = container.append('svg').attr('width', 1000).attr('height', 500)

  linkForce = d3
    .forceLink<Node, d3.SimulationLinkDatum<Node>>(links)
    .id((d) => d.id)

  simulation = forceSimulation(nodes)
    .force('link', linkForce)
    .force('charge', d3.forceManyBody().strength(-400))
    .force('x', d3.forceX())
    .force('y', d3.forceY())

  link = svg
    .append('g')
    .attr('fill', 'none')
    .attr('stroke-width', 1.5)
    .selectAll('path')
    .data(links)
    .join('path')
    .attr('stroke', 'black')

  node = svg
    .append('g')
    .attr('fill', 'currentColor')
    .attr('stroke-linecap', 'round')
    .attr('stroke-linejoin', 'round')
    .selectAll('g')
    .data(nodes)
    .join('g')

  node
    .append('circle')
    .attr('stroke', 'white')
    .attr('stroke-width', 1.5)
    .attr('r', 4)

  node
    .append('text')
    .attr('x', 8)
    .attr('y', '0.31em')
    .text((d) => d.question)
    .clone(true)
    .lower()
    .attr('fill', 'none')
    .attr('stroke', 'white')
    .attr('stroke-width', 3)

  const mouseLink = svg
    .append('g')
    .append('line')
    .attr('display', 'none')
    .attr('stroke', 'red')

  simulation.on('tick', () => {
    link.attr('d', (d: d3.SimulationLinkDatum<Node>) => linkArc(d as NodeLink))
    node.attr('transform', (d) => `translate(${d.x},${d.y})`)

    const closest = simulation.find(mouseX, mouseY, linkRadius)

    if (closest) {
      mouseLink
        .attr('display', 'true')
        .attr('x1', mouseX)
        .attr('y1', mouseY)
        .attr('x2', closest.x)
        .attr('y2', closest.y)
    } else {
      mouseLink.attr('display', 'none')
    }
  })

  const resize = () => {
    var width = parseInt(container.style('width'))
    var height = parseInt(container.style('height'))
    svg.attr('width', width)
    svg.attr('height', height)

    svg
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMinYMid meet')

    simulation.force('center', forceCenter(width / 2, height / 2))
    simulation.restart()
  }

  resize()
  d3.select(window).on(`resize.${container.attr('id')}`, resize)
})
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
