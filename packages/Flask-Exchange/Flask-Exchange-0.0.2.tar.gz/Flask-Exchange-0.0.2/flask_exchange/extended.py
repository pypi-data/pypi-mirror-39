from exchangelib import ExtendedProperty


class ExchangeProcessedExtendedProperty(ExtendedProperty):
    """This prints None for non-flagged messages, 1 for completed and 2 for follow-up."""
    property_tag = 0x1090
    property_type = "Integer"


class ExchangeTransactionIdExtendedProperty(ExtendedProperty):
    """Example of setting a custom header, useful for tracking emails"""
    distinguished_property_set_id = "InternetHeaders"
    property_name = "X-Transaction-Id"
    property_type = "String"


def _register(attr_name, attr_cls):
    return {
        "attr_name": attr_name,
        "attr_cls": attr_cls
    }


exchange_flags = _register("flag", ExchangeProcessedExtendedProperty)
exchange_header_transaction = _register("transaction_id", ExchangeTransactionIdExtendedProperty)

all_extended_properties = (
    exchange_flags,
    exchange_header_transaction
)
