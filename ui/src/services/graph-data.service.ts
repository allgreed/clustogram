import { ElementsDefinition } from 'cytoscape';
import { GraphToUiModel } from '@/graph-ui.model';

export class GraphDataService {
    getGraphElements(): Promise<ElementsDefinition> {
        return Promise.resolve(this.mapResponseToGraphElements(null as any));
    }

    private fetchData(): Promise<GraphToUiModel> {
        return fetch('/output.json').then(({ json }) => json());
    }

    private mapResponseToGraphElements(response: GraphToUiModel): ElementsDefinition {
        return {
            edges: [],
            nodes: []
        };
    }
}
