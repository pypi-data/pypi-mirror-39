# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['aria2p']

package_data = \
{'': ['*']}

install_requires = \
['requests']

entry_points = \
{'console_scripts': ['aria2p = aria2p.cli:main']}

setup_kwargs = {
    'name': 'aria2p',
    'version': '0.1.3',
    'description': 'Command-line tool and library to interact with an aria2c daemon process with JSON-RPC.',
    'long_description': '# Aria2p\nCommand-line tool and Python library to interact with an `aria2c` daemon process through JSON-RPC.\n\n# Requirements\n`aria2p` requires Python 3.6. To install Python 3.6, I recommend [`pyenv`](https://github.com/pyenv/pyenv):\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these two lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.7\n\n# make it available globally\npyenv global system 3.6.7\n```\n\n## Installation\nWith `pip`:\n```bash\npython3.6 -m pip install aria2p\n```\n\nWith [`pipx`](https://github.com/cs01/pipx):\n```bash\n# install pipx with the recommended method\ncurl https://raw.githubusercontent.com/cs01/pipx/master/get-pipx.py | python3\n\npipx install --python python3.6 aria2p\n```\n\n## Usage (as a library)\n**This library is still a work in progress. Some things listed here might not be implemented yet.**\n```python\nimport aria2p\n\n# initialization, these are the default values\naria2 = aria2p.API(\n    aria2p.JSONRPCClient(\n        host="http://localhost",\n        port=6800,\n        secret=""\n    )\n)\n\n# list downloads\ndownloads = aria2.get_downloads()\n\nfor download in downloads:\n    print(download.name, download.download_speed)\n    \n# add downloads\nmagnet_uri = "magnet:?xt=urn:..."\n\ndownload = aria2.add_magnet(magnet_uri)\n\n```\n\n## Usage (command-line)\nFor now, the command-line tool can only call methods using the client.\nMore options directly using the API will come later.\n\n```bash\naria2p -m,--method METHOD_NAME [-p,--params PARAMS... | -j,--json-params JSON_STRING]\n```\n\nThe `METHOD_NAME` can be the exact method name, or just the name without the prefix.\nIt is case-insensitive, and dashes and underscores will be removed.\nThe following are all equivalent:\n- `aria2.addUri`\n- `aria2.adduri`\n- `addUri`\n- `ADDURI`\n- `aria2.ADD-URI`\n- `add_uri`\n- `A-d_D-u_R-i` (yes it\'s valid)\n- `A---R---I---A---2.a__d__d__u__r__i` (I think you got it)\n- and even more ugly forms...\n\n### Examples\nList all available methods.\n*This example uses [`jq`](https://github.com/stedolan/jq).*\n```console\n$ aria2p -m listmethods | jq\n[\n  "aria2.addUri",\n  "aria2.addTorrent",\n  "aria2.getPeers",\n  "aria2.addMetalink",\n  "aria2.remove",\n  "aria2.pause",\n  "aria2.forcePause",\n  "aria2.pauseAll",\n  "aria2.forcePauseAll",\n  "aria2.unpause",\n  "aria2.unpauseAll",\n  "aria2.forceRemove",\n  "aria2.changePosition",\n  "aria2.tellStatus",\n  "aria2.getUris",\n  "aria2.getFiles",\n  "aria2.getServers",\n  "aria2.tellActive",\n  "aria2.tellWaiting",\n  "aria2.tellStopped",\n  "aria2.getOption",\n  "aria2.changeUri",\n  "aria2.changeOption",\n  "aria2.getGlobalOption",\n  "aria2.changeGlobalOption",\n  "aria2.purgeDownloadResult",\n  "aria2.removeDownloadResult",\n  "aria2.getVersion",\n  "aria2.getSessionInfo",\n  "aria2.shutdown",\n  "aria2.forceShutdown",\n  "aria2.getGlobalStat",\n  "aria2.saveSession",\n  "system.multicall",\n  "system.listMethods",\n  "system.listNotifications"\n]\n```\n\nList the GIDs (identifiers) of all active downloads.\n*Note that we must give the parameters as a JSON string.*\n```console\n$ aria2p -m tellactive -j \'[["gid"]]\'\n[{"gid": "b686cad55029d4df"}, {"gid": "4b39a1ad8fd94e26"}, {"gid": "9d331cc4b287e5df"}, {"gid": "8c9de0df753a5195"}]\n```\n\nPause a download using its GID.\n*Note that when a single string argument is required, it can be passed directly with `-p`.*\n```console\n$ aria2p -m pause -p b686cad55029d4df\n"b686cad55029d4df"\n```\n\nAdd a download using magnet URIs.\n*This example uses `jq -r` to remove the quotation marks around the result.*\n```console\n$ aria2p -m adduri -j \'[["magnet:?xt=urn:..."]]\' | jq -r\n4b39a1ad8fd94e26f\n```\n\nPurge download results (remove completed downloads from the list).\n```console\n$ aria2p -m purge_download_result\n"OK"\n```\n',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'url': 'https://github.com/pawamoy/aria2p',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
