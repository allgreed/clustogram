export interface GraphToUiModel {
    version: number;
    entities: GraphEntity[];
}

export interface GraphReference {
    name: string
}

export interface GraphEntity {
    name: string;
    kind: string;
    references: GraphReference[]
}
