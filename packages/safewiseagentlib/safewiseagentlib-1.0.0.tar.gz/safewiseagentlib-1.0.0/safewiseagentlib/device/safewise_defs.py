"""SafeWISE-related definitions."""

# pylint: disable=unused-import,import-error
import os
import logging

from safewiselib.client import CallException, PinException
from safewiselib.client import SafeWISEClient as Client
from safewiselib.messages import IdentityType, PassphraseAck, PinMatrixAck, PassphraseStateAck

try:
    from safewiselib.transport import get_transport
except ImportError:
    from safewiselib.device import SafeWISEDevice
    get_transport = SafeWISEDevice.find_by_path

log = logging.getLogger(__name__)


def find_device():
    """Selects a transport based on `SafeWISE_PATH` environment variable.

    If unset, picks first connected device.
    """
    try:
        return get_transport(os.environ.get("SafeWISE_PATH"))
    except Exception as e:  # pylint: disable=broad-except
        log.debug("Failed to find a SafeWISE device: %s", e)
