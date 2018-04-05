"""
Runs Default tests
Available Modules: http://testinfra.readthedocs.io/en/latest/modules.html

"""
import os
import testinfra.utils.ansible_runner

TESTINFRA_HOSTS = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_ufw_is_installed(host):
    """
    Tests that ufw is installed
    """

    ufw = host.package("ufw")
    assert ufw.is_installed


def test_ufw_running_and_enabled(host):
    """
    Tests that ufw is running and enabled
    """
    ufw = host.service("ufw")
    assert ufw.is_running
    assert ufw.is_enabled


def test_ufw_firewall_rules_exist(host):
    """
    Tests that ufw firewall allows port 22, 80, and 443
    """
    ssh_rule_str = \
        '-A ufw-user-input -p tcp -m tcp --dport 22 -j ACCEPT'
    http_rule_str = \
        '-A ufw-user-input -p tcp -m tcp --dport 80 -j ACCEPT'
    https_rule_str = \
        '-A ufw-user-input -p tcp -m tcp --dport 443 -j ACCEPT'
    rules = host.iptables.rules()
    assert ssh_rule_str in rules
    assert http_rule_str in rules
    assert https_rule_str in rules
