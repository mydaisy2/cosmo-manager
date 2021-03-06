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

class TestMultiInstanceApplication(TestCase):

    def test_deploy_multi_instance_application(self):
        dsl_path = resource("dsl/multi_instance.yaml")
        deploy(dsl_path)

        from cosmo.cloudmock.tasks import get_machines
        result = get_machines.apply_async()
        machines = set(result.get(timeout=10))
        self.assertEquals(2, len(machines))

        from cosmo.testmockoperations.tasks import get_state as get_state
        apps_state = get_state.apply_async().get(timeout=10)
        machines_with_apps = set([])
        for app_state in apps_state:
            host_id = app_state['relationships'].keys()[0]
            machines_with_apps.add(host_id)
        self.assertEquals(machines, machines_with_apps)

        pass