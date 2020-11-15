export interface GraphToUiModel {
    version: number;
    entities: GraphEntity[];
}

export interface GraphEntity {
    name: string;
    references: {
        name: string;
    }
}
