"""Unit tests of commenting managers."""

import unittest
from dlkit.runtime import PROXY_SESSION, proxy_example
from dlkit.runtime.managers import Runtime
REQUEST = proxy_example.SimpleRequest()
CONDITION = PROXY_SESSION.get_proxy_condition()
CONDITION.set_http_request(REQUEST)
PROXY = PROXY_SESSION.get_proxy(CONDITION)

from dlkit.primordium.type.primitives import Type
DEFAULT_TYPE = Type(**{'identifier': 'DEFAULT', 'namespace': 'DEFAULT', 'authority': 'DEFAULT',})

from dlkit.abstract_osid.type.objects import TypeList as abc_type_list
from dlkit.abstract_osid.osid import errors




class TestCommentingProfile(unittest.TestCase):
    """Tests for CommentingProfile"""

    @classmethod
    def setUpClass(cls):
        cls.mgr = Runtime().get_service_manager('COMMENTING', proxy=PROXY, implementation='TEST_SERVICE')



    def test_supports_comment_lookup(self):
        """Tests supports_comment_lookup"""
        self.assertTrue(isinstance(self.mgr.supports_comment_lookup(), bool))

    def test_supports_comment_query(self):
        """Tests supports_comment_query"""
        self.assertTrue(isinstance(self.mgr.supports_comment_query(), bool))

    def test_supports_comment_admin(self):
        """Tests supports_comment_admin"""
        self.assertTrue(isinstance(self.mgr.supports_comment_admin(), bool))

    def test_supports_book_lookup(self):
        """Tests supports_book_lookup"""
        self.assertTrue(isinstance(self.mgr.supports_book_lookup(), bool))

    def test_supports_book_admin(self):
        """Tests supports_book_admin"""
        self.assertTrue(isinstance(self.mgr.supports_book_admin(), bool))

    def test_supports_book_hierarchy(self):
        """Tests supports_book_hierarchy"""
        self.assertTrue(isinstance(self.mgr.supports_book_hierarchy(), bool))

    def test_supports_book_hierarchy_design(self):
        """Tests supports_book_hierarchy_design"""
        self.assertTrue(isinstance(self.mgr.supports_book_hierarchy_design(), bool))

    def test_get_comment_record_types(self):
        """Tests get_comment_record_types"""
        self.assertTrue(isinstance(self.mgr.get_comment_record_types(), abc_type_list))

    def test_get_comment_search_record_types(self):
        """Tests get_comment_search_record_types"""
        self.assertTrue(isinstance(self.mgr.get_comment_search_record_types(), abc_type_list))

    def test_get_book_record_types(self):
        """Tests get_book_record_types"""
        self.assertTrue(isinstance(self.mgr.get_book_record_types(), abc_type_list))

    def test_get_book_search_record_types(self):
        """Tests get_book_search_record_types"""
        self.assertTrue(isinstance(self.mgr.get_book_search_record_types(), abc_type_list))


