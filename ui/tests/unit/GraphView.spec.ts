import { mount } from '@vue/test-utils';
import GraphView from '@/components/GraphView.vue';
import { ElementsDefinition } from 'cytoscape';

jest.mock('@/services/graph-data.service', () => {
    return {
        GraphDataService: jest.fn().mockImplementation(() => {
            return {
                getGraphElements(): Promise<ElementsDefinition> {
                    return Promise.resolve({
                        nodes: [],
                        edges: []
                    });
                }
            };
        }),
    };
});


describe('GraphView', () => {
    it('shows create canvas', (done) => {
        const wrapper = mount(GraphView);
        wrapper.vm.$nextTick(() => {
            expect(wrapper.element.querySelector('canvas')).not.toBeNull();
            done();
        })
    });
});
