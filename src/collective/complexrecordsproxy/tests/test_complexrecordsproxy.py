from collective.complexrecordsproxy import ComplexRecordsProxy
from plone.registry import Registry
from plone.registry.fieldfactory import persistentFieldAdapter
from zope import schema
from zope.component import provideAdapter
from zope.interface import implementer
from zope.interface import Interface

import unittest
import zope.component.testing


class IAddress(Interface):
    street = schema.TextLine(title="Street")
    city = schema.TextLine(title="City", required=False)


class ISettings(Interface):
    title = schema.TextLine(title="Title", required=False)
    address = schema.Object(title="Address", schema=IAddress, required=False)
    addresses = schema.Tuple(
        title="Addresses",
        value_type=schema.Object(schema=IAddress),
        required=False,
        missing_value=(),
    )


@implementer(IAddress)
class Address:
    def __init__(self, street, city=None):
        self.street = street
        self.city = city


COMPLEX_FIELDS = ("address", "addresses")


class TestComplexRecordsProxy(unittest.TestCase):
    def setUp(self):
        zope.component.testing.setUp()
        provideAdapter(persistentFieldAdapter)
        self.registry = Registry()
        # Complex fields can't be records: they are stored as collections.
        self.registry.registerInterface(ISettings, omit=COMPLEX_FIELDS)
        self.settings = self.registry.forInterface(
            ISettings, omit=COMPLEX_FIELDS, factory=ComplexRecordsProxy
        )

    def tearDown(self):
        zope.component.testing.tearDown()

    def record_names(self, interface):
        return sorted(
            name
            for name in self.registry.records.keys()
            if name.startswith(interface.__identifier__)
        )

    def test_scalar_field(self):
        self.assertIsNone(self.settings.title)
        self.settings.title = "Hello"
        self.assertEqual(self.settings.title, "Hello")
        self.assertEqual(self.registry[ISettings.__identifier__ + ".title"], "Hello")

    def test_unknown_field(self):
        with self.assertRaises(AttributeError):
            self.settings.unknown

    def test_object_field_missing(self):
        self.assertIsNone(self.settings.address)

    def test_object_field(self):
        self.settings.address = Address("Rue de l'Ange", "Namur")
        address = self.settings.address
        self.assertIsInstance(address, ComplexRecordsProxy)
        self.assertEqual(address.street, "Rue de l'Ange")
        self.assertEqual(address.city, "Namur")
        self.assertEqual(
            self.record_names(IAddress),
            [
                IAddress.__identifier__ + "/address.city",
                IAddress.__identifier__ + "/address.street",
            ],
        )

    def test_collection_field_missing(self):
        self.assertEqual(self.settings.addresses, ())

    def test_collection_field(self):
        self.settings.addresses = (Address("Rue 1"), Address("Rue 2", "Liège"))
        addresses = self.settings.addresses
        self.assertEqual([a.street for a in addresses], ["Rue 1", "Rue 2"])
        self.assertEqual([a.city for a in addresses], [None, "Liège"])
        self.assertTrue(all(isinstance(a, ComplexRecordsProxy) for a in addresses))

    def test_collection_field_removes_deleted_items(self):
        self.settings.addresses = (Address("Rue 1"), Address("Rue 2"), Address("Rue 3"))
        self.settings.addresses = (Address("Rue 4"),)
        self.assertEqual([a.street for a in self.settings.addresses], ["Rue 4"])
        prefix = IAddress.__identifier__ + ".addresses/"
        self.assertEqual(
            self.record_names(IAddress),
            [prefix + "r0.city", prefix + "r0.street"],
        )
