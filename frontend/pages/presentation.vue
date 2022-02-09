<template>
  <div class="fill-screen">
    <div class="reveal">
      <div class="slides">
        <section data-markdown="slides/1.md" />
        <section>
          <div class="columns">
            <div class="column">
              <iframe data-src="/#view" width="1000px" height="600px" />
            </div>
            <div class="column">
              <iframe data-src="/#submit" width="1000px" height="600px" />
            </div>
          </div>
        </section>
        <section data-markdown="slides/2.md" />
        <section>
          <div class="columns">
            <div class="column">
              <iframe data-src="/#view" width="1000px" height="600px" />
            </div>
            <div class="column">
              <h1>Thank you</h1>
              <p>
                <a href="https://github.com/questia/web-app">
                  https://github.com/questia/web-app
                </a>
              </p>
              <p>Any questions?</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import Reveal from 'reveal.js'
import Markdown from 'reveal.js/plugin/markdown/markdown.esm.js'

onMounted(() => {
  let deck = new Reveal({
    plugins: [Markdown],
    embedded: true,
  })
  deck.initialize()

  window.setTimeout(() => {
    deck.layout()
  }, 500)
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
