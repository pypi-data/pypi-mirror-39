# Classes for Accessing the systemd Configuration Files

A collection of classes for accessing the systemd configuration files.

Only tested with Python 3.6 on Debian 9.5.

## Installation

pip install sysdfiles

## Documentation

* [Wiki](https://github.com/ShawnBaker/sysdfiles/wiki)
* [Release Notes](https://github.com/ShawnBaker/sysdfiles/blob/master/release-notes.md)

## Usage

```
from sysdfiles import NetworkFile

network = NetworkFile('/etc/systemd/network/lan.network')
print(network.match_name)
print(network.match_mac_address)
network.network_dhcp = ['8.8.8.8', '8.8.4.4']
network.network_dhcp_server = True
network.dhcp_server_emit_dns = True
network.dhcp_server_dns = '192.168.0.1'
network.route_metric = 10
network.save()
```

## Copyright and License

Copyright &copy; 2018 Shawn Baker using the [MIT License](https://opensource.org/licenses/MIT).
