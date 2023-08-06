# medmij-python

Python implementation of de MedMij ZAL, OCL, Whitelist and GNL

## Installation

```shell
$ pip install medmij-lists
```

## Usage

### Whitelist

```python
import urllib.request

import medmij_lists

WHITELIST_URL = "https://afsprakenstelsel.medmij.nl/download/attachments/22348803/MedMij_Whitelist_example.xml"

with urllib.request.urlopen(WHITELIST_URL) as u:
    whitelist_xml = u.read()

whitelist = medmij_lists.Whitelist(xmldata=whitelist_xml)

print('rcf-rso.nl' in whitelist)
print('example.com' in whitelist)
```

Run `whitelist.py`:

```shell
(env) $ python whitelist.py
True
False
```

### ZAL

```python
import urllib.request

import medmij_lists

ZAL_URL = "https://afsprakenstelsel.medmij.nl/download/attachments/22348803/MedMij_Zorgaanbiederslijst_example.xml"

with urllib.request.urlopen(ZAL_URL) as u:
    zal_xml = u.read()

zal = medmij_lists.ZAL(xmldata=zal_xml)
za = zal["umcharderwijk@medmij"]
print(za.gegevensdiensten["4"].authorization_endpoint_uri)
```

Run `zal.py`:

```shell
(env) $ python zal.py
https://medmij.za982.xisbridge.net/oauth/authorize
```

### OCL

```python
import urllib.request

import medmij_lists

OCL_URL = "https://afsprakenstelsel.medmij.nl/download/attachments/22348803/MedMij_OAuthclientlist_example.xml"

with urllib.request.urlopen(OCL_URL) as u:
    ocl_xml = u.read()

ocl = medmij_lists.OAuthclientList(xmldata=ocl_xml)
client = ocl["medmij.deenigeechtepgo.nl"]

print(client.organisatienaam)
```

Run `ocl.py`:

```shell
(env) $ python ocl.py
De Enige Echte PGO
```

### GNL

```python
import urllib.request

import medmij_lists

GNL_URL = "https://afsprakenstelsel.medmij.nl/download/attachments/22348803/MedMij_Gegevensdienstnamenlijst_example.xml"

with urllib.request.urlopen(GNL_URL) as u:
    gnl_xml = u.read()

gnl = medmij_lists.GNL(xmldata=gnl_xml)
gd = gnl["1"]

print(gd.weergavenaam)
```

Run `gnl.py`:

```shell
(env) $ python gnl.py
Basisgegevens Zorg
```

## Version Guidance

This library follows [Semantic Versioning](https://semver.org/).
The versions of the Afsprakenset are mapped to the versions of the library as follows:

| Version Afsprakenset       | Status     | Version library |
|----------------------------|------------|-----------------|
| [Afsprakenset release 1.1] | Latest     | 0.1.*           |

[Afsprakenset release 1.1]: https://afsprakenstelsel.medmij.nl/display/PUBLIC/Afsprakenset+release+1.1
