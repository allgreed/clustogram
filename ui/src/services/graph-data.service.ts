import { EdgeDefinition, ElementsDefinition, NodeDefinition } from 'cytoscape';
import { GraphEntity, GraphToUiModel } from '@/graph-ui.model';
import MOCK_JSON from '../../tests/graph-example.json';
import { getClassSelectorFromKind } from '@/graph-ui.config';
import { ErrorHandlerService } from '@/services/error-handler-service';
import { HttpClientService } from '@/services/http-client.service';

export class GraphDataService {
    getGraphElements(): Promise<ElementsDefinition> {
        return this.fetchData().then(this.mapResponseToGraphElements.bind(this));
    }

    private fetchData(): Promise<GraphToUiModel> {
        return HttpClientService.get(process.env.VUE_APP_GRAPH_DATA_URL)
            .then((response) => response.json())
            .catch(() => {
                ErrorHandlerService.handleError({message: 'Graph Data not found, returning mock data...'});
                return MOCK_JSON;
            });
    }

    private mapResponseToGraphElements(response: GraphToUiModel): ElementsDefinition {
        return {
            edges: this.mapGraphUiModelToEdgeDefinitions(response),
            nodes: this.mapGraphUiModelToNodeDefinitions(response)
        };
    }

    private mapGraphUiModelToNodeDefinitions(response: GraphToUiModel): NodeDefinition[] {
        return response.entities.map((entity) => {
            return ({
                data: {
                    id: entity.name,
                    label: entity.name
                },
                classes: getClassSelectorFromKind(entity.kind)
            });
        });
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
