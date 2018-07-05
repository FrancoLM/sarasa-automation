import logging

from behave import step

from features.steps.utils.remote_connection.linux_ssh_client import SSHClient


@step(u'I login via SSH to "{ip}":"{port}" as user "{ssh_user}" using key "{ssh_pkey}"')
def step_impl(context, ip, port, ssh_user, ssh_pkey):
    context.ssh_session = SSHClient(ip, port, ssh_user, ssh_pkey, password_auth=False)
    assert context.ssh_session, "SSH Session could not be established"


@step(u'the SSH session is established')
def step_impl(context):
    try:
        context.ssh_session
    except:
        error = "SSH Session unavailable"
        raise Exception(error)


@step(u'I login via SSH to "{ip}":"{port}" as user "{ssh_user}" and password "{ssh_password}"')
@step(u'I take a Galileo device from the device pool')
def step_impl(context, ip, port, ssh_user, ssh_password):
    context.ssh_session = SSHClient(ip, port, ssh_user, ssh_password)
    assert context.ssh_session, "SSH Session could not be established"


@step(u'I copy the file "{file_path}" via SSH')
@step(u'I copy the file "{file_path}" to "{dest_path}" via SSH')
def step_impl(context, file_path, dest_path="."):
    context.execute_steps(u'''Given the SSH session is established''')
    context.ssh_session.copy_file(file_path, dest_path)


@step(u'I send the command "{command}" via SSH')
def step_impl(context, command):
    context.execute_steps(u'''Given the SSH session is established''')
    stdin, stdout, stderr = context.ssh_session.send_command(command)
    logging.info("Output:\n%s" % stdout.read())


@step(u'I send the command "{command}" via SSH as background process')
def step_impl(context, command):
    prefix = "nohup "
    background = " > /dev/null 2>&1 &"
    bg_command = prefix + command + background
    context.execute_steps(u'''Given I send the command "%s" via SSH''' % bg_command)


@step(u'I get the PID of the process "{process}"')
def step_impl(context, process):
    context.execute_steps(u'''Given the SSH session is established''')
    pid = context.ssh_session.get_process_pid(process)
    logging.info("Process PID:\n%s" % pid)


@step(u'I close the SSH connection')
def step_impl(context):
    context.execute_steps(u'''Given the SSH session is established''')
    context.ssh_session.close_session()