class TestCommentingManager(unittest.TestCase):
    """Tests for CommentingManager"""

    # Implemented from resource.ResourceManager
    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('COMMENTING', implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_book_form_for_create([])
        create_form.display_name = 'Test Book'
        create_form.description = 'Test Book for commenting manager tests'
        catalog = cls.svc_mgr.create_book(create_form)
        cls.catalog_id = catalog.get_id()
        # cls.mgr = Runtime().get_manager('COMMENTING', 'TEST_JSON_1', (3, 0, 0))

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_book(cls.catalog_id)



    def test_get_comment_lookup_session(self):
        """Tests get_comment_lookup_session"""
        # if self.mgr.supports_comment_lookup():
        #     self.mgr.get_comment_lookup_session()
        if self.svc_mgr.supports_comment_lookup():
            self.svc_mgr.get_comment_lookup_session()

    def test_get_comment_lookup_session_for_book(self):
        """Tests get_comment_lookup_session_for_book"""
        # if self.mgr.supports_comment_lookup():
        #     self.mgr.get_comment_lookup_session_for_book(self.catalog_id)
        # with self.assertRaises(errors.NullArgument):
        #     self.mgr.get_comment_lookup_session_for_book()
        if self.svc_mgr.supports_comment_lookup():
            self.svc_mgr.get_comment_lookup_session_for_book(self.catalog_id)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.get_comment_lookup_session_for_book()

    def test_get_comment_query_session(self):
        """Tests get_comment_query_session"""
        # if self.mgr.supports_comment_query():
        #     self.mgr.get_comment_query_session()
        if self.svc_mgr.supports_comment_query():
            self.svc_mgr.get_comment_query_session()

    def test_get_comment_query_session_for_book(self):
        """Tests get_comment_query_session_for_book"""
        # if self.mgr.supports_comment_query():
        #     self.mgr.get_comment_query_session_for_book(self.catalog_id)
        # with self.assertRaises(errors.NullArgument):
        #     self.mgr.get_comment_query_session_for_book()
        if self.svc_mgr.supports_comment_query():
            self.svc_mgr.get_comment_query_session_for_book(self.catalog_id)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.get_comment_query_session_for_book()

    @unittest.skip('unimplemented test')
    def test_get_comment_admin_session(self):
        """Tests get_comment_admin_session"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_comment_admin_session_for_book(self):
        """Tests get_comment_admin_session_for_book"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_book_lookup_session(self):
        """Tests get_book_lookup_session"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_book_admin_session(self):
        """Tests get_book_admin_session"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_book_hierarchy_session(self):
        """Tests get_book_hierarchy_session"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_book_hierarchy_design_session(self):
        """Tests get_book_hierarchy_design_session"""
        pass

    def test_get_commenting_batch_manager(self):
        """Tests get_commenting_batch_manager"""
        # if self.mgr.supports_commenting_batch():
        #     self.mgr.get_commenting_batch_manager()
        if self.svc_mgr.supports_commenting_batch():
            self.svc_mgr.get_commenting_batch_manager()


class TestCommentingProxyManager(unittest.TestCase):
    """Tests for CommentingProxyManager"""

    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('COMMENTING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_book_form_for_create([])
        create_form.display_name = 'Test Book'
        create_form.description = 'Test Book for commenting proxy manager tests'
        catalog = cls.svc_mgr.create_book(create_form)
        cls.catalog_id = catalog.get_id()
        # cls.mgr = Runtime().get_proxy_manager('COMMENTING', 'TEST_JSON_1', (3, 0, 0))

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_book(cls.catalog_id)



    def test_get_comment_lookup_session(self):
        """Tests get_comment_lookup_session"""
        # if self.mgr.supports_comment_lookup():
        #     self.mgr.get_comment_lookup_session(PROXY)
        # with self.assertRaises(errors.NullArgument):
        #     self.mgr.get_comment_lookup_session()
        if self.svc_mgr.supports_comment_lookup():
            self.svc_mgr.get_comment_lookup_session(PROXY)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.get_comment_lookup_session()

    def test_get_comment_lookup_session_for_book(self):
        """Tests get_comment_lookup_session_for_book"""
        # if self.mgr.supports_comment_lookup():
        #     self.mgr.get_comment_lookup_session_for_book(self.catalog_id, PROXY)
        # with self.assertRaises(errors.NullArgument):
        #     self.mgr.get_comment_lookup_session_for_book()
        if self.svc_mgr.supports_comment_lookup():
            self.svc_mgr.get_comment_lookup_session_for_book(self.catalog_id, PROXY)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.get_comment_lookup_session_for_book()

    def test_get_comment_query_session(self):
        """Tests get_comment_query_session"""
        # if self.mgr.supports_comment_query():
        #     self.mgr.get_comment_query_session(PROXY)
        # with self.assertRaises(errors.NullArgument):
        #     self.mgr.get_comment_query_session()
        if self.svc_mgr.supports_comment_query():
            self.svc_mgr.get_comment_query_session(PROXY)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.get_comment_query_session()

    def test_get_comment_query_session_for_book(self):
        """Tests get_comment_query_session_for_book"""
        # if self.mgr.supports_comment_query():
        #     self.mgr.get_comment_query_session_for_book(self.catalog_id, PROXY)
        # with self.assertRaises(errors.NullArgument):
        #     self.mgr.get_comment_query_session_for_book()
        if self.svc_mgr.supports_comment_query():
            self.svc_mgr.get_comment_query_session_for_book(self.catalog_id, PROXY)
        with self.assertRaises(errors.NullArgument):
            self.svc_mgr.get_comment_query_session_for_book()

    @unittest.skip('unimplemented test')
    def test_get_comment_admin_session(self):
        """Tests get_comment_admin_session"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_comment_admin_session_for_book(self):
        """Tests get_comment_admin_session_for_book"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_book_lookup_session(self):
        """Tests get_book_lookup_session"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_book_admin_session(self):
        """Tests get_book_admin_session"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_book_hierarchy_session(self):
        """Tests get_book_hierarchy_session"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_book_hierarchy_design_session(self):
        """Tests get_book_hierarchy_design_session"""
        pass

    def test_get_commenting_batch_proxy_manager(self):
        """Tests get_commenting_batch_proxy_manager"""
        # if self.mgr.supports_commenting_batch():
        #     self.mgr.get_commenting_batch_proxy_manager()
        if self.svc_mgr.supports_commenting_batch():
            self.svc_mgr.get_commenting_batch_proxy_manager()
