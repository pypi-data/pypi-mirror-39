# -*- coding: utf-8 -*- #
#
# hexfarm/condor.py
#
#
# MIT License
#
# Copyright (c) 2018 Brandon Gomes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
Utilities for the HTCondor Parallel Computing Framework.

"""

try:
    import htcondor as _condor
except ImportError:
    _condor = None


'''
import sys
import subprocess

from dataclasses import dataclass


@dataclass
class User:
    """"""

    name: str


class Command:
    """"""

    PREFIX = 'condor_'

    def __init__(self, name, *args, **kwargs):
        """"""
        self.name = name

    def __call__(self, *args, **kwargs):
        """"""

    @property
    def full_name(self):
        """"""
        return PREFIX + self.name

    @property
    def docs(self):
        """"""
        return self('-help')

    @property
    def man(self):
        """"""
        return _run('man ' + self.name)



class Job:
    """"""

    def __init__(self, id):
        """"""
        self.id = id
        self.owner = ''
        self.submitted = ''

    @property
    def running_time(self):
        """"""




advertise = Command('advertise')
c_gahp = Command('c-gahp')
c_gahp_worker_thread = Command('c-gahp_worker_thread')
checkpoint = Command('checkpoint')
check_userlogs = Command('check_userlogs')
ckpt_server = Command('ckpt_server')
cod = Command('cod')
collector = Command('collector')
compile = Command('compile')
configure = Command('configure')
config_val = Command('config_val')
continue_ = Command('continue')
credd = Command('credd')
dagman = Command('dagman')
drain = Command('drain')
fetchlog = Command('fetchlog')
findhost = Command('findhost')
ft_gahp = Command('ft-gahp')
gather_info = Command('gather_info')
gridmanager = Command('gridmanager')
gridshell = Command('gridshell')
had = Command('had')
history = Command('history')
hold = Command('hold')
init = Command('init')
install = Command('install')
kbdd = Command('kbdd')
master = Command('master')
master_s = Command('master_s')
negotiator = Command('negotiator')
off = Command('off')
on = Command('on')
ping = Command('ping')
power = Command('power')
preen = Command('preen')
prio = Command('prio')
procd = Command('procd')
q = Command('q')
qedit = Command('qedit')
qsub = Command('qsub')
reconfig = Command('reconfig')
release = Command('release')
replication = Command('replication')
reschedule = Command('reschedule')
restart = Command('restart')
rm = Command('rm')
root_switchboard = Command('root_switchboard')
router_history = Command('router_history')
router_q = Command('router_q')
router_rm = Command('router_rm')
run = Command('run')
schedd = Command('schedd')
set_shutdown = Command('set_shutdown')
shadow = Command('shadow')
shadow_s = Command('shadow_s')
# shadow.std
ssh_to_job = Command('ssh_to_job')
startd = Command('startd')
starter = Command('starter')
# starter.std
stats = Command('stats')
status = Command('status')
store_cred = Command('store_cred')
submit = Command('submit')
submit_dag = Command('submit_dag')
suspend = Command('suspend')
tail = Command('tail')
test_match = Command('test_match')
transferd = Command('transferd')
transfer_data = Command('transfer_data')
updates_stats = Command('updates_stats')
userlog = Command('userlog')
userlog_job_counter = Command('userlog_job_counter')
userprio = Command('userprio')
vacate = Command('vacate')
vacate_job = Command('vacate_job')
version = Command('version')
vm_gahp = Command('vm-gahp')
vm_gahp_vmware = Command('vm-gahp-vmware')
vm_vmware = Command('vm_vmware')
# vm_vmware.pl
wait = Command('wait')
who = Command('who')
'''
