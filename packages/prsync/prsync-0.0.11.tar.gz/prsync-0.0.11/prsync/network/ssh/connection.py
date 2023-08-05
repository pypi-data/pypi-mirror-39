import prsync.network.ssh.ssh_client


def create_connection(server: prsync.network.ssh.ssh_client.SSHClient):
    server.new_session()
    return server


def close_connection(server: prsync.network.ssh.ssh_client.SSHClient):
    server.client.close()
    return 0


def run_cmd(server: prsync.network.ssh.ssh_client.SSHClient, cmd) -> tuple:
    cmd = cmd.strip("\n")
    return server.client.exec_command(cmd)
