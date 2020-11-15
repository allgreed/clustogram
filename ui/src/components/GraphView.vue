<template>
  <div ref="cy" style="width: 100vw; height: 100vh;"></div>
</template>

<script lang="ts">

import { defineComponent } from 'vue';
import cytoscape from 'cytoscape';
import dagre from 'cytoscape-dagre';
import { GRAPH_LAYOUT_OPTIONS } from '@/graph-ui.config';
import { GraphDataService } from '@/services/graph-data.service';

export default defineComponent({
  name: 'GraphView',
  mounted() {
    const graphContainer: HTMLElement = this.$refs.cy as HTMLElement;
    this.setupCytoscape(graphContainer);
  },
  methods: {
    async setupCytoscape(container: HTMLElement) {
      const { nodes, edges } = await new GraphDataService().getGraphElements();
      cytoscape.use(dagre);
      cytoscape({
        container,
        ...GRAPH_LAYOUT_OPTIONS,
        elements: {
          nodes,
          edges
        }
      })
    }
  }
});
</script>
