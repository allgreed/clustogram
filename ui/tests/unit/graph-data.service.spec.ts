import { GraphDataService } from '@/services/graph-data.service';
import { GraphToUiModel } from '@/graph-ui.model';

jest.mock('@/services/http-client.service', () => {
    const input: GraphToUiModel = {
        'version': 1,
        'entities': [
            {
                'name': 'XXX1',
                'kind': 'Service',
                'references': [
                    {
                        'name': 'XXX1A'
                    },
                    {
                        'name': 'XXX1B'
                    }
                ]
            },
            {
                'name': 'XXX1A',
                'kind': 'PersistentVolume',
                'references': []
            },
            {
                'name': 'XXX1B',
                'kind': 'Job',
                'references': []
            }
        ]
    };

    return {
        HttpClientService: {
            get: () => Promise.resolve({json: () => input})
        }
    };
});

describe('Graph Data Service', () => {
    it('should return Edges definition', async() => {
        const output = await new GraphDataService().getGraphElements();
        expect(output.edges).toEqual([
            {
                'data': {
                    'source': 'XXX1',
                    'target': 'XXX1A'
                }
            },
            {
                'data': {
                    'source': 'XXX1',
                    'target': 'XXX1B'
                }
            }
        ]);
    });

    it('should return node labels', async() => {
        const output = await new GraphDataService().getGraphElements();
        const labels = output.nodes.map((node) => node.data.label);
        expect(labels).toEqual(['XXX1', 'XXX1A', 'XXX1B']);
    });

    it('should return node classes', async() => {
        const output = await new GraphDataService().getGraphElements();
        const classes = output.nodes.map((node) => node.classes);
        expect(classes).toEqual(['Service', 'PersistentVolume', 'Job']);
    });
});
