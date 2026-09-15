#!/usr/bin/env python3
"""Print a UUID4 for an immutable artifact key using OS randomness."""

import uuid


if __name__ == "__main__":
    print(uuid.uuid4())
