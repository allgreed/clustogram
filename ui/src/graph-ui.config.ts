import { CytoscapeOptions } from 'cytoscape';
import ICON_MAPPING from '../../icons/icon_mapping.json';

export const ICONS_ROOT_DIR = '/icons/';

export const K8S_KIND_TO_ICON_FILE_NAME: Record<string, string> = ICON_MAPPING
    .reduce((acc, { namespace, icon }) => ({
        ...acc,
        [namespace]: icon
    }));

const ICON_STYLES: CytoscapeOptions['style'] = Object.entries(K8S_KIND_TO_ICON_FILE_NAME).map(([iconKind, iconFileName]) => {
    return {
        selector: '.' + getClassSelectorFromKind(iconKind),
        style: {
            'background-image': `url(${ ICONS_ROOT_DIR }${ iconFileName })`,
            'shape': 'rectangle',
            'font-size': 6,
            'text-wrap': 'wrap',
            'text-halign': 'center',
            'text-valign': 'bottom',
            'background-fit': 'cover',
            'background-opacity': 0,
        }
    };
});

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
                'width': 0.5,
                'target-arrow-shape': 'triangle',
                'line-color': '#9dbaea',
                'target-arrow-color': '#9dbaea',
                'curve-style': 'bezier',
                'arrow-scale': 0.4
            }
        },
        {
            selector: 'node',
            style: {
                'content': 'data(label)',
                'font-size': 4,
            }
        },
        ...ICON_STYLES
    ]
};

export function getClassSelectorFromKind(kind: string): string {
    return kind.replace(/\W/g, '');
}
