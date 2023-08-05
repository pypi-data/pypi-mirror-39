import uuid

from lxml import etree as ET
from lxml.builder import E

__all__ = ["Configuration", "Payload", "MCXPayload", "toxml"]


_UUID_NAMESPACE = uuid.UUID("edc00e4a-065a-4f58-ab24-3432f14b9e9e")


def _Element(k, v):
    if isinstance(v, bool):
        v = E.true if v else E.false
    elif isinstance(v, int):
        v = E.integer(str(v))
    elif isinstance(v, float):
        v = E.real(str(v))
    elif isinstance(v, str):
        v = E.string(v)
    elif isinstance(v, list):
        v = E.array(*v)
    # TODO data
    # TODO date
    elif not isinstance(v, ET._Element):
        raise TypeError()
    return E.key(k), v


def _Elements(**kwargs):
    els = []
    for k, v in kwargs.items():
        els.extend(_Element(k, v))
    return els


def Payload(
    PayloadType,
    *,
    PayloadUUID=None,
    PayloadIdentifier=None,
    PayloadVersion=1,
    **kwargs,
):
    if PayloadUUID is None:
        PayloadUUID = uuid.uuid4()
    PayloadUUID = str(PayloadUUID).upper()
    if PayloadIdentifier is None:
        PayloadIdentifier = PayloadType
    PayloadIdentifier = f"{PayloadIdentifier}.{PayloadUUID}"
    return E.dict(
        *_Elements(
            PayloadType=PayloadType,
            PayloadUUID=PayloadUUID,
            PayloadIdentifier=PayloadIdentifier,
            PayloadVersion=PayloadVersion,
            **kwargs,
        )
    )


def MCXPayload(__domain__, **kwargs):
    # fmt: off
    return Payload(
        PayloadType="com.apple.ManagedClient.preferences",
        PayloadContent=E.dict(*_Element(
            __domain__, E.dict(*_Element(
                "Forced", [E.dict(*_Element(
                    "mcx_preference_settings", E.dict(
                        *_Elements(**kwargs)
                    ),
                ))],
            )),
        )),
    )
    # fmt: on


def Configuration(
    PayloadIdentifier,
    *,
    PayloadUUID=None,
    PayloadDisplayName=None,
    PayloadScope="System",
    PayloadRemovalDisallowed=True,
    **kwargs,
):
    if PayloadDisplayName is None:
        PayloadDisplayName = PayloadIdentifier
    if PayloadUUID is None:
        PayloadUUID = uuid.uuid5(_UUID_NAMESPACE, PayloadIdentifier)
    root = E.plist(
        Payload(
            PayloadType="Configuration",
            PayloadUUID=PayloadUUID,
            PayloadIdentifier=PayloadIdentifier,
            PayloadDisplayName=PayloadDisplayName,
            PayloadScope=PayloadScope,
            PayloadRemovalDisallowed=PayloadRemovalDisallowed,
            **kwargs,
        ),
        version="1.0",
    )
    tree = root.getroottree()
    tree.docinfo.public_id = "-//Apple//DTD PLIST 1.0//EN"
    tree.docinfo.system_url = "http://www.apple.com/DTDs/PropertyList-1.0.dtd"
    return tree


def toxml(tree):
    return ET.tostring(
        tree, encoding="UTF-8", xml_declaration=True, pretty_print=True
    )
