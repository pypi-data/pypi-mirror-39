# SWToolz-Core API wrapper

Make queries to [Swtools-Core](https://github.com/MXMP/swtoolz-core) (forked from [xcme/swtoolz-core](https://github.com/xcme/swtoolz-core)) easier than ever.

## Install

```bash
pip install swtoolz
```

## Examples

### Enable port 10 on switch 10.90.90.90

```python
from swtoolz import SWToolz

swtoolz_community_number = 2
swtoolz_port = 7377

swt = SWToolz('swtoolz_url', 'swtoolz_user', swtoolz_community_number, swtoolz_port)
swt.change_port_admin_state('10.90.90.90', 10, 'enabled')
```

## Available methods

### get_port_admin_state(device_ip, port_num, media='copper')

Returns admin state of port in human-readable format ('enabled'/'disabled')

### change_port_admin_state(device_ip, port_num, target_state)

Changes admin state of port to `target_state` ('enabled'/'disabled').
