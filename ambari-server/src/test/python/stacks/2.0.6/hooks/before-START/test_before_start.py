#!/usr/bin/env python

'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from mock.mock import MagicMock, call, patch
from resource_management import *
from stacks.utils.RMFTestCase import *

@patch("os.path.exists", new = MagicMock(return_value=True))
@patch.object(Hook, "run_custom_hook", new = MagicMock())
class TestHookBeforeStart(RMFTestCase):
  def test_hook_default(self):
    self.executeScript("2.0.6/hooks/before-START/scripts/hook.py",
                       classname="BeforeConfigureHook",
                       command="hook",
                       config_file="default.json"
    )
    self.assertResourceCalled('Execute', '/bin/echo 0 > /selinux/enforce',
                              only_if = 'test -f /selinux/enforce',
                              )
    self.assertResourceCalled('Execute', 'mkdir -p /usr/lib/hadoop/lib/native/Linux-i386-32; ln -sf /usr/lib/libsnappy.so /usr/lib/hadoop/lib/native/Linux-i386-32/libsnappy.so',
                              )
    self.assertResourceCalled('Execute', 'mkdir -p /usr/lib/hadoop/lib/native/Linux-amd64-64; ln -sf /usr/lib64/libsnappy.so /usr/lib/hadoop/lib/native/Linux-amd64-64/libsnappy.so',
                              )
    self.assertResourceCalled('Directory', '/var/log/hadoop',
                              owner = 'root',
                              group = 'root',
                              recursive = True,
                              )
    self.assertResourceCalled('Directory', '/var/run/hadoop',
                              owner = 'root',
                              group = 'root',
                              recursive = True,
                              )
    self.assertResourceCalled('Directory', '/tmp/hadoop-hdfs',
                              owner = 'hdfs',
                              recursive = True,
                              )
    self.assertResourceCalled('File', '/etc/hadoop/conf/commons-logging.properties',
                              content = Template('commons-logging.properties.j2'),
                              owner = 'hdfs',
                              )
    self.assertResourceCalled('File', '/etc/hadoop/conf/health_check',
                              content = Template('health_check-v2.j2'),
                              owner = 'hdfs',
                              )
    self.assertResourceCalled('File',
                              '/etc/hadoop/conf/log4j.properties',
                              mode=0644,
                              group='hadoop',
                              owner='hdfs',
                              content='log4jproperties\nline2log4jproperties\nline2'
                              )
    self.assertResourceCalled('File', '/etc/hadoop/conf/hadoop-metrics2.properties',
                              content = Template('hadoop-metrics2.properties.j2'),
                              owner = 'hdfs',
                              )
    self.assertResourceCalled('File', '/etc/hadoop/conf/task-log4j.properties',
                              content = StaticFile('task-log4j.properties'),
                              mode = 0755,
                              )
    self.assertResourceCalled('File', '/etc/hadoop/conf/configuration.xsl',
      owner = 'hdfs',
      group = 'hadoop',
    )
    self.assertResourceCalled('File', '/etc/hadoop/conf/masters',
      owner = 'hdfs',
      group = 'hadoop',
    )
    self.assertResourceCalled('Execute', 'mkdir -p /tmp/HDP-artifacts/;     curl -kf --retry 10     http://c6401.ambari.apache.org:8080/resources//UnlimitedJCEPolicyJDK7.zip -o /tmp/HDP-artifacts//UnlimitedJCEPolicyJDK7.zip',
        environment = {"no_proxy": "c6401.ambari.apache.org"},
        not_if = 'test -e /tmp/HDP-artifacts//UnlimitedJCEPolicyJDK7.zip',
        ignore_failures = True,
        path = ['/bin', '/usr/bin/'],
    )
    self.assertNoMoreResources()

  def test_hook_secured(self):
    self.executeScript("2.0.6/hooks/before-START/scripts/hook.py",
                       classname="BeforeConfigureHook",
                       command="hook",
                       config_file="secured.json"
    )
    self.assertResourceCalled('Execute', '/bin/echo 0 > /selinux/enforce',
                              only_if = 'test -f /selinux/enforce',
                              )
    self.assertResourceCalled('Execute', 'mkdir -p /usr/lib/hadoop/lib/native/Linux-i386-32; ln -sf /usr/lib/libsnappy.so /usr/lib/hadoop/lib/native/Linux-i386-32/libsnappy.so',
                              )
    self.assertResourceCalled('Execute', 'mkdir -p /usr/lib/hadoop/lib/native/Linux-amd64-64; ln -sf /usr/lib64/libsnappy.so /usr/lib/hadoop/lib/native/Linux-amd64-64/libsnappy.so',
                              )
    self.assertResourceCalled('Directory', '/var/log/hadoop',
                              owner = 'root',
                              group = 'root',
                              recursive = True,
                              )
    self.assertResourceCalled('Directory', '/var/run/hadoop',
                              owner = 'root',
                              group = 'root',
                              recursive = True,
                              )
    self.assertResourceCalled('Directory', '/tmp/hadoop-hdfs',
                              owner = 'hdfs',
                              recursive = True,
                              )
    self.assertResourceCalled('File', '/etc/hadoop/conf/commons-logging.properties',
                              content = Template('commons-logging.properties.j2'),
                              owner = 'root',
                              )
    self.assertResourceCalled('File', '/etc/hadoop/conf/health_check',
                              content = Template('health_check-v2.j2'),
                              owner = 'root',
                              )
    self.assertResourceCalled('File',
                              '/etc/hadoop/conf/log4j.properties',
                              mode=0644,
                              group='hadoop',
                              owner='hdfs',
                              content='log4jproperties\nline2log4jproperties\nline2'
                              )
    self.assertResourceCalled('File', '/etc/hadoop/conf/hadoop-metrics2.properties',
                              content = Template('hadoop-metrics2.properties.j2'),
                              owner = 'hdfs',
                              )
    self.assertResourceCalled('File', '/etc/hadoop/conf/task-log4j.properties',
                              content = StaticFile('task-log4j.properties'),
                              mode = 0755,
                              )
    self.assertResourceCalled('File', '/etc/hadoop/conf/configuration.xsl',
                              owner = 'hdfs',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('File', '/etc/hadoop/conf/masters',
                              owner = 'hdfs',
                              group = 'hadoop',
                              )
    self.assertResourceCalled('Execute', 'mkdir -p /tmp/HDP-artifacts/;     curl -kf --retry 10     http://c6401.ambari.apache.org:8080/resources//UnlimitedJCEPolicyJDK7.zip -o /tmp/HDP-artifacts//UnlimitedJCEPolicyJDK7.zip',
        environment = {"no_proxy": "c6401.ambari.apache.org"},
        not_if = 'test -e /tmp/HDP-artifacts//UnlimitedJCEPolicyJDK7.zip',
        ignore_failures = True,
        path = ['/bin', '/usr/bin/'],
    )
    self.assertResourceCalled('Execute', 'rm -f local_policy.jar; rm -f US_export_policy.jar; unzip -o -j -q /tmp/HDP-artifacts//UnlimitedJCEPolicyJDK7.zip',
        path = ['/bin/', '/usr/bin'],
        only_if = 'test -e /usr/jdk64/jdk1.7.0_45/jre/lib/security && test -f /tmp/HDP-artifacts//UnlimitedJCEPolicyJDK7.zip',
        cwd = '/usr/jdk64/jdk1.7.0_45/jre/lib/security',
    )
    self.assertNoMoreResources()
    
def test_that_jce_is_required_in_secured_cluster(self):
  try:
    self.executeScript("2.0.6/hooks/before-START/scripts/hook.py",
                       classname="BeforeStartHook",
                       command="hook",
                       config_file="secured_no_jce_name.json"
    )
    self.fail("Should throw an exception")
  except Fail:
    pass  # Expected
