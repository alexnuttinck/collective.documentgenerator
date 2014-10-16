# -*- coding: utf-8 -*-

from collective.documentgenerator.interfaces import IDocumentGenerationHelper

from collective.documentgenerator.testing import ArchetypesIntegrationTests

from zope.component import queryAdapter


class TestArchetypesHelperView(ArchetypesIntegrationTests):
    """
    Test Archetypes helper view.
    """

    def test_AT_helper_view_registration(self):
        """
        Test that when we query a IDocumentGenerationHelper adpater on an AT object, we get
        the AT implementation of DocumentGenerationHelperView.
        """
        from collective.documentgenerator.helper import ATDocumentGenerationHelperView

        helper_view = queryAdapter(self.AT_topic, IDocumentGenerationHelper)
        msg = "The helper should have been an instance of ATDocumentGenerationHelperView"
        self.assertTrue(isinstance(helper_view, ATDocumentGenerationHelperView), msg)

    def test_AT_proxy_object_registration(self):
        """
        Test that when we query a IDocumentGenerationHelper adpater on an AT object, we get
        the AT implementation of DocumentGenerationHelperView.
        """
        from collective.documentgenerator.helper import ATDisplayProxyObject

        helper_view = queryAdapter(self.AT_topic, IDocumentGenerationHelper)
        proxy = helper_view.obj
        msg = "The proxy object should have been an instance of ATDisplayProxyObject"
        self.assertTrue(isinstance(proxy, ATDisplayProxyObject), msg)

    def test_AT_proxy_object_behaviour(self):
        """
        When trying to access an attribute attr_name on the object, the proxy should return
        display(attr_name) if the attribute is a field of the object schema.
        If attr_name is not a schema's field, it should delegate its access to the real object.

        eg: proxy.title -> proxy.display(field_name='title', context=real_object)
            proxy.some_method() -> real_object.some_method()
        """
        from collective.documentgenerator.interfaces import IDocumentGenerationHelper

        helper_view = queryAdapter(self.AT_topic, IDocumentGenerationHelper)
        proxy = helper_view.obj

        proxy.display = lambda field_name: 'yolo'

        msg = "The proxy should have call proxy.display() method as 'title' is a schema's field."
        self.assertTrue(proxy.description == 'yolo', msg)

        msg = "If we try to access the attribute value through the accessor, it should return \
               the real value stored on the schema's field."
        self.assertTrue(proxy.Title() != 'yolo', msg)


class TestArchetypesHelperViewMethods(ArchetypesIntegrationTests):
    """
    Test Archetypes implementation of helper view's methods.
    """

    def setUp(self):
        super(TestArchetypesHelperViewMethods, self).setUp()
        self.view = queryAdapter(self.AT_topic, IDocumentGenerationHelper)

    def _test_display(self, field_name, expected, to_set=None):
        if to_set is None:
            to_set = expected

        field = self.AT_topic.getField(field_name)
        field.set(self.AT_topic, to_set)

        result = self.view.display(field_name)

        msg = "Expected the of field '{}' to be '{}' but got '{}'".format(
            field_name,
            expected,
            result
        )
        self.assertTrue(expected == result, msg)

    def test_display_method_on_text_field(self):
        field_name = 'description'
        expected_text = 'Yolo!'
        self._test_display(field_name, expected_text)

    def test_display_method_on_select_field(self):
        field_name = 'customViewFields'
        to_set = ['Title', 'Description', 'EffectiveDate']
        expected_text = 'Title, Description, Effective Date'
        self._test_display(field_name, expected_text, to_set=to_set)

    def test_display_method_on_multiselect_field(self):
        """
        """