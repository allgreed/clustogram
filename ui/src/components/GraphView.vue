<template>
  <div class="actions-bar">
    <button v-on:click="fitGraph()" class="graph-action mr-8">FIT</button>
    <button v-on:click="exportGraph()" :disabled="exportStatus === 'loading'" ref="exportBtnRef" class="graph-action">
      <template v-if="exportStatus === 'loading'">
        Exporting...
      </template>
      <template v-else>Export</template>
    </button>
  </div>
  <div ref="cy" style="width: 100vw; height: 100vh;"></div>
</template>

<script lang="ts">
/* eslint-disable no-unused-vars */

import { defineComponent } from 'vue';
import cytoscape from 'cytoscape';
import dagre from 'cytoscape-dagre';
import { GRAPH_LAYOUT_OPTIONS } from '@/graph-ui.config';
import { GraphDataService } from '@/services/graph-data.service';
import { saveAs } from 'file-saver';
import { LoadStatus } from '@/graph-ui.model';
import { ErrorHandlerService } from '@/services/error-handler-service';
import { HttpClientService } from '@/services/http-client.service';

interface GraphViewData {
  cy: cytoscape.Core | undefined
  exportStatus: LoadStatus,
}

export default defineComponent({
  name: 'GraphView',
  data(): GraphViewData {
    return {
      cy: undefined,
      exportStatus: 'idle',
    };
  },
  mounted() {
    const graphContainer: HTMLElement = this.$refs.cy as HTMLElement;
    this.setupCytoscape(graphContainer).then((cytoscape) => {
      this.cy = cytoscape;
    })
  },
  methods: {
    async setupCytoscape(container: HTMLElement): Promise<cytoscape.Core> {
      const { nodes, edges } = await new GraphDataService().getGraphElements();
      cytoscape.use(dagre);
      return cytoscape({
        container,
        ...GRAPH_LAYOUT_OPTIONS,
        elements: {
          nodes,
          edges
        },
        wheelSensitivity: 0.2
      });
    },

    fitGraph(): void {
      this.cy?.fit();
    },

    exportGraph(): void {
      this.exportStatus = 'loading';

      HttpClientService.get(process.env.VUE_APP_GRAPH_DATA_URL).then((response) => response.text()).then((content) => {
        saveAs(new Blob([content]), 'graph-export.json');
      }).then(() => {
        this.exportStatus = 'idle';
      }).catch(() => {
        ErrorHandlerService.handleError({ message: 'Failed to Export Graph' });
        this.exportStatus = 'error';
      });
    }
  }
});
</script>

<style scoped>
.actions-bar {
  position: absolute;
  z-index: 10;
}

.graph-action {
  background: #326ce5;
  font-family: sans-serif;
  border-radius: 4px;
  border-width: 0;
  color: #fff;
  font-size: 14px;
  padding: 4px 12px;
  cursor: pointer;
}

.graph-action:hover {
  transition: 0.2s;
  background: #447df5;
}

.graph-action:disabled {
  background: #a7a7a7;
}

.mr-8 {
  margin-right: 8px;
}
</style>
