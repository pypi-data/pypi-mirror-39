# Silkaj
[![Version](https://img.shields.io/pypi/v/silkaj.svg)](https://pypi.python.org/pypi/silkaj) [![License](https://img.shields.io/pypi/l/silkaj.svg)](https://pypi.python.org/pypi/silkaj) [![Python versions](https://img.shields.io/pypi/pyversions/silkaj.svg)](https://pypi.python.org/pypi/silkaj)

- CLI Duniter client written with Python 3.
- [Website](https://silkaj.duniter.org)

## Install
```bash
pip3 install silkaj --user
```

- [Install with Pip](doc/install_pip.md)
- [Install with pipenv](doc/install_pipenv.md)
- [Install with the build](doc/install_build.md)
- [Build an executable with Pyinstaller](doc/build_with_pyinstaller.md)

## Usage
- Get help usage with `-h`, `--help` or `--usage` options, then run:
```bash
silkaj <sub-command>
```

- Will automatically request and post data on `duniter.org 10901` main Ğ1 node.

- Specify a custom node with `-p` option:
```bash
silkaj <sub-command> -p <address>:<port>
```

## Features
- Currency information
- Show amount of account
- Send transaction
- Proof-of-Work difficulties: Σ diffi, Π diffi, match
- network information tab:
 - endpoints, ip6, ip4, domain name and port. Handle nodes sharing same pubkey.
 - pubkey, uid, if member.
 - Proof-of-Work difficulties.
 - generated block and median times.
 - nodes versions.
 - current block n°, hash and time.
- Issuers last ones or all: hash, gentime, mediantime

## Wrappers
- [Install as a drop-down for GNOME Shell with Argos](doc/argos.md)
- [How-to: automate transactions and multi-output](doc/how-to_automate_transactions_and_multi-output.md)
- [Transaction generator written in Shell](https://gitlab.com/jytou/tgen)

## Example
```bash
silkaj network

### 20 peers ups, with 15 members and 5 non-members

|        domain       |      ip4       | port | block |    hash     | gen_time |    uid    |member| pubkey |diffi| version  |
|---------------------+----------------+------+-------+-------------+----------+-----------+------+--------+-----+----------|
| cgeek.fr            | 88.174.120.187 |  9330| 41166 | 000027421F… | 15:59:00 | cgeek     | yes  | HnFcS… |  77 | 0.31.0b6 |
| mirror1.cgeek.fr    | 88.174.120.187 |  9331| 41166 | 000027421F… | 15:59:00 |           | no   | 4jT89… |     | 0.31.0b6 |
| mirror2.cgeek.fr    | 88.174.120.187 |  9332| 41166 | 000027421F… | 15:59:00 |           | no   | AZ2JP… |     | 0.31.0b6 |
| …t.duniter.inso.ovh |                |    80| 41166 | 000027421F… | 15:59:00 | inso      | yes  | 8Fi1V… | 231 | 0.30.17  |
| peer.duniter.org    | 51.255.197.83  |  8999| 41166 | 000027421F… | 15:59:00 |           | no   | BSmby… |     | 0.30.17  |
| desktop.moul.re     | 78.227.107.45  | 24723| 41166 | 000027421F… | 15:59:00 | moul      | yes  | J78bP… |  77 | 0.31.0b7 |
| misc.moul.re        | 78.227.107.45  |  8999| 41166 | 000027421F… | 15:59:00 | moul      | yes  | J78bP… |  77 | 0.31.0b7 |
| test-net.duniter.fr | 88.189.14.141  |  9201| 41166 | 000027421F… | 15:59:00 | kimamila  | yes  | 5ocqz… | 385 | 0.31.0b3 |
| raspi3.cgeek.fr     | 88.174.120.187 |  8999| 41166 | 000027421F… | 15:59:00 |           | no   | G3wQw… |     | 0.31.0a9 |
| duniter.vincentux.fr|                |  8999| 41166 | 000027421F… | 15:59:00 | vincentux | yes  | 9bZEA… |     | 0.30.17  |
| remuniter.cgeek.fr  | 88.174.120.187 | 16120| 41166 | 000027421F… | 15:59:00 | remuniter…| yes  | TENGx… |     | 0.30.17  |
|                     | 88.163.42.58   | 34052| 41166 | 000027421F… | 15:59:00 | cler53    | yes  | 4eDis… |  77 | 0.30.17  |
| suchard.si7v.fr     | 163.172.252.3  |  8999| 41166 | 000027421F… | 15:59:00 | hacky     | yes  | DesHj… |  77 | 0.31.0a8 |
|                     | 87.91.122.123  |  9330| 41166 | 000027421F… | 15:59:00 | mmpio     | yes  | BmDso… | 154 | 0.31.0b3 |
| …er.help-web-low.fr | 151.80.40.148  |  8999| 41166 | 000027421F… | 15:59:00 | pafzedog  | yes  | XeBpJ… | 154 | 0.30.17  |
|                     | 87.90.32.15    |  8999| 41166 | 000027421F… | 15:59:00 | nay4      | yes  | BnSRj… |  77 | 0.31.0a9 |
| duniter.modulix.net | 212.47.227.101 |  9330| 41166 | 000027421F… | 15:59:00 | modulix   | yes  | DeCip… |     | 0.30.17  |
|                     | 88.174.120.187 | 33036| 41166 | 000027421F… | 15:59:00 |           | no   | GNRug… |     | 0.31.0b7 |
| duniter.cco.ovh     | 163.172.176.32 |  8999| 41166 | 000027421F… | 15:59:00 | charles   | yes  | DA4PY… |  77 | 0.31.0a8 |
| duniter.ktorn.com   | 107.170.192.122|  8999| 41166 | 000027421F… | 15:59:00 | ktorn     | yes  | BR5DD… |  77 | 0.30.17  |
```

### Dependencies
Silkaj is based on Python dependencies:

- [Tabulate](https://bitbucket.org/astanin/python-tabulate/overview): to display charts.
- [Commandlines](https://github.com/chrissimpkins/commandlines): to parse command and sub-commands.
- [PyNaCl](https://github.com/pyca/pynacl/): Cryptography (NaCl) library.
- [scrypt](https://bitbucket.org/mhallin/py-scrypt): scrypt key derivation function.
- [pyaes](https://github.com/ricmoo/pyaes): Pure-Python implementation of AES

### Names
I wanted to call that program:
- bamiyan
- margouillat
- lsociety
- cashmere

I finally called it `Silkaj` as `Silk` in esperanto.
