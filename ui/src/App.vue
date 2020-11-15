<template>
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
  margin: 0;
  padding: 0;
}
</style>
