<template>
  <div>
    <b-navbar type="is-primary">
      <template #brand>
        <b-navbar-item>
          <img src="/icon.png" class="mt-1 mr-2" />
          <h1 class="title" style="color: white"><b>Questia</b></h1>
        </b-navbar-item>
      </template>
      <template #start>
        <b-navbar-item @click="() => (isTeacher = true)">
          Teacher view
        </b-navbar-item>
        <b-navbar-item @click="() => (isTeacher = false)">
          Student view
        </b-navbar-item>
      </template>
    </b-navbar>
    <div class="body">
      <div class="box my-4 mx-2 ml-4 column is-2">
        <div class="p-2">
          <b-menu class="menu">
            <b-menu-list>
              <b-menu-item
                label="View questions"
                @click="() => (page = 1)"
                :active="page === 1"
              />
              <b-menu-item
                label="Submit question"
                @click="() => (page = 2)"
                :active="page === 2"
              />
              <b-menu-item label="Transcript" disabled />
            </b-menu-list>
          </b-menu>
        </div>
      </div>
      <div class="box my-4 mx-2 mr-4 column" style="overflow: hidden">
        <div v-if="page === 2" class="enter-question">
          <div class="container p-5">
            <div class="columns">
              <div class="column is-4">
                <h2 class="title">Submit question</h2>
                <b-field label="Question">
                  <b-input
                    v-model="questionInput"
                    :disabled="suggestionExists"
                  ></b-input>
                </b-field>
                <b-field>
                  <b-button
                    @click="suggestQuestion"
                    :disabled="suggestionExists"
                  >
                    Submit Question
                  </b-button>
                </b-field>
                <b-notification
                  type="is-primary"
                  :closable="false"
                  :active="suggestionExists"
                >
                  <div class="block">
                    <p>This question looks very similar to:</p>
                    <p>
                      <em>
                        {{ suggestionText }}
                      </em>
                    </p>
                    <p>Is your question separate, linked or a duplicate?</p>
                  </div>
                  <div class="buttons">
                    <b-button
                      type="is-primary is-light"
                      @click="selectSeparate"
                    >
                      Separate
                    </b-button>
                    <b-button type="is-primary is-light" @click="selectLinked">
                      Linked
                    </b-button>
                    <b-button
                      type="is-primary is-light"
                      @click="selectDuplicate"
                    >
                      Duplicate
                    </b-button>
                  </div>
                </b-notification>
              </div>
            </div>
          </div>
        </div>

        <div
          class="view-questions fill"
          :style="{ visibility: page === 1 ? 'visible' : 'hidden' }"
        >
          <div
            class="fill"
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
                        <b-input></b-input>
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
      </div>
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
const isTeacher = ref(true)

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
}

interface NodeLink extends d3.SimulationLinkDatum<Node> {
  source: Node
  target: Node
}

const answerQuestion = () => {
  if (selectedNode.value) {
    // selectedNode.value.answered = true
    // selectedNode.value.answer = 'answer'
  }
}

const nodes: Node[] = reactive([])

const links: d3.SimulationLinkDatum<Node>[] = reactive([])

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
        .attr('r', 8)

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
  const container = d3.select(graph.value)

  const svg = container.append('svg').attr('width', 1000).attr('height', 500)

  linkForce = d3
    .forceLink<Node, d3.SimulationLinkDatum<Node>>(links)
    .id((d) => d.id)

  simulation = forceSimulation(nodes)
    .force('link', linkForce)
    .force('charge', d3.forceManyBody().strength(-3000))
    .force('x', d3.forceX())
    .force('y', d3.forceY())
    .velocityDecay(0.8)

  link = svg
    .append('g')
    .attr('fill', 'none')
    .attr('stroke-width', 1.5)
    .selectAll('path')
    .data(links)
    .join('path')

  node = svg
    .append('g')
    .attr('fill', 'currentColor')
    .attr('stroke-linecap', 'round')
    .attr('stroke-linejoin', 'round')
    .selectAll('g')
    .data(nodes)
    .join('g')

  simulation.on('tick', () => {
    link.attr('d', (d: d3.SimulationLinkDatum<Node>) => linkArc(d as NodeLink))
    node.attr('transform', (d) => `translate(${d.x},${d.y})`)

    // const closest = simulation.find(mouseX, mouseY, linkRadius)
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
  window.setInterval(fetchState, 4000)
  await fetchState()
})

const questionInput = ref('What are forces?')
const suggestion = ref<number | null>(null)
const suggestionText = ref('')
const suggestionExists = computed(() => suggestion.value !== null)

const submitQuestion = async (link: number) => {
  await $axios.$put('/api/confirm-link', {
    text: questionInput.value,
    link,
  })
}

const suggestQuestion = async () => {
  if (suggestionExists.value) {
    return
  }

  const { id, text } = await $axios.$post('/api/get-potential-link', {
    text: questionInput.value,
  })

  if (id !== -1) {
    suggestion.value = id
    suggestionText.value = text
  } else {
    await submitQuestion(0)
    questionInput.value = ''
  }
}

const selectSeparate = async () => {
  await submitQuestion(0)
  questionInput.value = ''
  suggestion.value = null
}

const selectLinked = async () => {
  await submitQuestion(suggestion.value as number)
  questionInput.value = ''
  suggestion.value = null
}

const selectDuplicate = () => {
  suggestion.value = null
}
</script>

<style>
.fill {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

html {
  overflow: hidden;
}

.body {
  display: flex;
  height: calc(100vh - 52px);
  width: 100vw;
  background-color: #f8f8f8;
}

.main-panel {
  display: flex;
}
</style>
