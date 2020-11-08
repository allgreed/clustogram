import { shallowMount } from '@vue/test-utils'
import GraphView from '@/components/GraphView.vue';

describe('GraphView', () => {
  it('shows app name', () => {
    const wrapper = shallowMount(GraphView)
    expect(wrapper.text()).toMatch('Clustogram')
  })
})
