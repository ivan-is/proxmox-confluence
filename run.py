from __future__ import print_function
import logging

from logger import setup_logger
from proxmox import Proxmox
from formatter import HtmlFormatter


setup_logger()
logging.getLogger("proxmoxer.core").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    formatter = HtmlFormatter()
    proxmox = Proxmox()
    results = proxmox.get_stats()
    table = formatter.get_table(results)
    # dict(vm._asdict())
    # pp.pprint(results)
    print(table)

