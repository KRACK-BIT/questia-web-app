<template>
  <div>
    <b-navbar type="is-primary">
      <template #brand>
        <b-navbar-item>
          <img src="/icon.png" class="mt-1 mr-2" />
          <h1 class="title" style="color: white">
            <b>Questia</b>
            <span style="font-weight: lighter; font-size: 1.5rem">
              {{ isTeacher ? 'Teacher' : 'Student' }}
            </span>
          </h1>
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
      <div
        class="box my-4 mx-2 ml-4 column is-2"
        v-if="$route.hash !== '#view' && $route.hash !== '#submit'"
      >
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
        </div>
      </div>
    </div>
    <b-modal v-model="modalActive" :width="640" :has-modal-card="isTeacher">
      <div v-if="isTeacher" class="modal-card" style="width: auto">
        <form v-on:submit.prevent>
          <header class="modal-card-head">
            <p class="modal-card-title">Answer question</p>
          </header>
          <section class="modal-card-body">
            <b-field label="Answer">
              <b-input />
            </b-field>
          </section>
          <footer class="modal-card-foot">
            <b-button
              type="button"
              tag="input"
              native-type="submit"
              @click="answerQuestion"
              disabled
            >
              Submit Answer
            </b-button>
          </footer>
        </form>
      </div>
      <div v-else class="box">
        <p>Question currently unanswered</p>
      </div>
    </b-modal>
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
  type: 'Question' | 'Topic'
}

interface Node extends d3.SimulationNodeDatum {
  id: number
  text: string
  x: number
  y: number
  type: 'Question' | 'Topic'
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
  if (node && node.type === 'Question') {
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
        .attr('fill', (d) => (d.type === 'Topic' ? '#4A4A4A' : '#7957D5'))

      output
        .append('text')
        .attr('x', '0.6em')
        .attr('y', '0.7em')
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

const route = useRoute()
const page = ref(route.hash === '#submit' ? 2 : 1)

const $axios = useNuxtApp().$axios as NuxtAxiosInstance

const getLinksAndNodes = async () => {
  const { links, nodes: serverNodes } = (await $axios.$get(
    '/api/get-tree'
  )) as {
    links: d3.SimulationLinkDatum<Node>[]
    nodes: ServerNode[]
  }
  const nodes = serverNodes.map(({ id, text, type }) => {
    return {
      x: 0,
      y: 0,
      id,
      text,
      type,
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
