import { CytoscapeOptions } from 'cytoscape';

export const GRAPH_LAYOUT_OPTIONS: CytoscapeOptions = {
    layout: {
        name: 'dagre'
    },
    boxSelectionEnabled: false,
    autounselectify: true,
    style: [
        {
            selector: 'node',
            style: {
                'background-color': '#11479e',
                'content': 'data(label)'
            }
        },
        {
            selector: 'edge',
            style: {
                'width': 1,
                'target-arrow-shape': 'triangle',
                'line-color': '#9dbaea',
                'target-arrow-color': '#9dbaea',
                'curve-style': 'bezier'
            }
        }
    ]
}
