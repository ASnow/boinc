# This file is part of BOINC.
# http://boinc.berkeley.edu
# Copyright (C) 2016 University of California
#
# BOINC is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# BOINC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with BOINC.  If not, see <http://www.gnu.org/licenses/>.

# test functions for submit_api.py

# YOU MUST CREATE A FILE "test_auth' CONTAINING
#
# project URL
# authenticator of your account

from submit_api import *

# read URL and auth from a file so we don't have to include it here
#
def get_auth():
    with open("test_auth", "r") as f:
        url = (f.readline()).strip()
        auth = (f.readline()).strip()
    return [url, auth]

# make a batch description, to be passed to estimate_batch() or submit_batch()
#
def make_batch_desc():
    file = FILE_DESC()
    file.mode = 'local_staged'
    file.source = 'input'

    job = JOB_DESC()
    job.files = [file]

    batch = BATCH_DESC()
    [batch.project, batch.authenticator] = get_auth()
    batch.app_name = "uppercase"
    batch.batch_name = "blah28"
    batch.jobs = []

    for i in range(2):
        job.command_line = '-i %s' %(i)
        if True:
            job.wu_template = """
<input_template>
    <file_info>
    </file_info>
    <workunit>
        <file_ref>
            <open_name>in</open_name>
        </file_ref>
        <target_nresults>1</target_nresults>
        <min_quorum>1</min_quorum>
        <credit>%d</credit>
        <rsc_fpops_est>   60e9  </rsc_fpops_est>
    </workunit>
</input_template>
""" % (i+1)
        if True:
            job.result_template = """
<output_template>
    <file_info>
        <name><OUTFILE_0/></name>
        <generated_locally/>
        <upload_when_present/>
        <max_nbytes>4000000</max_nbytes>
        <url><UPLOAD_URL/></url>
    </file_info>
    <result>
        <file_ref>
            <file_name><OUTFILE_0/></file_name>
            <open_name>out</open_name>
        </file_ref>
    </result>
</output_template>
"""
        job.rsc_fpops_est = (i+1)*1e9
        batch.jobs.append(copy.copy(job))

    return batch

def test_estimate_batch():
    batch = make_batch_desc()
    #print batch.to_xml("submit")
    r = estimate_batch(batch)
    if check_error(r):
        return
    print 'estimated time: ', r[0].text, ' seconds'

def test_submit_batch():
    batch = make_batch_desc()
    r = submit_batch(batch)
    if check_error(r):
        return
    print 'batch ID: ', r[0].text

def test_query_batches():
    req = REQUEST()
    [req.project, req.authenticator] = get_auth()
    req.get_cpu_time = True
    r = query_batches(req)
    if check_error(r):
        return
    print ET.tostring(r)

def test_query_batch():
    req = REQUEST()
    [req.project, req.authenticator] = get_auth()
    req.batch_id = 271
    req.get_cpu_time = True
    r = query_batch(req)
    if check_error(r):
        return
    print ET.tostring(r)
    print 'njobs: ', r.find('njobs').text
    print 'fraction done: ', r.find('fraction_done').text
    print 'total CPU time: ', r.find('total_cpu_time').text
    # ... various other fields
    print 'jobs:'
    for job in r.findall('job'):
        print '   id: ', job.find('id').text
        print '      n_outfiles: ', job.find('n_outfiles').text
        # ... various other fields

def test_create_batch():
    req = CREATE_BATCH_REQ()
    [req.project, req.authenticator] = get_auth()
    req.app_name = 'uppercase'
    req.batch_name = 'foobar'
    req.expire_time = 0
    r = create_batch(req)
    if check_error(r):
        return
    print 'batch ID: ', r[0].text

def test_abort_batch():
    req = REQUEST()
    [req.project, req.authenticator] = get_auth()
    req.batch_id = 271
    r = abort_batch(req)
    if check_error(r):
        return
    print 'success'

def test_upload_files():
    req = UPLOAD_FILES_REQ()
    [req.project, req.authenticator] = get_auth()
    req.batch_id = 283
    req.local_names = ('updater.cpp', 'kill_wu.cpp')
    req.boinc_names = ('dxxxb_updater.cpp', 'dxxxb_kill_wu.cpp')
    r = upload_files(req)
    if check_error(r):
        return
    print 'upload_files: success'

def test_query_files():
    req = QUERY_FILES_REQ()
    [req.project, req.authenticator] = get_auth()
    req.batch_id = 271
    req.boinc_names = ('dxxx_updater.cpp', 'dxxx_kill_wu.cpp')
    r = query_files(req)
    if check_error(r):
        return
    print 'absent files:'
    for f in r[0]:
        print f.text

def test_get_output_file():
    req = REQUEST()
    [req.project, req.authenticator] = get_auth()
    req.instance_name = 'uppercase_32275_1484961754.784017_0_0';
    req.file_num = 1;
    r = get_output_file(req)
    print(r)

def test_get_output_files():
    req = REQUEST()
    [req.project, req.authenticator] = get_auth()
    req.batch_id = 271
    r = get_output_files(req)
    print(r)

test_submit_batch()
