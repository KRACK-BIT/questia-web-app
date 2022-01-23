<template>
  <div class="page">
    <b-navbar style="background-color: #765ad8">
      <template #brand>
        <b-navbar-item>
          <img src="../static/icon.png" style="margin: 10px" />
          <h1 class="title" style="color: white"><b>Questia</b></h1>
        </b-navbar-item>
      </template>
    </b-navbar>
    <div class="body">
      <div class="side-panel">
        <b-sidebar position="static" open type="is-light">
          <div class="p-4">
            <b-menu class="menu">
              <b-menu-list>
                <b-menu-item
                  label="Submit question"
                  @click="() => (page = 1)"
                  :active="page === 1"
                />
                <b-menu-item
                  label="View questions"
                  @click="() => (page = 2)"
                  :active="page === 2"
                />
              </b-menu-list>
            </b-menu>
          </div>
        </b-sidebar>
      </div>
      <div v-if="page === 1" class="enter-question">
        <div class="section">
          <div style="text-align: center; margin: 15px">
            <b-field label="Question">
              <b-input></b-input>
            </b-field>
          </div>
          <div style="margin: 15px">
            <b-field>
              <b-button>Submit Question</b-button>
            </b-field>
          </div>
          <div style="margin: 15px">
            <p v-if="isLink === 1">
              This question looks very similar to: {{ linkQuestion }}. Is your
              question seperate, linked or a duplicate?
            </p>
          </div>
          <div v-if="isLink" style="margin: 15px">
            <b-field>
              <b-button>Seperate</b-button>
              <b-button>Linked</b-button>
              <b-button>Duplicate</b-button>
            </b-field>
          </div>
        </div>
      </div>
      <div v-show="page === 2" class="view-questions">
        <div
          class="whole-screen"
          ref="graph"
          @click="modifyNode"
          @mousemove="mouseMove"
        />
        <b-modal v-if="isTeacher" v-model="modalActive">
          <modal-form>
            <form action="">
              <div class="modal-card" style="width: auto">
                <header
                  class="modal-card-head"
                  style="display: flex; flex-direction: column"
                >
                  <div>
                    <p class="modal-card-title" style="margin: 15px">
                      Answer Question:
                    </p>
                    <b-field>
                      <b-input> </b-input>
                    </b-field>
                  </div>
                  <b-button
                    type="button"
                    style="margin: 10px"
                    @click="answerQuestion"
                    >Submit Answer</b-button
                  >
                </header>
              </div>
            </form>
          </modal-form>
        </b-modal>
        <b-modal v-if="!isTeacher" v-model="modalActive">
          <modal-form>
            <form action="">
              <div class="modal-card" style="width: auto">
                <header class="modal-card-head">
                  <p class="modal-card-title">Answer: {{}}</p>
                </header>
              </div>
            </form>
          </modal-form>
        </b-modal>
      </div>
      <div v-if="page === 3" class="view-transcript"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import * as d3 from 'd3'
import { forceSimulation, forceCenter } from 'd3-force'

import type { NuxtAxiosInstance } from '@nuxtjs/axios'

const graph = ref<HTMLBodyElement | null>(null)

const linkRadius = 100
const deleteRadius = 20
const modalActive = ref(false)
const selectedNode = ref<Node | null>(null)
const isLink = ref(0)
const linkQuestion = ref('What are forces?')
const isTeacher = ref(1)

interface ServerNode {
  id: number
  text: string
  topic: string
}

interface Node extends d3.SimulationNodeDatum {
  id: number
  text: string
  x: number
  y: number
  answered: boolean
  answer: string
}

interface NodeLink extends d3.SimulationLinkDatum<Node> {
  source: Node
  target: Node
}

const answerQuestion = () => {
  if (selectedNode.value) {
    selectedNode.value.answered = true
    selectedNode.value.answer = 'answer'
  }
}

const nodes: Node[] = reactive([
  {
    id: 1,
    text: 'What is five plus five?',
    x: 0,
    y: 0,
    answered: false,
    answer: '',
  },
  {
    id: 2,
    text: 'What is ten plus five?',
    x: 0,
    y: 0,
    answered: false,
    answer: '',
  },
  {
    id: 3,
    text: 'What is life?',
    x: 0,
    y: 0,
    answered: false,
    answer: '',
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
    modalActive.value = true
    selectedNode.value = node
  } else {
    /*
    const newId = nodes.length + 1
    const node = simulation.find(x, y, linkRadius)

    nodes.push({
      id: newId,
      text: `Question ${newId}`,
      x: x,
      y: y,
    })

    if (node) {
      links.push({
        source: getId(node),
        target: newId,
      })
    }
    */
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
        .text((d) => d.text)
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
  while (graph.value === null) {}
  console.log(JSON.stringify(graph.value))
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
    .text((d) => d.text)
    .clone(true)
    .lower()
    .attr('fill', 'none')
    .attr('stroke', 'white')
    .attr('stroke-width', 3)

  simulation.on('tick', () => {
    link.attr('d', (d: d3.SimulationLinkDatum<Node>) => linkArc(d as NodeLink))
    node.attr('transform', (d) => `translate(${d.x},${d.y})`)

    const closest = simulation.find(mouseX, mouseY, linkRadius)
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

const page = ref(1)

const $axios = useNuxtApp().$axios as NuxtAxiosInstance

const getLinksAndNodes = async () => {
  const { links, nodes: serverNodes } = (await $axios.$get(
    '/api/get-tree'
  )) as {
    links: d3.SimulationLinkDatum<Node>[]
    nodes: ServerNode[]
  }
  const nodes = serverNodes.map(({ id, text }) => {
    return {
      x: 0,
      y: 0,
      id,
      text,
    }
  })
  return { links, nodes }
}

const fetchState = async () => {
  const { links: latestLinks, nodes: latestNodes } = await getLinksAndNodes()
  const newNodes = latestNodes.filter(
    (node) => !nodes.some((n) => n.id === node.id)
  )
  const newLinks = latestLinks.filter(
    (link) =>
      !links.some(
        (l) =>
          getId(l.source) === getId(link.source) &&
          getId(l.target) === getId(link.target)
      )
  )
  nodes.push(...newNodes)
  links.push(...newLinks)
}

onMounted(async () => {
  window.setInterval(fetchState, 500)
  await fetchState()
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

.page {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.body {
  display: flex;
  height: 100%;
  width: 100vw;
}

.side-panel {
  display: flex;
  flex-direction: column;
}
.main-panel {
  display: flex;
}

.whole-screen {
  display: flex;
}

.enter-questions {
  display: flex;
  flex-direction: column;
}

.enter-question {
  justify-content: center;
  align-content: center;
}

.section {
  display: flex;
  flex-direction: column;
}
</style>

