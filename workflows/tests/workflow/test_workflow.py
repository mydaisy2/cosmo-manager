########
# Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

__author__ = 'idanmo'

from testenv import TestCase
from testenv import get_resource as resource
from testenv import deploy_application as deploy


class TestRuoteWorkflows(TestCase):

    def test_execute_operation(self):
        dsl_path = resource("dsl/basic.yaml")
        deploy(dsl_path)

        from cosmo.cloudmock.tasks import get_machines
        result = get_machines.apply_async()
        machines = result.get(timeout=10)

        self.assertEquals(1, len(machines))

    def test_dependencies_order_with_two_nodes(self):
        dsl_path = resource("dsl/dependencies-order-with-two-nodes.yaml")
        deploy(dsl_path)

        from cosmo.testmockoperations.tasks import get_state as testmock_get_state
        states = testmock_get_state.apply_async().get(timeout=10)
        self.assertEquals(2, len(states))
        self.assertEquals('mock_app.containing_node', states[0]['id'])
        self.assertEquals('mock_app.contained_in_node', states[1]['id'])

    def test_cloudify_runtime_properties_injection(self):
        dsl_path = resource("dsl/dependencies-order-with-two-nodes.yaml")
        deploy(dsl_path)

        from cosmo.testmockoperations.tasks import get_state as testmock_get_state
        states = testmock_get_state.apply_async().get(timeout=10)
        node_runtime_props = states[1]['relationships']['mock_app.containing_node']
        self.assertEquals('value1', node_runtime_props['property1'])
        self.assertEquals('true', node_runtime_props['reachable'])
        self.assertEquals(2, len(node_runtime_props))



