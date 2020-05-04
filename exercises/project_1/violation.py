import subprocess
import time

ETCD_CTL = './etcdctl'

# Assumes that node `n` runs on port `1000n`
ENDPOINT_ARG = '--endpoints=127.0.0.1:1000{}'

# Serializable consistency (local read optimization)
CONSISTENCY_ARG = '--consistency=s'

# Print only values (doh)
OUTPUT_ARG = '--print-value-only'

def write(k, v, n=1):
    proc = subprocess.Popen(
            [
                ETCD_CTL,
                ENDPOINT_ARG.format(n),
                'put',
                str(k),
                str(v),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
    )
    out, err = proc.communicate()

    print("Node {}: write({}, {})".format(n, k, v))

def read(k, n=1):
    proc = subprocess.Popen(
            [
                ETCD_CTL,
                ENDPOINT_ARG.format(n),
                'get',
                CONSISTENCY_ARG,
                OUTPUT_ARG,
                str(k),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
    )
    out, err = proc.communicate()

    v = out.rstrip()
    print("Node {}: read({}) => {}".format(n, k, v))

def main():
    k = 'violation'

    print('---')
    write(k, 0)
    # Give ETCD time to catch up in spite of artificial delays
    time.sleep(1)
    read(k, n=1)
    read(k, n=2)
    print('---')

    write(k, 1, n=1)
    read(k, n=1)
    read(k, n=2)
    print('---')

    time.sleep(1)
    read(k, n=2)
    print('---')

if __name__ == "__main__":
    main()
