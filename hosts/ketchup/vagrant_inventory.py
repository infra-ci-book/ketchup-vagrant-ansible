#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Ansible Dynamic Inventory Program for Vagrant.
# It is able to parse the output from
#  `vagrant global-status --machine-readable` and convert data structure
#  to JSON format.
#
# Link: https://www.vagrantup.com/docs/cli/machine-readable.html
#
#
# Copyright 2018 Hideki Saito <saito@fgrep.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import subprocess
import re

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


class VagrantMissingHostException(Exception):
    pass


class VagrantInventory(object):
    __name__ = 'VagrantInventory'
    vagrant_stat_cmd = ['vagrant', 'global-status', '--machine-readable']
    ssh_user = 'vagrant'

    def __init__(self):
        self.parse_cli_args()
        vagrant_output = self.get_vagrant_output()
        self.inventory = self.get_inventory(vagrant_output)

    def show(self):
        print_data = None
        if self.args.host:
            print_data = self.get_host_info(self.args.host)
        elif self.args.list:
            print_data = self.inventory
        return json.dumps(print_data, indent=2)

    def get_vagrant_output(self):
        output = subprocess.check_output(
            self.vagrant_stat_cmd).decode('utf-8').split('\n')
        parsed_output = self._parse_vagrant_output(output)
        return parsed_output

    def get_inventory(self, vagrant_output):
        inventory = {}
        default_info = {'hosts': [], 'vars': {}}
        meta_info = {}

        inventory['_meta'] = {'hostvars': {}}
        for line in vagrant_output:
            vm_provider = line['provider']
            vm_provider_combined = '{provider}_combined'.format(
                provider=vm_provider)
            vm_state = line['state']
            vm_state_combined = '{state}_combined'.format(state=vm_state)
            if vm_provider not in inventory.keys():
                inventory[vm_provider] = {'hosts': [], 'vars': {}}
                inventory[vm_provider_combined] = {'hosts': [], 'vars': {}}
            if vm_state not in inventory.keys():
                inventory[vm_state] = {'hosts': [], 'vars': {}}
                inventory[vm_state_combined] = {'hosts': [], 'vars': {}}

        for line in vagrant_output:
            vm_provider = line['provider']
            vm_provider_combined = '{provider}_combined'.format(
                provider=line['provider'])
            vm_id = line['id']
            vm_name = line['name']
            vm_state = line['state']
            vm_state_combined = '{state}_combined'.format(state=vm_state)
            vm_directory = line['directory']
            vm_name_id = '{name}_{id}'.format(name=vm_name, id=vm_id)

            ssh_private_key_path = \
                '.vagrant/machines/{host}/virtualbox/private_key'.format(
                    host=vm_name)

            inventory[vm_provider]['hosts'].append(vm_name)
            inventory[vm_provider]['vars']['provider'] = vm_provider
            inventory[vm_provider_combined]['hosts'].append(vm_name_id)
            inventory[vm_provider_combined]['provider'] = vm_provider

            inventory[vm_state]['hosts'].append(vm_name)
            inventory[vm_state]['vars']['provider'] = vm_provider
            inventory[vm_state_combined]['hosts'].append(vm_name_id)
            inventory[vm_state_combined]['provider'] = vm_provider

            meta_info['id'] = vm_id
            meta_info['name'] = vm_name
            meta_info['provider'] = vm_provider
            meta_info['state'] = vm_state
            meta_info['directory'] = vm_directory
            meta_info['ansible_ssh_user'] = self.ssh_user
            meta_info['ansible_ssh_private_key_file'] = \
                '{basedir}/{privkey}'.format(
                    basedir=line['directory'], privkey=ssh_private_key_path)
            inventory['_meta']['hostvars'][vm_name] = meta_info
            inventory['_meta']['hostvars'][vm_name_id] = meta_info
            meta_info = {}
        return inventory

    def get_host_info(self, host):
        if host in self.inventory['_meta']['hostvars']:
            return self.inventory['_meta']['hostvars'][host]
        else:
            raise VagrantMissingHostException('%s not found' % host)

    def parse_cli_args(self):
        parser = argparse.ArgumentParser(
            description='Produce an Ansible Inventory file')
        parser.add_argument(
            '--list',
            action='store_true',
            default=True,
            help='List instances (default: True)')
        parser.add_argument(
            '--host',
            action='store',
            help='Get all the variables about a specific instance')
        self.args = parser.parse_args()

    def _parse_vagrant_output(self, buffer):
        records = []
        record = []

        begin_record = '^-+$'
        end_record = r'^ \\n.*$'

        begin = False
        for line in buffer:
            columns = line.split(',')
            if re.match(begin_record, columns[4].rstrip(' ')):
                begin = True
                continue
            if not begin:
                continue
            if re.match(end_record, columns[4].rstrip(' ')):
                break
            if columns[4] == '':
                records.append(record)
                record = []
            else:
                record.append(columns[4].rstrip(' '))
        return self._convert_vagrant_output(records)

    def _convert_vagrant_output(self, parsed_buffer):
        records = []
        record = {}

        for line in parsed_buffer:
            record['id'] = line[0]
            record['name'] = line[1]
            record['provider'] = line[2]
            record['state'] = line[3]
            record['directory'] = line[4]
            records.append(record)
            record = {}

        return records


if __name__ == '__main__':
    print(VagrantInventory().show())

#
# EOF
#
