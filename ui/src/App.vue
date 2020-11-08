<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <Graphview app-name="Clustogram"/>
</template>

<script>

import GraphView from './components/GraphView.vue'

export default {
  components: {
    Graphview: GraphView
  }
}
</script>

<style>
#app {
  font-family: Arial sans-serif;
}
</style>
