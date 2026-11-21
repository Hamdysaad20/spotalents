#!/usr/bin/env python3
"""
DRY Footer Synchronizer for SpotTalents.
Reads the single source of truth from components/footer.html
and synchronizes it across all HTML pages in the project (including blog).
"""

import os
import sys

# Delegate directly to sync_components with footer flag
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))

from sync_components import sync_all

if __name__ == "__main__":
    sync_all(sync_nav=False, sync_call_to_action=False, sync_foot=True)
