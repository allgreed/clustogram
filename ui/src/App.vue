<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <GraphView></GraphView>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import GraphView from './components/GraphView.vue';

export default defineComponent({
  name: 'App',
  components: {
    GraphView
  }
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
