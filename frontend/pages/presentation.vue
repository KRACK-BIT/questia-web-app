<template>
  <div class="fill-screen">
    <div class="reveal">
      <div class="slides">
        <section>Slide 1</section>
        <section>Slide 2</section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Reveal from 'reveal.js'
import Markdown from 'reveal.js/plugin/markdown/markdown.esm.js'

onMounted(() => {
  let deck = new Reveal({
    plugins: [Markdown],
  })
  deck.initialize()
})

useMeta({
  link: [
    {
      rel: 'stylesheet',
      href: '/node_modules/reveal.js/dist/reveal.css',
    },
    {
      rel: 'stylesheet',
      href: '/node_modules/reveal.js/dist/theme/black.css',
    },
  ],
})
</script>

<style>
.fill-screen {
  width: 100vw;
  height: 100vh;
}
</style>
