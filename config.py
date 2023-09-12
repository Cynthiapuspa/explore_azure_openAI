#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "cee41a5d-e985-43bd-8065-2edc515e98d4")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "aKg8Q~QMyTaM12ywnlzzya_hMwzvTtNpPnDaXdmY")
