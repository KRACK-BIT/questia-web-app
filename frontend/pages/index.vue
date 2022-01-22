<template>
  <section class="hero is-fullheight">
    <div class="hero-body" ref="graph"></div>
  </section>
</template>

<script setup lang="ts">
import * as d3 from 'd3';

const graph = ref<HTMLBodyElement | null>(null);

onMounted(() => {
  d3.select(graph.value)
    .append("span")
    .text("Hello, world!");
});
</script>
