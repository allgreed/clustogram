import { EdgeDefinition, ElementsDefinition, NodeDefinition } from 'cytoscape';
import { GraphEntity, GraphToUiModel } from '@/graph-ui.model';
import MOCK_JSON from '../../tests/graph-example.json';

export class GraphDataService {
    getGraphElements(): Promise<ElementsDefinition> {
        return Promise.resolve(this.mapResponseToGraphElements(MOCK_JSON as any));
    }

    private fetchData(): Promise<GraphToUiModel> {
        return fetch('/output.json').then(({ json }) => json());
    }

    private mapResponseToGraphElements(response: GraphToUiModel): ElementsDefinition {
        return {
            edges: this.mapGraphUiModelToEdgeDefinitions(response),
            nodes: this.mapGraphUiModelToNodeDefinitions(response)
        };
    }

    private mapGraphUiModelToNodeDefinitions(response: GraphToUiModel): NodeDefinition[] {
        return response.entities.map((entity) => ({
            data: {
                id: entity.name,
                label: entity.name
            }
        }));
    }

    private mapGraphUiModelToEdgeDefinitions(response: GraphToUiModel): EdgeDefinition[] {
        return response.entities.map(this.mapEntityToEdges).flat();
    }

    private mapEntityToEdges(graphEntity: GraphEntity): EdgeDefinition[] {
        return graphEntity.references.reduce((acc: EdgeDefinition[], reference) => {
            const edgeDef: EdgeDefinition = { data: { source: graphEntity.name, target: reference.name } };
            return [...acc, edgeDef];
        }, []);
    }
}
