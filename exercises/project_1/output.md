# Atomicity violation

The following example shows an atomicity violation if the local-read
optimization is enabled.

The execution was as follows:

- `write(0)` to node `1`
- `sleep(1)` to allow catch-up
- `read()` from nodes `1` and `2`, showing consistency

- `write(1)` to node `1`
- `read()` on node `1`, showing new value is stored
- `read()` on node `2`, showing old value is stored

- `sleep(1)` to allow catch-up
- `read()` on node `2`, showing eventual consistency

Hence, the `write(1)` operation was not atomic, as it did not happen at one
point in time across nodes - a read on one node returned the old value `0`
*after* a read on another node had already returned the new value `1`.

The violation might take a few tries to be reproducable, as the vulnerable
window where the write arrived at one host but not the other is rather narrow,
and our interaction with `etcd` via `popen` is rather slow.

```
vagrant@dalg:~/etcdproj$ python example.py 
---
Node 1: write(violation, 0)
Node 1: read(violation) => 0
Node 2: read(violation) => 0
---
Node 1: write(violation, 1)
Node 1: read(violation) => 1
Node 2: read(violation) => 0
---
Node 2: read(violation) => 1
---
```
