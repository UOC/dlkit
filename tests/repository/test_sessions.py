"""Unit tests of repository sessions."""


import unittest


from dlkit.abstract_osid.hierarchy.objects import Hierarchy
from dlkit.abstract_osid.id.objects import IdList
from dlkit.abstract_osid.osid import errors
from dlkit.abstract_osid.osid.objects import OsidForm
from dlkit.abstract_osid.osid.objects import OsidNode
from dlkit.abstract_osid.repository import objects as ABCObjects
from dlkit.abstract_osid.repository import queries as ABCQueries
from dlkit.json_.id.objects import IdList
from dlkit.primordium.id.primitives import Id
from dlkit.primordium.type.primitives import Type
from dlkit.runtime import PROXY_SESSION, proxy_example
from dlkit.runtime.managers import Runtime


REQUEST = proxy_example.SimpleRequest()
CONDITION = PROXY_SESSION.get_proxy_condition()
CONDITION.set_http_request(REQUEST)
PROXY = PROXY_SESSION.get_proxy(CONDITION)

DEFAULT_TYPE = Type(**{'identifier': 'DEFAULT', 'namespace': 'DEFAULT', 'authority': 'DEFAULT'})
DEFAULT_GENUS_TYPE = Type(**{'identifier': 'DEFAULT', 'namespace': 'GenusType', 'authority': 'ODL.MIT.EDU'})
ALIAS_ID = Id(**{'identifier': 'ALIAS', 'namespace': 'ALIAS', 'authority': 'ALIAS'})
NEW_TYPE = Type(**{'identifier': 'NEW', 'namespace': 'MINE', 'authority': 'YOURS'})
NEW_TYPE_2 = Type(**{'identifier': 'NEW 2', 'namespace': 'MINE', 'authority': 'YOURS'})
DEFAULT_GENUS_TYPE = Type(**{'identifier': 'DEFAULT', 'namespace': 'GenusType', 'authority': 'DLKIT.MIT.EDU'})
AGENT_ID = Id(**{'identifier': 'jane_doe', 'namespace': 'osid.agent.Agent', 'authority': 'MIT-ODL'})


class TestAssetLookupSession(unittest.TestCase):
    """Tests for AssetLookupSession"""

    @classmethod
    def setUpClass(cls):
        # Implemented from init template for ResourceLookupSession
        cls.asset_list = list()
        cls.asset_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetLookupSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + str(num)
            create_form.description = 'Test Asset for AssetLookupSession tests'
            obj = cls.catalog.create_asset(create_form)
            cls.asset_list.append(obj)
            cls.asset_ids.append(obj.ident)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        # Implemented from init template for ResourceLookupSession
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)

    def test_get_repository_id(self):
        """Tests get_repository_id"""
        # From test_templates/resource.py ResourceLookupSession.get_bin_id_template
        self.assertEqual(self.catalog.get_repository_id(), self.catalog.ident)

    def test_get_repository(self):
        """Tests get_repository"""
        # is this test really needed?
        # From test_templates/resource.py::ResourceLookupSession::get_bin_template
        self.assertIsNotNone(self.catalog)

    def test_can_lookup_assets(self):
        """Tests can_lookup_assets"""
        # From test_templates/resource.py ResourceLookupSession.can_lookup_resources_template
        self.assertTrue(isinstance(self.catalog.can_lookup_assets(), bool))

    def test_use_comparative_asset_view(self):
        """Tests use_comparative_asset_view"""
        # From test_templates/resource.py ResourceLookupSession.use_comparative_resource_view_template
        self.catalog.use_comparative_asset_view()

    def test_use_plenary_asset_view(self):
        """Tests use_plenary_asset_view"""
        # From test_templates/resource.py ResourceLookupSession.use_plenary_resource_view_template
        self.catalog.use_plenary_asset_view()

    def test_use_federated_repository_view(self):
        """Tests use_federated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_federated_bin_view_template
        self.catalog.use_federated_repository_view()

    def test_use_isolated_repository_view(self):
        """Tests use_isolated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_isolated_bin_view_template
        self.catalog.use_isolated_repository_view()

    def test_get_asset(self):
        """Tests get_asset"""
        # From test_templates/resource.py ResourceLookupSession.get_resource_template
        self.catalog.use_isolated_repository_view()
        obj = self.catalog.get_asset(self.asset_list[0].ident)
        self.assertEqual(obj.ident, self.asset_list[0].ident)
        self.catalog.use_federated_repository_view()
        obj = self.catalog.get_asset(self.asset_list[0].ident)
        self.assertEqual(obj.ident, self.asset_list[0].ident)

    def test_get_assets_by_ids(self):
        """Tests get_assets_by_ids"""
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_ids_template
        from dlkit.abstract_osid.repository.objects import AssetList
        objects = self.catalog.get_assets_by_ids(self.asset_ids)
        self.assertTrue(isinstance(objects, AssetList))
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_assets_by_ids(self.asset_ids)
        self.assertTrue(objects.available() > 0)
        self.assertTrue(isinstance(objects, AssetList))

    def test_get_assets_by_genus_type(self):
        """Tests get_assets_by_genus_type"""
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_genus_type_template
        from dlkit.abstract_osid.repository.objects import AssetList
        objects = self.catalog.get_assets_by_genus_type(DEFAULT_GENUS_TYPE)
        self.assertTrue(isinstance(objects, AssetList))
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_assets_by_genus_type(DEFAULT_GENUS_TYPE)
        self.assertTrue(objects.available() > 0)
        self.assertTrue(isinstance(objects, AssetList))

    def test_get_assets_by_parent_genus_type(self):
        """Tests get_assets_by_parent_genus_type"""
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_parent_genus_type_template
        from dlkit.abstract_osid.repository.objects import AssetList
        objects = self.catalog.get_assets_by_parent_genus_type(DEFAULT_GENUS_TYPE)
        self.assertTrue(isinstance(objects, AssetList))
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_assets_by_parent_genus_type(DEFAULT_GENUS_TYPE)
        self.assertTrue(objects.available() == 0)
        self.assertTrue(isinstance(objects, AssetList))

    def test_get_assets_by_record_type(self):
        """Tests get_assets_by_record_type"""
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_record_type_template
        from dlkit.abstract_osid.repository.objects import AssetList
        objects = self.catalog.get_assets_by_record_type(DEFAULT_TYPE)
        self.assertTrue(isinstance(objects, AssetList))
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_assets_by_record_type(DEFAULT_TYPE)
        self.assertTrue(objects.available() == 0)
        self.assertTrue(isinstance(objects, AssetList))

    def test_get_assets_by_provider(self):
        """Tests get_assets_by_provider"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_assets_by_provider(True)

    def test_get_assets(self):
        """Tests get_assets"""
        # From test_templates/resource.py ResourceLookupSession.get_resources_template
        from dlkit.abstract_osid.repository.objects import AssetList
        objects = self.catalog.get_assets()
        self.assertTrue(isinstance(objects, AssetList))
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_assets()
        self.assertTrue(objects.available() > 0)
        self.assertTrue(isinstance(objects, AssetList))

    def test_get_asset_with_alias(self):
        self.catalog.alias_asset(self.asset_ids[0], ALIAS_ID)
        obj = self.catalog.get_asset(ALIAS_ID)
        self.assertEqual(obj.get_id(), self.asset_ids[0])


class TestAssetQuerySession(unittest.TestCase):
    """Tests for AssetQuerySession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceQuerySession::init_template
        cls.asset_list = list()
        cls.asset_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetQuerySession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + color
            create_form.description = (
                'Test Asset for AssetQuerySession tests, did I mention green')
            obj = cls.catalog.create_asset(create_form)
            cls.asset_list.append(obj)
            cls.asset_ids.append(obj.ident)

    def setUp(self):
        # From test_templates/resource.py::ResourceQuerySession::init_template
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceQuerySession::init_template
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)

    def test_get_repository_id(self):
        """Tests get_repository_id"""
        # From test_templates/resource.py ResourceLookupSession.get_bin_id_template
        self.assertEqual(self.catalog.get_repository_id(), self.catalog.ident)

    def test_get_repository(self):
        """Tests get_repository"""
        # is this test really needed?
        # From test_templates/resource.py::ResourceLookupSession::get_bin_template
        self.assertIsNotNone(self.catalog)

    def test_can_search_assets(self):
        """Tests can_search_assets"""
        # From test_templates/resource.py ResourceQuerySession::can_search_resources_template
        self.assertTrue(isinstance(self.session.can_search_assets(), bool))

    def test_use_federated_repository_view(self):
        """Tests use_federated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_federated_bin_view_template
        self.catalog.use_federated_repository_view()

    def test_use_isolated_repository_view(self):
        """Tests use_isolated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_isolated_bin_view_template
        self.catalog.use_isolated_repository_view()

    def test_get_asset_query(self):
        """Tests get_asset_query"""
        # From test_templates/resource.py ResourceQuerySession::get_resource_query_template
        query = self.session.get_asset_query()

    def test_get_assets_by_query(self):
        """Tests get_assets_by_query"""
        # From test_templates/resource.py ResourceQuerySession::get_resources_by_query_template
        # Need to add some tests with string types
        query = self.session.get_asset_query()
        query.match_display_name('orange')
        self.assertEqual(self.catalog.get_assets_by_query(query).available(), 2)
        query.clear_display_name_terms()
        query.match_display_name('blue', match=False)
        self.assertEqual(self.session.get_assets_by_query(query).available(), 3)


class TestAssetSearchSession(unittest.TestCase):
    """Tests for AssetSearchSession"""

    def test_get_asset_search(self):
        """Tests get_asset_search"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_asset_search()

    def test_get_asset_search_order(self):
        """Tests get_asset_search_order"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_asset_search_order()

    def test_get_assets_by_search(self):
        """Tests get_assets_by_search"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_assets_by_search(True, True)

    def test_get_asset_query_from_inspector(self):
        """Tests get_asset_query_from_inspector"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_asset_query_from_inspector(True)


class TestAssetAdminSession(unittest.TestCase):
    """Tests for AssetAdminSession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceAdminSession::init_template
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetAdminSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)

    def setUp(self):
        # From test_templates/resource.py::ResourceAdminSession::init_template
        form = self.catalog.get_asset_form_for_create([])
        form.display_name = 'new Asset'
        form.description = 'description of Asset'
        form.set_genus_type(NEW_TYPE)
        self.osid_object = self.catalog.create_asset(form)
        self.session = self.catalog

    def tearDown(self):
        # From test_templates/resource.py::ResourceAdminSession::init_template
        self.catalog.delete_asset(self.osid_object.ident)

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceAdminSession::init_template
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)

    def test_get_repository_id(self):
        """Tests get_repository_id"""
        # From test_templates/resource.py ResourceLookupSession.get_bin_id_template
        self.assertEqual(self.catalog.get_repository_id(), self.catalog.ident)

    def test_get_repository(self):
        """Tests get_repository"""
        # is this test really needed?
        # From test_templates/resource.py::ResourceLookupSession::get_bin_template
        self.assertIsNotNone(self.catalog)

    def test_can_create_assets(self):
        """Tests can_create_assets"""
        # From test_templates/resource.py::ResourceAdminSession::can_create_resources_template
        self.assertTrue(isinstance(self.catalog.can_create_assets(), bool))

    def test_can_create_asset_with_record_types(self):
        """Tests can_create_asset_with_record_types"""
        # From test_templates/resource.py::ResourceAdminSession::can_create_resource_with_record_types_template
        self.assertTrue(isinstance(self.catalog.can_create_asset_with_record_types(DEFAULT_TYPE), bool))

    def test_get_asset_form_for_create(self):
        """Tests get_asset_form_for_create"""
        # From test_templates/resource.py::ResourceAdminSession::get_resource_form_for_create_template
        form = self.catalog.get_asset_form_for_create([])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())

    def test_create_asset(self):
        """Tests create_asset"""
        # From test_templates/resource.py::ResourceAdminSession::create_resource_template
        from dlkit.abstract_osid.repository.objects import Asset
        self.assertTrue(isinstance(self.osid_object, Asset))
        self.assertEqual(self.osid_object.display_name.text, 'new Asset')
        self.assertEqual(self.osid_object.description.text, 'description of Asset')
        self.assertEqual(self.osid_object.genus_type, NEW_TYPE)

    def test_can_update_assets(self):
        """Tests can_update_assets"""
        # From test_templates/resource.py::ResourceAdminSession::can_update_resources_template
        self.assertTrue(isinstance(self.catalog.can_update_assets(), bool))

    def test_get_asset_form_for_update(self):
        """Tests get_asset_form_for_update"""
        # From test_templates/resource.py::ResourceAdminSession::get_resource_form_for_update_template
        form = self.catalog.get_asset_form_for_update(self.osid_object.ident)
        self.assertTrue(isinstance(form, OsidForm))
        self.assertTrue(form.is_for_update())

    def test_update_asset(self):
        """Tests update_asset"""
        # From test_templates/resource.py::ResourceAdminSession::update_resource_template
        from dlkit.abstract_osid.repository.objects import Asset
        form = self.catalog.get_asset_form_for_update(self.osid_object.ident)
        form.display_name = 'new name'
        form.description = 'new description'
        form.set_genus_type(NEW_TYPE_2)
        updated_object = self.catalog.update_asset(form)
        self.assertTrue(isinstance(updated_object, Asset))
        self.assertEqual(updated_object.ident, self.osid_object.ident)
        self.assertEqual(updated_object.display_name.text, 'new name')
        self.assertEqual(updated_object.description.text, 'new description')
        self.assertEqual(updated_object.genus_type, NEW_TYPE_2)

    def test_can_delete_assets(self):
        """Tests can_delete_assets"""
        # From test_templates/resource.py::ResourceAdminSession::can_delete_resources_template
        self.assertTrue(isinstance(self.catalog.can_delete_assets(), bool))

    def test_delete_asset(self):
        """Tests delete_asset"""
        # From test_templates/resource.py::ResourceAdminSession::delete_resource_template
        form = self.catalog.get_asset_form_for_create([])
        form.display_name = 'new Asset'
        form.description = 'description of Asset'
        form.set_genus_type(NEW_TYPE)
        osid_object = self.catalog.create_asset(form)
        self.catalog.delete_asset(osid_object.ident)
        with self.assertRaises(errors.NotFound):
            self.catalog.get_asset(osid_object.ident)

    def test_can_manage_asset_aliases(self):
        """Tests can_manage_asset_aliases"""
        # From test_templates/resource.py::ResourceAdminSession::can_manage_resource_aliases_template
        self.assertTrue(isinstance(self.catalog.can_manage_asset_aliases(), bool))

    def test_alias_asset(self):
        """Tests alias_asset"""
        # From test_templates/resource.py::ResourceAdminSession::alias_resource_template
        alias_id = Id(self.catalog.ident.namespace + '%3Amy-alias%40ODL.MIT.EDU')
        self.catalog.alias_asset(self.osid_object.ident, alias_id)
        aliased_object = self.catalog.get_asset(alias_id)
        self.assertEqual(aliased_object.ident, self.osid_object.ident)

    def test_can_create_asset_content(self):
        """Tests can_create_asset_content"""
        # From test_templates/resource.py::ResourceAdminSession::can_create_resources_template
        self.assertTrue(isinstance(self.catalog.can_create_asset_content(), bool))

    def test_can_create_asset_content_with_record_types(self):
        """Tests can_create_asset_content_with_record_types"""
        # From test_templates/resource.py::ResourceAdminSession::can_create_resource_with_record_types_template
        self.assertTrue(isinstance(self.catalog.can_create_asset_content_with_record_types(DEFAULT_TYPE), bool))

    def test_get_asset_content_form_for_create(self):
        """Tests get_asset_content_form_for_create"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_asset_content_form_for_create(True, True)

    def test_create_asset_content(self):
        """Tests create_asset_content"""
        with self.assertRaises(errors.Unimplemented):
            self.session.create_asset_content(True)

    def test_can_update_asset_contents(self):
        """Tests can_update_asset_contents"""
        # From test_templates/resource.py::ResourceAdminSession::can_update_resources_template
        self.assertTrue(isinstance(self.catalog.can_update_asset_contents(), bool))

    def test_get_asset_content_form_for_update(self):
        """Tests get_asset_content_form_for_update"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_asset_content_form_for_update(True)

    def test_update_asset_content(self):
        """Tests update_asset_content"""
        with self.assertRaises(errors.Unimplemented):
            self.session.update_asset_content(True)

    def test_can_delete_asset_contents(self):
        """Tests can_delete_asset_contents"""
        # From test_templates/resource.py::ResourceAdminSession::can_delete_resources_template
        self.assertTrue(isinstance(self.catalog.can_delete_asset_contents(), bool))

    def test_delete_asset_content(self):
        """Tests delete_asset_content"""
        with self.assertRaises(errors.Unimplemented):
            self.session.delete_asset_content(True)


class TestAssetNotificationSession(unittest.TestCase):
    """Tests for AssetNotificationSession"""

    @classmethod
    def setUpClass(cls):
        # Implemented from init template for ResourceLookupSession
        cls.asset_list = list()
        cls.asset_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetNotificationSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        for num in [0, 1]:
            create_form = cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + str(num)
            create_form.description = 'Test Asset for AssetNotificationSession tests'
            obj = cls.catalog.create_asset(create_form)
            cls.asset_list.append(obj)
            cls.asset_ids.append(obj.ident)

    def setUp(self):
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        # Implemented from init template for ResourceLookupSession
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)

    def test_get_repository_id(self):
        """Tests get_repository_id"""
        # From test_templates/resource.py ResourceLookupSession.get_bin_id_template
        self.assertEqual(self.catalog.get_repository_id(), self.catalog.ident)

    def test_get_repository(self):
        """Tests get_repository"""
        # is this test really needed?
        # From test_templates/resource.py::ResourceLookupSession::get_bin_template
        self.assertIsNotNone(self.catalog)

    def test_can_register_for_asset_notifications(self):
        """Tests can_register_for_asset_notifications"""
        with self.assertRaises(errors.Unimplemented):
            self.session.can_register_for_asset_notifications()

    def test_use_federated_repository_view(self):
        """Tests use_federated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_federated_bin_view_template
        self.catalog.use_federated_repository_view()

    def test_use_isolated_repository_view(self):
        """Tests use_isolated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_isolated_bin_view_template
        self.catalog.use_isolated_repository_view()

    def test_register_for_new_assets(self):
        """Tests register_for_new_assets"""
        with self.assertRaises(errors.Unimplemented):
            self.session.register_for_new_assets()

    def test_register_for_new_assets_by_genus_type(self):
        """Tests register_for_new_assets_by_genus_type"""
        with self.assertRaises(errors.Unimplemented):
            self.session.register_for_new_assets_by_genus_type(True)

    def test_register_for_changed_assets(self):
        """Tests register_for_changed_assets"""
        with self.assertRaises(errors.Unimplemented):
            self.session.register_for_changed_assets()

    def test_register_for_changed_assets_by_genus_type(self):
        """Tests register_for_changed_assets_by_genus_type"""
        with self.assertRaises(errors.Unimplemented):
            self.session.register_for_changed_assets_by_genus_type(True)

    def test_register_for_changed_asset(self):
        """Tests register_for_changed_asset"""
        with self.assertRaises(errors.Unimplemented):
            self.session.register_for_changed_asset(True)

    def test_register_for_deleted_assets(self):
        """Tests register_for_deleted_assets"""
        with self.assertRaises(errors.Unimplemented):
            self.session.register_for_deleted_assets()

    def test_register_for_deleted_assets_by_genus_type(self):
        """Tests register_for_deleted_assets_by_genus_type"""
        with self.assertRaises(errors.Unimplemented):
            self.session.register_for_deleted_assets_by_genus_type(True)

    def test_register_for_deleted_asset(self):
        """Tests register_for_deleted_asset"""
        with self.assertRaises(errors.Unimplemented):
            self.session.register_for_deleted_asset(True)

    def test_reliable_asset_notifications(self):
        """Tests reliable_asset_notifications"""
        with self.assertRaises(errors.Unimplemented):
            self.session.reliable_asset_notifications()

    def test_unreliable_asset_notifications(self):
        """Tests unreliable_asset_notifications"""
        with self.assertRaises(errors.Unimplemented):
            self.session.unreliable_asset_notifications()

    def test_acknowledge_asset_notification(self):
        """Tests acknowledge_asset_notification"""
        with self.assertRaises(errors.Unimplemented):
            self.session.acknowledge_asset_notification(True)


class TestAssetRepositorySession(unittest.TestCase):
    """Tests for AssetRepositorySession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceBinSession::init_template
        cls.asset_list = list()
        cls.asset_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetRepositorySession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository for Assignment'
        create_form.description = 'Test Repository for AssetRepositorySession tests assignment'
        cls.assigned_catalog = cls.svc_mgr.create_repository(create_form)
        for num in [0, 1, 2]:
            create_form = cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + str(num)
            create_form.description = 'Test Asset for AssetRepositorySession tests'
            obj = cls.catalog.create_asset(create_form)
            cls.asset_list.append(obj)
            cls.asset_ids.append(obj.ident)
        cls.svc_mgr.assign_asset_to_repository(
            cls.asset_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.assign_asset_to_repository(
            cls.asset_ids[2], cls.assigned_catalog.ident)

    def setUp(self):
        # From test_templates/resource.py::ResourceBinSession::init_template
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceBinSession::init_template
        cls.svc_mgr.unassign_asset_from_repository(
            cls.asset_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.unassign_asset_from_repository(
            cls.asset_ids[2], cls.assigned_catalog.ident)
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.assigned_catalog.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)

    def test_can_lookup_asset_repository_mappings(self):
        """Tests can_lookup_asset_repository_mappings"""
        # From test_templates/resource.py::ResourceBinSession::can_lookup_resource_bin_mappings
        result = self.session.can_lookup_asset_repository_mappings()
        self.assertTrue(result)

    def test_use_comparative_repository_view(self):
        """Tests use_comparative_repository_view"""
        # From test_templates/resource.py::BinLookupSession::use_comparative_bin_view_template
        self.svc_mgr.use_comparative_repository_view()

    def test_use_plenary_repository_view(self):
        """Tests use_plenary_repository_view"""
        # From test_templates/resource.py::BinLookupSession::use_plenary_bin_view_template
        self.svc_mgr.use_plenary_repository_view()

    def test_get_asset_ids_by_repository(self):
        """Tests get_asset_ids_by_repository"""
        # From test_templates/resource.py::ResourceBinSession::get_resource_ids_by_bin_template
        objects = self.svc_mgr.get_asset_ids_by_repository(self.assigned_catalog.ident)
        self.assertEqual(objects.available(), 2)

    def test_get_assets_by_repository(self):
        """Tests get_assets_by_repository"""
        # From test_templates/resource.py::ResourceBinSession::get_resources_by_bin_template
        results = self.session.get_assets_by_repository(self.assigned_catalog.ident)
        self.assertTrue(isinstance(results, ABCObjects.AssetList))
        self.assertEqual(results.available(), 2)

    def test_get_asset_ids_by_repositories(self):
        """Tests get_asset_ids_by_repositories"""
        # From test_templates/resource.py::ResourceBinSession::get_resource_ids_by_bins_template
        catalog_ids = [self.catalog.ident, self.assigned_catalog.ident]
        object_ids = self.session.get_asset_ids_by_repositories(catalog_ids)
        self.assertTrue(isinstance(object_ids, IdList))
        # Currently our impl does not remove duplicate objectIds
        self.assertEqual(object_ids.available(), 5)

    def test_get_assets_by_repositories(self):
        """Tests get_assets_by_repositories"""
        # From test_templates/resource.py::ResourceBinSession::get_resources_by_bins_template
        catalog_ids = [self.catalog.ident, self.assigned_catalog.ident]
        results = self.session.get_assets_by_repositories(catalog_ids)
        self.assertTrue(isinstance(results, ABCObjects.AssetList))
        # Currently our impl does not remove duplicate objects
        self.assertEqual(results.available(), 5)

    def test_get_repository_ids_by_asset(self):
        """Tests get_repository_ids_by_asset"""
        # From test_templates/resource.py::ResourceBinSession::get_bin_ids_by_resource_template
        cats = self.svc_mgr.get_repository_ids_by_asset(self.asset_ids[1])
        self.assertEqual(cats.available(), 2)

    def test_get_repositories_by_asset(self):
        """Tests get_repositories_by_asset"""
        # From test_templates/resource.py::ResourceBinSession::get_bins_by_resource_template
        cats = self.svc_mgr.get_repositories_by_asset(self.asset_ids[1])
        self.assertEqual(cats.available(), 2)


class TestAssetRepositoryAssignmentSession(unittest.TestCase):
    """Tests for AssetRepositoryAssignmentSession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceBinAssignmentSession::init_template
        cls.asset_list = list()
        cls.asset_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetRepositoryAssignmentSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository for Assignment'
        create_form.description = 'Test Repository for AssetRepositoryAssignmentSession tests assignment'
        cls.assigned_catalog = cls.svc_mgr.create_repository(create_form)
        for num in [0, 1, 2]:
            create_form = cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + str(num)
            create_form.description = 'Test Asset for AssetRepositoryAssignmentSession tests'
            obj = cls.catalog.create_asset(create_form)
            cls.asset_list.append(obj)
            cls.asset_ids.append(obj.ident)

    def setUp(self):
        # From test_templates/resource.py::ResourceBinAssignmentSession::init_template
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceBinAssignmentSession::init_template
        for obj in cls.catalog.get_assets():
            cls.catalog.delete_asset(obj.ident)
        cls.svc_mgr.delete_repository(cls.assigned_catalog.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)

    def test_can_assign_assets(self):
        """Tests can_assign_assets"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::can_assign_resources_template
        result = self.session.can_assign_assets()
        self.assertTrue(isinstance(result, bool))

    def test_can_assign_assets_to_repository(self):
        """Tests can_assign_assets_to_repository"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::can_assign_resources_to_bin_template
        result = self.session.can_assign_assets_to_repository(self.assigned_catalog.ident)
        self.assertTrue(isinstance(result, bool))

    def test_get_assignable_repository_ids(self):
        """Tests get_assignable_repository_ids"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::get_assignable_bin_ids_template
        # Note that our implementation just returns all catalogIds, which does not follow
        #   the OSID spec (should return only the catalogIds below the given one in the hierarchy.
        results = self.session.get_assignable_repository_ids(self.catalog.ident)
        self.assertTrue(isinstance(results, IdList))

        # Because we're not deleting all banks from all tests, we might
        #   have some crufty banks here...but there should be at least 2.
        self.assertTrue(results.available() >= 2)

    def test_get_assignable_repository_ids_for_asset(self):
        """Tests get_assignable_repository_ids_for_asset"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::get_assignable_bin_ids_for_item_template
        # Note that our implementation just returns all catalogIds, which does not follow
        #   the OSID spec (should return only the catalogIds below the given one in the hierarchy.
        results = self.session.get_assignable_repository_ids_for_asset(self.catalog.ident, self.asset_ids[0])
        self.assertTrue(isinstance(results, IdList))

        # Because we're not deleting all banks from all tests, we might
        #   have some crufty banks here...but there should be at least 2.
        self.assertTrue(results.available() >= 2)

    def test_assign_asset_to_repository(self):
        """Tests assign_asset_to_repository"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::assign_resource_to_bin_template
        results = self.assigned_catalog.get_assets()
        self.assertEqual(results.available(), 0)
        self.session.assign_asset_to_repository(self.asset_ids[1], self.assigned_catalog.ident)
        results = self.assigned_catalog.get_assets()
        self.assertEqual(results.available(), 1)
        self.session.unassign_asset_from_repository(
            self.asset_ids[1],
            self.assigned_catalog.ident)

    def test_unassign_asset_from_repository(self):
        """Tests unassign_asset_from_repository"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::unassign_resource_from_bin_template
        results = self.assigned_catalog.get_assets()
        self.assertEqual(results.available(), 0)
        self.session.assign_asset_to_repository(
            self.asset_ids[1],
            self.assigned_catalog.ident)
        results = self.assigned_catalog.get_assets()
        self.assertEqual(results.available(), 1)
        self.session.unassign_asset_from_repository(
            self.asset_ids[1],
            self.assigned_catalog.ident)
        results = self.assigned_catalog.get_assets()
        self.assertEqual(results.available(), 0)


class TestAssetCompositionSession(unittest.TestCase):
    """Tests for AssetCompositionSession"""

    @classmethod
    def setUpClass(cls):
        cls.asset_list = list()
        cls.asset_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetLookupSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        create_form = cls.catalog.get_composition_form_for_create([])
        create_form.display_name = 'Test Composition for AssetCompositionSession tests'
        create_form.description = 'Test Compposion for AssetCompositionSession tests'
        cls.composition = cls.catalog.create_composition(create_form)
        for num in [0, 1, 2, 3]:
            create_form = cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + str(num)
            create_form.description = 'Test Asset for AssetLookupSession tests'
            obj = cls.catalog.create_asset(create_form)
            cls.asset_list.append(obj)
            cls.asset_ids.append(obj.ident)
            cls.catalog.add_asset(obj.ident, cls.composition.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_repositories():
            for obj in catalog.get_assets():
                catalog.delete_asset(obj.ident)
            for obj in catalog.get_compositions():
                catalog.delete_composition(obj.ident)
            cls.svc_mgr.delete_repository(catalog.ident)

    def test_get_repository_id(self):
        """Tests get_repository_id"""
        # From test_templates/resource.py ResourceLookupSession.get_bin_id_template
        self.assertEqual(self.catalog.get_repository_id(), self.catalog.ident)

    def test_get_repository(self):
        """Tests get_repository"""
        # is this test really needed?
        # From test_templates/resource.py::ResourceLookupSession::get_bin_template
        self.assertIsNotNone(self.catalog)

    def test_can_access_asset_compositions(self):
        """Tests can_access_asset_compositions"""
        with self.assertRaises(errors.Unimplemented):
            self.session.can_access_asset_compositions()

    def test_use_comparative_asset_composition_view(self):
        """Tests use_comparative_asset_composition_view"""
        # From test_templates/resource.py ResourceLookupSession.use_comparative_resource_view_template
        self.catalog.use_comparative_asset_composition_view()

    def test_use_plenary_asset_composition_view(self):
        """Tests use_plenary_asset_composition_view"""
        # From test_templates/resource.py ResourceLookupSession.use_plenary_resource_view_template
        self.catalog.use_plenary_asset_composition_view()

    def test_use_federated_repository_view(self):
        """Tests use_federated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_federated_bin_view_template
        self.catalog.use_federated_repository_view()

    def test_use_isolated_repository_view(self):
        """Tests use_isolated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_isolated_bin_view_template
        self.catalog.use_isolated_repository_view()

    def test_get_composition_assets(self):
        """Tests get_composition_assets"""
        self.assertEqual(self.catalog.get_composition_assets(self.composition.ident).available(), 4)

    def test_get_compositions_by_asset(self):
        """Tests get_compositions_by_asset"""
        self.assertEqual(self.catalog.get_compositions_by_asset(self.asset_ids[0]).available(), 1)
        self.assertEqual(self.catalog.get_compositions_by_asset(self.asset_ids[0]).next().ident, self.composition.ident)


class TestAssetCompositionDesignSession(unittest.TestCase):
    """Tests for AssetCompositionDesignSession"""

    @classmethod
    def setUpClass(cls):
        cls.asset_list = list()
        cls.asset_ids = list()
        cls.composition_list = list()
        cls.composition_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for AssetLookupSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        for num in [0, 1, 2, 3]:
            create_form = cls.catalog.get_asset_form_for_create([])
            create_form.display_name = 'Test Asset ' + str(num)
            create_form.description = 'Test Asset for AssetLookupSession tests' + str(num)
            asset = cls.catalog.create_asset(create_form)
            cls.asset_list.append(asset)
            cls.asset_ids.append(asset.ident)
        for num in [0, 1, 2, 3, 4]:
            create_form = cls.catalog.get_composition_form_for_create([])
            create_form.display_name = 'Test Composition ' + str(num)
            create_form.description = 'Test Compposion for AssetCompositionSession tests ' + str(num)
            composition = cls.catalog.create_composition(create_form)
            cls.composition_list.append(composition)
            cls.composition_ids.append(composition.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_repositories():
            for obj in catalog.get_compositions():
                catalog.delete_composition(obj.ident)
            for obj in catalog.get_assets():
                catalog.delete_asset(obj.ident)
            cls.svc_mgr.delete_repository(catalog.ident)

    def test_get_repository_id(self):
        """Tests get_repository_id"""
        # From test_templates/resource.py ResourceLookupSession.get_bin_id_template
        self.assertEqual(self.catalog.get_repository_id(), self.catalog.ident)

    def test_get_repository(self):
        """Tests get_repository"""
        # is this test really needed?
        # From test_templates/resource.py::ResourceLookupSession::get_bin_template
        self.assertIsNotNone(self.catalog)

    def test_can_compose_assets(self):
        """Tests can_compose_assets"""
        with self.assertRaises(errors.Unimplemented):
            self.session.can_compose_assets()

    def test_add_asset(self):
        """Tests add_asset"""
        for asset_id in self.asset_ids:
            self.catalog.add_asset(asset_id, self.composition_ids[0])
        self.assertEqual(self.catalog.get_composition_assets(self.composition_ids[0]).available(), 4)
        self.assertEqual(self.catalog.get_composition_assets(self.composition_ids[0]).next().display_name.text, 'Test Asset 0')

    def test_move_asset_ahead(self):
        """Tests move_asset_ahead"""
        for asset_id in self.asset_ids:
            self.catalog.add_asset(asset_id, self.composition_ids[1])
        self.catalog.move_asset_ahead(self.asset_ids[2], self.composition_ids[1], self.asset_ids[0])
        first_asset = self.catalog.get_composition_assets(self.composition_ids[1]).next()
        self.assertEqual(first_asset.ident, self.asset_ids[2])

    def test_move_asset_behind(self):
        """Tests move_asset_behind"""
        for asset_id in self.asset_ids:
            self.catalog.add_asset(asset_id, self.composition_ids[2])
        self.catalog.move_asset_behind(self.asset_ids[0], self.composition_ids[2], self.asset_ids[3])
        last_asset = list(self.catalog.get_composition_assets(self.composition_ids[2]))[-1]
        self.assertEqual(last_asset.ident, self.asset_ids[0])

    def test_order_assets(self):
        """Tests order_assets"""
        for asset_id in self.asset_ids:
            self.catalog.add_asset(asset_id, self.composition_ids[3])
        new_order = [self.asset_ids[2], self.asset_ids[3], self.asset_ids[1], self.asset_ids[0]]
        self.catalog.order_assets(new_order, self.composition_ids[3])
        asset_list = list(self.catalog.get_composition_assets(self.composition_ids[3]))
        for num in [0, 1, 2, 3]:
            self.assertEqual(new_order[num], asset_list[num].ident)

    def test_remove_asset(self):
        """Tests remove_asset"""
        for asset_id in self.asset_ids:
            self.catalog.add_asset(asset_id, self.composition_ids[4])
        self.catalog.remove_asset(self.asset_ids[1], self.composition_ids[4])
        self.assertEqual(self.catalog.get_composition_assets(self.composition_ids[4]).available(), 3)


class TestCompositionLookupSession(unittest.TestCase):
    """Tests for CompositionLookupSession"""

    @classmethod
    def setUpClass(cls):
        cls.composition_list = list()
        cls.composition_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for CompositionLookupSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        for num in [0, 1, 2, 3]:
            create_form = cls.catalog.get_composition_form_for_create([])
            create_form.display_name = 'Test Composition ' + str(num)
            create_form.description = 'Test Composition for CompositionLookupSession tests'
            if num > 1:
                create_form.sequestered = True
            obj = cls.catalog.create_composition(create_form)
            cls.composition_list.append(obj)
            cls.composition_ids.append(obj.ident)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_repositories():
            catalog.use_unsequestered_composition_view()
            for obj in catalog.get_compositions():
                catalog.delete_composition(obj.ident)
            cls.svc_mgr.delete_repository(catalog.ident)

    def test_get_repository_id(self):
        """Tests get_repository_id"""
        # From test_templates/resource.py ResourceLookupSession.get_bin_id_template
        self.assertEqual(self.catalog.get_repository_id(), self.catalog.ident)

    def test_get_repository(self):
        """Tests get_repository"""
        # is this test really needed?
        # From test_templates/resource.py::ResourceLookupSession::get_bin_template
        self.assertIsNotNone(self.catalog)

    def test_can_lookup_compositions(self):
        """Tests can_lookup_compositions"""
        # From test_templates/resource.py ResourceLookupSession.can_lookup_resources_template
        self.assertTrue(isinstance(self.catalog.can_lookup_compositions(), bool))

    def test_use_comparative_composition_view(self):
        """Tests use_comparative_composition_view"""
        # From test_templates/resource.py ResourceLookupSession.use_comparative_resource_view_template
        self.catalog.use_comparative_composition_view()

    def test_use_plenary_composition_view(self):
        """Tests use_plenary_composition_view"""
        # From test_templates/resource.py ResourceLookupSession.use_plenary_resource_view_template
        self.catalog.use_plenary_composition_view()

    def test_use_federated_repository_view(self):
        """Tests use_federated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_federated_bin_view_template
        self.catalog.use_federated_repository_view()

    def test_use_isolated_repository_view(self):
        """Tests use_isolated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_isolated_bin_view_template
        self.catalog.use_isolated_repository_view()

    def test_use_active_composition_view(self):
        """Tests use_active_composition_view"""
        # From test_templates/repository.py::CompositionLookupSession::use_active_composition_view_template
        # Ideally also verify the value is set...
        self.catalog.use_active_composition_view()

    def test_use_any_status_composition_view(self):
        """Tests use_any_status_composition_view"""
        # From test_templates/repository.py::CompositionLookupSession::use_any_status_composition_view_template
        # Ideally also verify the value is set...
        self.catalog.use_any_status_composition_view()

    def test_use_sequestered_composition_view(self):
        """Tests use_sequestered_composition_view"""
        # From test_templates/repository.py::CompositionLookupSession::use_sequestered_composition_view
        # Ideally also verify the value is set...
        self.catalog.use_sequestered_composition_view()

    def test_use_unsequestered_composition_view(self):
        """Tests use_unsequestered_composition_view"""
        # From test_templates/repository.py::CompositionLookupSession::use_unsequestered_composition_view
        # Ideally also verify the value is set...
        self.catalog.use_unsequestered_composition_view()

    def test_get_composition(self):
        """Tests get_composition"""
        self.catalog.use_isolated_repository_view()
        obj = self.catalog.get_composition(self.composition_list[0].ident)
        self.assertEqual(obj.ident, self.composition_list[0].ident)
        self.catalog.use_federated_repository_view()
        obj = self.catalog.get_composition(self.composition_list[0].ident)
        self.assertEqual(obj.ident, self.composition_list[0].ident)
        self.catalog.use_sequestered_composition_view()
        obj = self.catalog.get_composition(self.composition_list[1].ident)
        with self.assertRaises(errors.NotFound):
            obj = self.catalog.get_composition(self.composition_list[3].ident)

    def test_get_compositions_by_ids(self):
        """Tests get_compositions_by_ids"""
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_ids_template
        from dlkit.abstract_osid.repository.objects import CompositionList
        objects = self.catalog.get_compositions_by_ids(self.composition_ids)
        self.assertTrue(isinstance(objects, CompositionList))
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_compositions_by_ids(self.composition_ids)
        self.assertTrue(objects.available() > 0)
        self.assertTrue(isinstance(objects, CompositionList))

    def test_get_compositions_by_genus_type(self):
        """Tests get_compositions_by_genus_type"""
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_genus_type_template
        from dlkit.abstract_osid.repository.objects import CompositionList
        objects = self.catalog.get_compositions_by_genus_type(DEFAULT_GENUS_TYPE)
        self.assertTrue(isinstance(objects, CompositionList))
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_compositions_by_genus_type(DEFAULT_GENUS_TYPE)
        self.assertTrue(objects.available() > 0)
        self.assertTrue(isinstance(objects, CompositionList))

    def test_get_compositions_by_parent_genus_type(self):
        """Tests get_compositions_by_parent_genus_type"""
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_parent_genus_type_template
        from dlkit.abstract_osid.repository.objects import CompositionList
        objects = self.catalog.get_compositions_by_parent_genus_type(DEFAULT_GENUS_TYPE)
        self.assertTrue(isinstance(objects, CompositionList))
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_compositions_by_parent_genus_type(DEFAULT_GENUS_TYPE)
        self.assertTrue(objects.available() == 0)
        self.assertTrue(isinstance(objects, CompositionList))

    def test_get_compositions_by_record_type(self):
        """Tests get_compositions_by_record_type"""
        # From test_templates/resource.py ResourceLookupSession.get_resources_by_record_type_template
        from dlkit.abstract_osid.repository.objects import CompositionList
        objects = self.catalog.get_compositions_by_record_type(DEFAULT_TYPE)
        self.assertTrue(isinstance(objects, CompositionList))
        self.catalog.use_federated_repository_view()
        objects = self.catalog.get_compositions_by_record_type(DEFAULT_TYPE)
        self.assertTrue(objects.available() == 0)
        self.assertTrue(isinstance(objects, CompositionList))

    def test_get_compositions_by_provider(self):
        """Tests get_compositions_by_provider"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_compositions_by_provider(True)

    def test_get_compositions(self):
        """Tests get_compositions"""
        from dlkit.abstract_osid.repository.objects import CompositionList
        objects = self.catalog.get_compositions()
        self.assertTrue(isinstance(objects, CompositionList))
        self.catalog.use_federated_repository_view()
        self.catalog.use_unsequestered_composition_view()
        self.assertEqual(self.catalog.get_compositions().available(), 4)
        self.catalog.use_sequestered_composition_view()
        self.assertEqual(self.catalog.get_compositions().available(), 2)


class TestCompositionQuerySession(unittest.TestCase):
    """Tests for CompositionQuerySession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceQuerySession::init_template
        cls.composition_list = list()
        cls.composition_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for CompositionQuerySession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        for color in ['Orange', 'Blue', 'Green', 'orange']:
            create_form = cls.catalog.get_composition_form_for_create([])
            create_form.display_name = 'Test Composition ' + color
            create_form.description = (
                'Test Composition for CompositionQuerySession tests, did I mention green')
            obj = cls.catalog.create_composition(create_form)
            cls.composition_list.append(obj)
            cls.composition_ids.append(obj.ident)

    def setUp(self):
        # From test_templates/resource.py::ResourceQuerySession::init_template
        self.session = self.catalog

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceQuerySession::init_template
        for obj in cls.catalog.get_compositions():
            cls.catalog.delete_composition(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)

    def test_get_repository_id(self):
        """Tests get_repository_id"""
        # From test_templates/resource.py ResourceLookupSession.get_bin_id_template
        self.assertEqual(self.catalog.get_repository_id(), self.catalog.ident)

    def test_get_repository(self):
        """Tests get_repository"""
        # is this test really needed?
        # From test_templates/resource.py::ResourceLookupSession::get_bin_template
        self.assertIsNotNone(self.catalog)

    def test_can_search_compositions(self):
        """Tests can_search_compositions"""
        # From test_templates/resource.py ResourceQuerySession::can_search_resources_template
        self.assertTrue(isinstance(self.session.can_search_compositions(), bool))

    def test_use_federated_repository_view(self):
        """Tests use_federated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_federated_bin_view_template
        self.catalog.use_federated_repository_view()

    def test_use_isolated_repository_view(self):
        """Tests use_isolated_repository_view"""
        # From test_templates/resource.py ResourceLookupSession.use_isolated_bin_view_template
        self.catalog.use_isolated_repository_view()

    def test_use_sequestered_composition_view(self):
        """Tests use_sequestered_composition_view"""
        # From test_templates/repository.py::CompositionLookupSession::use_sequestered_composition_view
        # Ideally also verify the value is set...
        self.catalog.use_sequestered_composition_view()

    def test_use_unsequestered_composition_view(self):
        """Tests use_unsequestered_composition_view"""
        # From test_templates/repository.py::CompositionLookupSession::use_unsequestered_composition_view
        # Ideally also verify the value is set...
        self.catalog.use_unsequestered_composition_view()

    def test_get_composition_query(self):
        """Tests get_composition_query"""
        # From test_templates/resource.py ResourceQuerySession::get_resource_query_template
        query = self.session.get_composition_query()

    def test_get_compositions_by_query(self):
        """Tests get_compositions_by_query"""
        cfu = self.catalog.get_composition_form_for_update(self.composition_list[3].ident)
        cfu.set_sequestered(True)
        self.catalog.update_composition(cfu)
        query = self.catalog.get_composition_query()
        query.match_display_name('orange')
        self.assertEqual(self.catalog.get_compositions_by_query(query).available(), 1)
        query.clear_display_name_terms()
        query.match_display_name('blue', match=False)
        self.assertEqual(self.catalog.get_compositions_by_query(query).available(), 2)
        cfu = self.catalog.get_composition_form_for_update(self.composition_list[3].ident)
        cfu.set_sequestered(False)
        self.catalog.update_composition(cfu)


class TestCompositionSearchSession(unittest.TestCase):
    """Tests for CompositionSearchSession"""

    def test_get_composition_search(self):
        """Tests get_composition_search"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_composition_search()

    def test_get_composition_search_order(self):
        """Tests get_composition_search_order"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_composition_search_order()

    def test_get_compositions_by_search(self):
        """Tests get_compositions_by_search"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_compositions_by_search(True, True)

    def test_get_composition_query_from_inspector(self):
        """Tests get_composition_query_from_inspector"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_composition_query_from_inspector(True)


class TestCompositionAdminSession(unittest.TestCase):
    """Tests for CompositionAdminSession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceAdminSession::init_template
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for CompositionAdminSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)

    def setUp(self):
        # From test_templates/resource.py::ResourceAdminSession::init_template
        form = self.catalog.get_composition_form_for_create([])
        form.display_name = 'new Composition'
        form.description = 'description of Composition'
        form.set_genus_type(NEW_TYPE)
        self.osid_object = self.catalog.create_composition(form)
        self.session = self.catalog

    def tearDown(self):
        # From test_templates/resource.py::ResourceAdminSession::init_template
        self.catalog.delete_composition(self.osid_object.ident)

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceAdminSession::init_template
        for obj in cls.catalog.get_compositions():
            cls.catalog.delete_composition(obj.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)

    def test_get_repository_id(self):
        """Tests get_repository_id"""
        # From test_templates/resource.py ResourceLookupSession.get_bin_id_template
        self.assertEqual(self.catalog.get_repository_id(), self.catalog.ident)

    def test_get_repository(self):
        """Tests get_repository"""
        # is this test really needed?
        # From test_templates/resource.py::ResourceLookupSession::get_bin_template
        self.assertIsNotNone(self.catalog)

    def test_can_create_compositions(self):
        """Tests can_create_compositions"""
        # From test_templates/resource.py::ResourceAdminSession::can_create_resources_template
        self.assertTrue(isinstance(self.catalog.can_create_compositions(), bool))

    def test_can_create_composition_with_record_types(self):
        """Tests can_create_composition_with_record_types"""
        # From test_templates/resource.py::ResourceAdminSession::can_create_resource_with_record_types_template
        self.assertTrue(isinstance(self.catalog.can_create_composition_with_record_types(DEFAULT_TYPE), bool))

    def test_get_composition_form_for_create(self):
        """Tests get_composition_form_for_create"""
        # From test_templates/resource.py::ResourceAdminSession::get_resource_form_for_create_template
        form = self.catalog.get_composition_form_for_create([])
        self.assertTrue(isinstance(form, OsidForm))
        self.assertFalse(form.is_for_update())

    def test_create_composition(self):
        """Tests create_composition"""
        # From test_templates/resource.py::ResourceAdminSession::create_resource_template
        from dlkit.abstract_osid.repository.objects import Composition
        self.assertTrue(isinstance(self.osid_object, Composition))
        self.assertEqual(self.osid_object.display_name.text, 'new Composition')
        self.assertEqual(self.osid_object.description.text, 'description of Composition')
        self.assertEqual(self.osid_object.genus_type, NEW_TYPE)

    def test_can_update_compositions(self):
        """Tests can_update_compositions"""
        # From test_templates/resource.py::ResourceAdminSession::can_update_resources_template
        self.assertTrue(isinstance(self.catalog.can_update_compositions(), bool))

    def test_get_composition_form_for_update(self):
        """Tests get_composition_form_for_update"""
        # From test_templates/resource.py::ResourceAdminSession::get_resource_form_for_update_template
        form = self.catalog.get_composition_form_for_update(self.osid_object.ident)
        self.assertTrue(isinstance(form, OsidForm))
        self.assertTrue(form.is_for_update())

    def test_update_composition(self):
        """Tests update_composition"""
        # From test_templates/resource.py::ResourceAdminSession::update_resource_template
        from dlkit.abstract_osid.repository.objects import Composition
        form = self.catalog.get_composition_form_for_update(self.osid_object.ident)
        form.display_name = 'new name'
        form.description = 'new description'
        form.set_genus_type(NEW_TYPE_2)
        updated_object = self.catalog.update_composition(form)
        self.assertTrue(isinstance(updated_object, Composition))
        self.assertEqual(updated_object.ident, self.osid_object.ident)
        self.assertEqual(updated_object.display_name.text, 'new name')
        self.assertEqual(updated_object.description.text, 'new description')
        self.assertEqual(updated_object.genus_type, NEW_TYPE_2)

    def test_can_delete_compositions(self):
        """Tests can_delete_compositions"""
        # From test_templates/resource.py::ResourceAdminSession::can_delete_resources_template
        self.assertTrue(isinstance(self.catalog.can_delete_compositions(), bool))

    def test_delete_composition(self):
        """Tests delete_composition"""
        # From test_templates/resource.py::ResourceAdminSession::delete_resource_template
        form = self.catalog.get_composition_form_for_create([])
        form.display_name = 'new Composition'
        form.description = 'description of Composition'
        form.set_genus_type(NEW_TYPE)
        osid_object = self.catalog.create_composition(form)
        self.catalog.delete_composition(osid_object.ident)
        with self.assertRaises(errors.NotFound):
            self.catalog.get_composition(osid_object.ident)

    def test_delete_composition_node(self):
        """Tests delete_composition_node"""
        with self.assertRaises(errors.Unimplemented):
            self.session.delete_composition_node(True)

    def test_add_composition_child(self):
        """Tests add_composition_child"""
        with self.assertRaises(errors.Unimplemented):
            self.session.add_composition_child(True, True)

    def test_remove_composition_child(self):
        """Tests remove_composition_child"""
        with self.assertRaises(errors.Unimplemented):
            self.session.remove_composition_child(True, True)

    def test_can_manage_composition_aliases(self):
        """Tests can_manage_composition_aliases"""
        # From test_templates/resource.py::ResourceAdminSession::can_manage_resource_aliases_template
        self.assertTrue(isinstance(self.catalog.can_manage_composition_aliases(), bool))

    def test_alias_composition(self):
        """Tests alias_composition"""
        # From test_templates/resource.py::ResourceAdminSession::alias_resource_template
        alias_id = Id(self.catalog.ident.namespace + '%3Amy-alias%40ODL.MIT.EDU')
        self.catalog.alias_composition(self.osid_object.ident, alias_id)
        aliased_object = self.catalog.get_composition(alias_id)
        self.assertEqual(aliased_object.ident, self.osid_object.ident)

    def test_composition_assignment(self):
        composition_list = list()
        composition_ids = list()
        for num in [0, 1, 2, 3]:
            create_form = self.catalog.get_composition_form_for_create([])
            create_form.display_name = 'Test Composition ' + str(num)
            create_form.description = 'Test Composition for CompositionLookupSession tests'
            obj = self.catalog.create_composition(create_form)
            composition_list.append(obj)
            composition_ids.append(obj.ident)
        update_form = self.catalog.get_composition_form_for_update(composition_ids[0])
        update_form.set_children(composition_ids[1:])
        self.catalog.update_composition(update_form)
        composition = self.catalog.get_composition(composition_ids[0])
        self.assertEqual(composition.get_children_ids().available(), 3)
        self.assertEqual(composition.get_child_ids().available(), 3)
        self.assertEqual(composition.get_children().available(), 3)


class TestCompositionRepositorySession(unittest.TestCase):
    """Tests for CompositionRepositorySession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceBinSession::init_template
        cls.composition_list = list()
        cls.composition_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for CompositionRepositorySession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository for Assignment'
        create_form.description = 'Test Repository for CompositionRepositorySession tests assignment'
        cls.assigned_catalog = cls.svc_mgr.create_repository(create_form)
        for num in [0, 1, 2]:
            create_form = cls.catalog.get_composition_form_for_create([])
            create_form.display_name = 'Test Composition ' + str(num)
            create_form.description = 'Test Composition for CompositionRepositorySession tests'
            obj = cls.catalog.create_composition(create_form)
            cls.composition_list.append(obj)
            cls.composition_ids.append(obj.ident)
        cls.svc_mgr.assign_composition_to_repository(
            cls.composition_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.assign_composition_to_repository(
            cls.composition_ids[2], cls.assigned_catalog.ident)

    def setUp(self):
        # From test_templates/resource.py::ResourceBinSession::init_template
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceBinSession::init_template
        cls.svc_mgr.unassign_composition_from_repository(
            cls.composition_ids[1], cls.assigned_catalog.ident)
        cls.svc_mgr.unassign_composition_from_repository(
            cls.composition_ids[2], cls.assigned_catalog.ident)
        for obj in cls.catalog.get_compositions():
            cls.catalog.delete_composition(obj.ident)
        cls.svc_mgr.delete_repository(cls.assigned_catalog.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)

    def test_use_comparative_composition_repository_view(self):
        """Tests use_comparative_composition_repository_view"""
        # From test_templates/resource.py::BinLookupSession::use_comparative_bin_view_template
        self.svc_mgr.use_comparative_composition_repository_view()

    def test_use_plenary_composition_repository_view(self):
        """Tests use_plenary_composition_repository_view"""
        # From test_templates/resource.py::BinLookupSession::use_plenary_bin_view_template
        self.svc_mgr.use_plenary_composition_repository_view()

    def test_can_lookup_composition_repository_mappings(self):
        """Tests can_lookup_composition_repository_mappings"""
        # From test_templates/resource.py::ResourceBinSession::can_lookup_resource_bin_mappings
        result = self.session.can_lookup_composition_repository_mappings()
        self.assertTrue(result)

    def test_get_composition_ids_by_repository(self):
        """Tests get_composition_ids_by_repository"""
        # From test_templates/resource.py::ResourceBinSession::get_resource_ids_by_bin_template
        objects = self.svc_mgr.get_composition_ids_by_repository(self.assigned_catalog.ident)
        self.assertEqual(objects.available(), 2)

    def test_get_compositions_by_repository(self):
        """Tests get_compositions_by_repository"""
        # From test_templates/resource.py::ResourceBinSession::get_resources_by_bin_template
        results = self.session.get_compositions_by_repository(self.assigned_catalog.ident)
        self.assertTrue(isinstance(results, ABCObjects.CompositionList))
        self.assertEqual(results.available(), 2)

    def test_get_composition_ids_by_repositories(self):
        """Tests get_composition_ids_by_repositories"""
        # From test_templates/resource.py::ResourceBinSession::get_resource_ids_by_bins_template
        catalog_ids = [self.catalog.ident, self.assigned_catalog.ident]
        object_ids = self.session.get_composition_ids_by_repositories(catalog_ids)
        self.assertTrue(isinstance(object_ids, IdList))
        # Currently our impl does not remove duplicate objectIds
        self.assertEqual(object_ids.available(), 5)

    def test_get_compoitions_by_repositories(self):
        """Tests get_compoitions_by_repositories"""
        # From test_templates/resource.py::ResourceBinSession::get_resources_by_bins_template
        catalog_ids = [self.catalog.ident, self.assigned_catalog.ident]
        results = self.session.get_compoitions_by_repositories(catalog_ids)
        self.assertTrue(isinstance(results, ABCObjects.CompositionList))
        # Currently our impl does not remove duplicate objects
        self.assertEqual(results.available(), 5)

    def test_get_repository_ids_by_composition(self):
        """Tests get_repository_ids_by_composition"""
        # From test_templates/resource.py::ResourceBinSession::get_bin_ids_by_resource_template
        cats = self.svc_mgr.get_repository_ids_by_composition(self.composition_ids[1])
        self.assertEqual(cats.available(), 2)

    def test_get_repositories_by_composition(self):
        """Tests get_repositories_by_composition"""
        # From test_templates/resource.py::ResourceBinSession::get_bins_by_resource_template
        cats = self.svc_mgr.get_repositories_by_composition(self.composition_ids[1])
        self.assertEqual(cats.available(), 2)


class TestCompositionRepositoryAssignmentSession(unittest.TestCase):
    """Tests for CompositionRepositoryAssignmentSession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceBinAssignmentSession::init_template
        cls.composition_list = list()
        cls.composition_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for CompositionRepositoryAssignmentSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository for Assignment'
        create_form.description = 'Test Repository for CompositionRepositoryAssignmentSession tests assignment'
        cls.assigned_catalog = cls.svc_mgr.create_repository(create_form)
        for num in [0, 1, 2]:
            create_form = cls.catalog.get_composition_form_for_create([])
            create_form.display_name = 'Test Composition ' + str(num)
            create_form.description = 'Test Composition for CompositionRepositoryAssignmentSession tests'
            obj = cls.catalog.create_composition(create_form)
            cls.composition_list.append(obj)
            cls.composition_ids.append(obj.ident)

    def setUp(self):
        # From test_templates/resource.py::ResourceBinAssignmentSession::init_template
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceBinAssignmentSession::init_template
        for obj in cls.catalog.get_compositions():
            cls.catalog.delete_composition(obj.ident)
        cls.svc_mgr.delete_repository(cls.assigned_catalog.ident)
        cls.svc_mgr.delete_repository(cls.catalog.ident)

    def test_can_assign_compositions(self):
        """Tests can_assign_compositions"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::can_assign_resources_template
        result = self.session.can_assign_compositions()
        self.assertTrue(isinstance(result, bool))

    def test_can_assign_compositions_to_repository(self):
        """Tests can_assign_compositions_to_repository"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::can_assign_resources_to_bin_template
        result = self.session.can_assign_compositions_to_repository(self.assigned_catalog.ident)
        self.assertTrue(isinstance(result, bool))

    def test_get_assignable_repository_ids(self):
        """Tests get_assignable_repository_ids"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::get_assignable_bin_ids_template
        # Note that our implementation just returns all catalogIds, which does not follow
        #   the OSID spec (should return only the catalogIds below the given one in the hierarchy.
        results = self.session.get_assignable_repository_ids(self.catalog.ident)
        self.assertTrue(isinstance(results, IdList))

        # Because we're not deleting all banks from all tests, we might
        #   have some crufty banks here...but there should be at least 2.
        self.assertTrue(results.available() >= 2)

    def test_get_assignable_repository_ids_for_composition(self):
        """Tests get_assignable_repository_ids_for_composition"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::get_assignable_bin_ids_for_item_template
        # Note that our implementation just returns all catalogIds, which does not follow
        #   the OSID spec (should return only the catalogIds below the given one in the hierarchy.
        results = self.session.get_assignable_repository_ids_for_composition(self.catalog.ident, self.composition_ids[0])
        self.assertTrue(isinstance(results, IdList))

        # Because we're not deleting all banks from all tests, we might
        #   have some crufty banks here...but there should be at least 2.
        self.assertTrue(results.available() >= 2)

    def test_assign_composition_to_repository(self):
        """Tests assign_composition_to_repository"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::assign_resource_to_bin_template
        results = self.assigned_catalog.get_compositions()
        self.assertEqual(results.available(), 0)
        self.session.assign_composition_to_repository(self.composition_ids[1], self.assigned_catalog.ident)
        results = self.assigned_catalog.get_compositions()
        self.assertEqual(results.available(), 1)
        self.session.unassign_composition_from_repository(
            self.composition_ids[1],
            self.assigned_catalog.ident)

    def test_unassign_composition_from_repository(self):
        """Tests unassign_composition_from_repository"""
        # From test_templates/resource.py::ResourceBinAssignmentSession::unassign_resource_from_bin_template
        results = self.assigned_catalog.get_compositions()
        self.assertEqual(results.available(), 0)
        self.session.assign_composition_to_repository(
            self.composition_ids[1],
            self.assigned_catalog.ident)
        results = self.assigned_catalog.get_compositions()
        self.assertEqual(results.available(), 1)
        self.session.unassign_composition_from_repository(
            self.composition_ids[1],
            self.assigned_catalog.ident)
        results = self.assigned_catalog.get_compositions()
        self.assertEqual(results.available(), 0)


class TestRepositoryLookupSession(unittest.TestCase):
    """Tests for RepositoryLookupSession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::BinLookupSession::init_template
        cls.catalogs = list()
        cls.catalog_ids = list()
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        for num in [0, 1]:
            create_form = cls.svc_mgr.get_repository_form_for_create([])
            create_form.display_name = 'Test Repository ' + str(num)
            create_form.description = 'Test Repository for repository proxy manager tests'
            catalog = cls.svc_mgr.create_repository(create_form)
            cls.catalogs.append(catalog)
            cls.catalog_ids.append(catalog.ident)

    def setUp(self):
        # From test_templates/resource.py::BinLookupSession::init_template
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::BinLookupSession::init_template
        for catalog in cls.svc_mgr.get_repositories():
            cls.svc_mgr.delete_repository(catalog.ident)

    def test_can_lookup_repositories(self):
        """Tests can_lookup_repositories"""
        # From test_templates/resource.py::BinLookupSession::can_lookup_bins_template
        self.assertTrue(isinstance(self.session.can_lookup_repositories(), bool))

    def test_use_comparative_repository_view(self):
        """Tests use_comparative_repository_view"""
        # From test_templates/resource.py::BinLookupSession::use_comparative_bin_view_template
        self.svc_mgr.use_comparative_repository_view()

    def test_use_plenary_repository_view(self):
        """Tests use_plenary_repository_view"""
        # From test_templates/resource.py::BinLookupSession::use_plenary_bin_view_template
        self.svc_mgr.use_plenary_repository_view()

    def test_get_repository(self):
        """Tests get_repository"""
        # From test_templates/resource.py::BinLookupSession::get_bin_template
        catalog = self.svc_mgr.get_repository(self.catalogs[0].ident)
        self.assertEqual(catalog.ident, self.catalogs[0].ident)

    def test_get_repositories_by_ids(self):
        """Tests get_repositories_by_ids"""
        # From test_templates/resource.py::BinLookupSession::get_bins_by_ids_template
        catalogs = self.svc_mgr.get_repositories_by_ids(self.catalog_ids)
        self.assertTrue(catalogs.available() == 2)
        self.assertTrue(isinstance(catalogs, ABCObjects.RepositoryList))
        reversed_catalog_ids = [str(cat_id) for cat_id in self.catalog_ids][::-1]
        for index, catalog in enumerate(catalogs):
            self.assertEqual(str(catalog.ident),
                             reversed_catalog_ids[index])

    def test_get_repositories_by_genus_type(self):
        """Tests get_repositories_by_genus_type"""
        # From test_templates/resource.py::BinLookupSession::get_bins_by_genus_type_template
        catalogs = self.svc_mgr.get_repositories_by_genus_type(DEFAULT_GENUS_TYPE)
        self.assertTrue(catalogs.available() > 0)
        self.assertTrue(isinstance(catalogs, ABCObjects.RepositoryList))

    def test_get_repositories_by_parent_genus_type(self):
        """Tests get_repositories_by_parent_genus_type"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_repositories_by_parent_genus_type(True)

    def test_get_repositories_by_record_type(self):
        """Tests get_repositories_by_record_type"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_repositories_by_record_type(True)

    def test_get_repositories_by_provider(self):
        """Tests get_repositories_by_provider"""
        with self.assertRaises(errors.Unimplemented):
            self.session.get_repositories_by_provider(True)

    def test_get_repositories(self):
        """Tests get_repositories"""
        # From test_templates/resource.py::BinLookupSession::get_bins_template
        catalogs = self.svc_mgr.get_repositories()
        self.assertTrue(catalogs.available() > 0)
        self.assertTrue(isinstance(catalogs, ABCObjects.RepositoryList))


class TestRepositoryQuerySession(unittest.TestCase):
    """Tests for RepositoryQuerySession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::BinQuerySession::init_template
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def setUp(self):
        # From test_templates/resource.py::BinQuerySession::init_template
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::BinQuerySession::init_template
        cls.svc_mgr.delete_repository(cls.catalog.ident)

    def test_can_search_repositories(self):
        """Tests can_search_repositories"""
        # From test_templates/resource.py ResourceQuerySession::can_search_resources_template
        self.assertTrue(isinstance(self.session.can_search_repositories(), bool))

    def test_get_repository_query(self):
        """Tests get_repository_query"""
        # From test_templates/resource.py::BinQuerySession::get_bin_query_template
        query = self.session.get_repository_query()
        self.assertTrue(isinstance(query, ABCQueries.RepositoryQuery))

    def test_get_repositories_by_query(self):
        """Tests get_repositories_by_query"""
        # From test_templates/resource.py::BinQuerySession::get_bins_by_query_template
        query = self.session.get_repository_query()
        query.match_display_name('Test catalog')
        self.assertEqual(self.session.get_repositories_by_query(query).available(), 1)
        query.clear_display_name_terms()
        query.match_display_name('Test catalog', match=False)
        self.assertEqual(self.session.get_repositories_by_query(query).available(), 0)


class TestRepositoryAdminSession(unittest.TestCase):
    """Tests for RepositoryAdminSession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::BinAdminSession::init_template
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        # Initialize test catalog:
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository'
        create_form.description = 'Test Repository for RepositoryAdminSession tests'
        cls.catalog = cls.svc_mgr.create_repository(create_form)
        # Initialize catalog to be deleted:
        create_form = cls.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'Test Repository For Deletion'
        create_form.description = 'Test Repository for RepositoryAdminSession deletion test'
        cls.catalog_to_delete = cls.svc_mgr.create_repository(create_form)

    def setUp(self):
        # From test_templates/resource.py::BinAdminSession::init_template
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::BinAdminSession::init_template
        for catalog in cls.svc_mgr.get_repositories():
            cls.svc_mgr.delete_repository(catalog.ident)

    def test_can_create_repositories(self):
        """Tests can_create_repositories"""
        # From test_templates/resource.py BinAdminSession.can_create_bins_template
        self.assertTrue(isinstance(self.svc_mgr.can_create_repositories(), bool))

    def test_can_create_repository_with_record_types(self):
        """Tests can_create_repository_with_record_types"""
        # From test_templates/resource.py BinAdminSession.can_create_bin_with_record_types_template
        self.assertTrue(isinstance(self.svc_mgr.can_create_repository_with_record_types(DEFAULT_TYPE), bool))

    def test_get_repository_form_for_create(self):
        """Tests get_repository_form_for_create"""
        # From test_templates/resource.py BinAdminSession.get_bin_form_for_create_template
        from dlkit.abstract_osid.repository.objects import RepositoryForm
        catalog_form = self.svc_mgr.get_repository_form_for_create([])
        self.assertTrue(isinstance(catalog_form, RepositoryForm))
        self.assertFalse(catalog_form.is_for_update())

    def test_create_repository(self):
        """Tests create_repository"""
        # From test_templates/resource.py BinAdminSession.create_bin_template
        from dlkit.abstract_osid.repository.objects import Repository
        catalog_form = self.svc_mgr.get_repository_form_for_create([])
        catalog_form.display_name = 'Test Repository'
        catalog_form.description = 'Test Repository for RepositoryAdminSession.create_repository tests'
        new_catalog = self.svc_mgr.create_repository(catalog_form)
        self.assertTrue(isinstance(new_catalog, Repository))

    def test_can_update_repositories(self):
        """Tests can_update_repositories"""
        # From test_templates/resource.py BinAdminSession.can_update_bins_template
        self.assertTrue(isinstance(self.svc_mgr.can_update_repositories(), bool))

    def test_get_repository_form_for_update(self):
        """Tests get_repository_form_for_update"""
        # From test_templates/resource.py BinAdminSession.get_bin_form_for_update_template
        from dlkit.abstract_osid.repository.objects import RepositoryForm
        catalog_form = self.svc_mgr.get_repository_form_for_update(self.catalog.ident)
        self.assertTrue(isinstance(catalog_form, RepositoryForm))
        self.assertTrue(catalog_form.is_for_update())

    def test_update_repository(self):
        """Tests update_repository"""
        # From test_templates/resource.py BinAdminSession.update_bin_template
        catalog_form = self.svc_mgr.get_repository_form_for_update(self.catalog.ident)
        # Update some elements here?
        self.svc_mgr.update_repository(catalog_form)

    def test_can_delete_repositories(self):
        """Tests can_delete_repositories"""
        # From test_templates/resource.py BinAdminSession.can_delete_bins_template
        self.assertTrue(isinstance(self.svc_mgr.can_delete_repositories(), bool))

    def test_delete_repository(self):
        """Tests delete_repository"""
        # From test_templates/resource.py BinAdminSession.delete_bin_template
        cat_id = self.catalog_to_delete.ident
        self.svc_mgr.delete_repository(cat_id)
        with self.assertRaises(errors.NotFound):
            self.svc_mgr.get_repository(cat_id)

    def test_can_manage_repository_aliases(self):
        """Tests can_manage_repository_aliases"""
        # From test_templates/resource.py::ResourceAdminSession::can_manage_resource_aliases_template
        self.assertTrue(isinstance(self.svc_mgr.can_manage_repository_aliases(), bool))

    def test_alias_repository(self):
        """Tests alias_repository"""
        # From test_templates/resource.py BinAdminSession.alias_bin_template
        alias_id = Id('repository.Repository%3Amy-alias%40ODL.MIT.EDU')
        self.svc_mgr.alias_repository(self.catalog_to_delete.ident, alias_id)
        aliased_catalog = self.svc_mgr.get_repository(alias_id)
        self.assertEqual(self.catalog_to_delete.ident, aliased_catalog.ident)


class TestRepositoryHierarchySession(unittest.TestCase):
    """Tests for RepositoryHierarchySession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::BinHierarchySession::init_template
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        cls.catalogs = dict()
        for name in ['Root', 'Child 1', 'Child 2', 'Grandchild 1']:
            create_form = cls.svc_mgr.get_repository_form_for_create([])
            create_form.display_name = name
            create_form.description = 'Test Repository ' + name
            cls.catalogs[name] = cls.svc_mgr.create_repository(create_form)
        cls.svc_mgr.add_root_repository(cls.catalogs['Root'].ident)
        cls.svc_mgr.add_child_repository(cls.catalogs['Root'].ident, cls.catalogs['Child 1'].ident)
        cls.svc_mgr.add_child_repository(cls.catalogs['Root'].ident, cls.catalogs['Child 2'].ident)
        cls.svc_mgr.add_child_repository(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)

    def setUp(self):
        # From test_templates/resource.py::BinHierarchySession::init_template
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::BinHierarchySession::init_template
        cls.svc_mgr.remove_child_repository(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)
        cls.svc_mgr.remove_child_repositories(cls.catalogs['Root'].ident)
        cls.svc_mgr.remove_root_repository(cls.catalogs['Root'].ident)
        for cat_name in cls.catalogs:
            cls.svc_mgr.delete_repository(cls.catalogs[cat_name].ident)

    def test_get_repository_hierarchy_id(self):
        """Tests get_repository_hierarchy_id"""
        # From test_templates/resource.py::BinHierarchySession::get_bin_hierarchy_id_template
        hierarchy_id = self.svc_mgr.get_repository_hierarchy_id()
        self.assertTrue(isinstance(hierarchy_id, Id))

    def test_get_repository_hierarchy(self):
        """Tests get_repository_hierarchy"""
        # From test_templates/resource.py::BinHierarchySession::get_bin_hierarchy_template
        hierarchy = self.svc_mgr.get_repository_hierarchy()
        self.assertTrue(isinstance(hierarchy, Hierarchy))

    def test_can_access_repository_hierarchy(self):
        """Tests can_access_repository_hierarchy"""
        # From test_templates/resource.py::BinHierarchySession::can_access_objective_bank_hierarchy_template
        self.assertTrue(isinstance(self.svc_mgr.can_access_repository_hierarchy(), bool))

    def test_use_comparative_repository_view(self):
        """Tests use_comparative_repository_view"""
        # From test_templates/resource.py::BinLookupSession::use_comparative_bin_view_template
        self.svc_mgr.use_comparative_repository_view()

    def test_use_plenary_repository_view(self):
        """Tests use_plenary_repository_view"""
        # From test_templates/resource.py::BinLookupSession::use_plenary_bin_view_template
        self.svc_mgr.use_plenary_repository_view()

    def test_get_root_repository_ids(self):
        """Tests get_root_repository_ids"""
        # From test_templates/resource.py::BinHierarchySession::get_root_bin_ids_template
        root_ids = self.svc_mgr.get_root_repository_ids()
        self.assertTrue(isinstance(root_ids, IdList))
        # probably should be == 1, but we seem to be getting test cruft,
        # and I can't pinpoint where it's being introduced.
        self.assertTrue(root_ids.available() >= 1)

    def test_get_root_repositories(self):
        """Tests get_root_repositories"""
        # From test_templates/resource.py::BinHierarchySession::get_root_bins_template
        from dlkit.abstract_osid.repository.objects import RepositoryList
        roots = self.svc_mgr.get_root_repositories()
        self.assertTrue(isinstance(roots, RepositoryList))
        self.assertTrue(roots.available() == 1)

    def test_has_parent_repositories(self):
        """Tests has_parent_repositories"""
        # From test_templates/resource.py::BinHierarchySession::has_parent_bins_template
        self.assertTrue(isinstance(self.svc_mgr.has_parent_repositories(self.catalogs['Child 1'].ident), bool))
        self.assertTrue(self.svc_mgr.has_parent_repositories(self.catalogs['Child 1'].ident))
        self.assertTrue(self.svc_mgr.has_parent_repositories(self.catalogs['Child 2'].ident))
        self.assertTrue(self.svc_mgr.has_parent_repositories(self.catalogs['Grandchild 1'].ident))
        self.assertFalse(self.svc_mgr.has_parent_repositories(self.catalogs['Root'].ident))

    def test_is_parent_of_repository(self):
        """Tests is_parent_of_repository"""
        # From test_templates/resource.py::BinHierarchySession::is_parent_of_bin_template
        self.assertTrue(isinstance(self.svc_mgr.is_parent_of_repository(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident), bool))
        self.assertTrue(self.svc_mgr.is_parent_of_repository(self.catalogs['Root'].ident, self.catalogs['Child 1'].ident))
        self.assertTrue(self.svc_mgr.is_parent_of_repository(self.catalogs['Child 1'].ident, self.catalogs['Grandchild 1'].ident))
        self.assertFalse(self.svc_mgr.is_parent_of_repository(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident))

    def test_get_parent_repository_ids(self):
        """Tests get_parent_repository_ids"""
        # From test_templates/resource.py::BinHierarchySession::get_parent_bin_ids_template
        from dlkit.abstract_osid.id.objects import IdList
        catalog_list = self.svc_mgr.get_parent_repository_ids(self.catalogs['Child 1'].ident)
        self.assertTrue(isinstance(catalog_list, IdList))
        self.assertEqual(catalog_list.available(), 1)

    def test_get_parent_repositories(self):
        """Tests get_parent_repositories"""
        # From test_templates/resource.py::BinHierarchySession::get_parent_bins_template
        from dlkit.abstract_osid.repository.objects import RepositoryList
        catalog_list = self.svc_mgr.get_parent_repositories(self.catalogs['Child 1'].ident)
        self.assertTrue(isinstance(catalog_list, RepositoryList))
        self.assertEqual(catalog_list.available(), 1)
        self.assertEqual(catalog_list.next().display_name.text, 'Root')

    def test_is_ancestor_of_repository(self):
        """Tests is_ancestor_of_repository"""
        # From test_templates/resource.py::BinHierarchySession::is_ancestor_of_bin_template
        self.assertRaises(errors.Unimplemented,
                          self.svc_mgr.is_ancestor_of_repository,
                          self.catalogs['Root'].ident,
                          self.catalogs['Child 1'].ident)
        # self.assertTrue(isinstance(self.svc_mgr.is_ancestor_of_repository(
        #     self.catalogs['Root'].ident,
        #     self.catalogs['Child 1'].ident),
        #     bool))
        # self.assertTrue(self.svc_mgr.is_ancestor_of_repository(
        #     self.catalogs['Root'].ident,
        #     self.catalogs['Child 1'].ident))
        # self.assertTrue(self.svc_mgr.is_ancestor_of_repository(
        #     self.catalogs['Root'].ident,
        #     self.catalogs['Grandchild 1'].ident))
        # self.assertFalse(self.svc_mgr.is_ancestor_of_repository(
        #     self.catalogs['Child 1'].ident,
        #     self.catalogs['Root'].ident))

    def test_has_child_repositories(self):
        """Tests has_child_repositories"""
        self.assertTrue(isinstance(self.svc_mgr.has_child_repositories(self.catalogs['Child 1'].ident), bool))
        self.assertTrue(self.svc_mgr.has_child_repositories(self.catalogs['Root'].ident))
        self.assertTrue(self.svc_mgr.has_child_repositories(self.catalogs['Child 1'].ident))
        self.assertFalse(self.svc_mgr.has_child_repositories(self.catalogs['Child 2'].ident))
        self.assertFalse(self.svc_mgr.has_child_repositories(self.catalogs['Grandchild 1'].ident))

    def test_is_child_of_repository(self):
        """Tests is_child_of_repository"""
        self.assertTrue(isinstance(self.svc_mgr.is_child_of_repository(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident), bool))
        self.assertTrue(self.svc_mgr.is_child_of_repository(self.catalogs['Child 1'].ident, self.catalogs['Root'].ident))
        self.assertTrue(self.svc_mgr.is_child_of_repository(self.catalogs['Grandchild 1'].ident, self.catalogs['Child 1'].ident))
        self.assertFalse(self.svc_mgr.is_child_of_repository(self.catalogs['Root'].ident, self.catalogs['Child 1'].ident))

    def test_get_child_repository_ids(self):
        """Tests get_child_repository_ids"""
        from dlkit.abstract_osid.id.objects import IdList
        catalog_list = self.svc_mgr.get_child_repository_ids(self.catalogs['Child 1'].ident)
        self.assertTrue(isinstance(catalog_list, IdList))
        self.assertEqual(catalog_list.available(), 1)

    def test_get_child_repositories(self):
        """Tests get_child_repositories"""
        from dlkit.abstract_osid.repository.objects import RepositoryList
        catalog_list = self.svc_mgr.get_child_repositories(self.catalogs['Child 1'].ident)
        self.assertTrue(isinstance(catalog_list, RepositoryList))
        self.assertEqual(catalog_list.available(), 1)
        self.assertEqual(catalog_list.next().display_name.text, 'Grandchild 1')

    def test_is_descendant_of_repository(self):
        """Tests is_descendant_of_repository"""
        # From test_templates/resource.py::BinHierarchySession::is_descendant_of_bin_template
        self.assertRaises(errors.Unimplemented,
                          self.svc_mgr.is_descendant_of_repository,
                          self.catalogs['Child 1'].ident,
                          self.catalogs['Root'].ident)
        # self.assertTrue(isinstance(self.svc_mgr.is_descendant_of_repository(
        #     self.catalogs['Root'].ident,
        #     self.catalogs['Child 1'].ident),
        #     bool))
        # self.assertTrue(self.svc_mgr.is_descendant_of_repository(
        #     self.catalogs['Child 1'].ident,
        #     self.catalogs['Root'].ident))
        # self.assertTrue(self.svc_mgr.is_descendant_of_repository(
        #     self.catalogs['Grandchild 1'].ident,
        #     self.catalogs['Root'].ident))
        # self.assertFalse(self.svc_mgr.is_descendant_of_repository(
        #     self.catalogs['Root'].ident,
        #     self.catalogs['Child 1'].ident))

    def test_get_repository_node_ids(self):
        """Tests get_repository_node_ids"""
        # From test_templates/resource.py::BinHierarchySession::get_bin_node_ids_template
        # Per the spec, perhaps counterintuitively this method returns a
        #  node, **not** a IdList...
        node = self.svc_mgr.get_repository_node_ids(self.catalogs['Child 1'].ident, 1, 2, False)
        self.assertTrue(isinstance(node, OsidNode))
        self.assertFalse(node.is_root())
        self.assertFalse(node.is_leaf())
        self.assertTrue(node.get_child_ids().available(), 1)
        self.assertTrue(isinstance(node.get_child_ids(), IdList))
        self.assertTrue(node.get_parent_ids().available(), 1)
        self.assertTrue(isinstance(node.get_parent_ids(), IdList))

    def test_get_repository_nodes(self):
        """Tests get_repository_nodes"""
        # From test_templates/resource.py::BinHierarchySession::get_bin_nodes_template
        node = self.svc_mgr.get_repository_nodes(self.catalogs['Child 1'].ident, 1, 2, False)
        self.assertTrue(isinstance(node, OsidNode))
        self.assertFalse(node.is_root())
        self.assertFalse(node.is_leaf())
        self.assertTrue(node.get_child_ids().available(), 1)
        self.assertTrue(isinstance(node.get_child_ids(), IdList))
        self.assertTrue(node.get_parent_ids().available(), 1)
        self.assertTrue(isinstance(node.get_parent_ids(), IdList))


class TestRepositoryHierarchyDesignSession(unittest.TestCase):
    """Tests for RepositoryHierarchyDesignSession"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::BinHierarchyDesignSession::init_template
        cls.svc_mgr = Runtime().get_service_manager('REPOSITORY', proxy=PROXY, implementation='TEST_SERVICE')
        cls.catalogs = dict()
        for name in ['Root', 'Child 1', 'Child 2', 'Grandchild 1']:
            create_form = cls.svc_mgr.get_repository_form_for_create([])
            create_form.display_name = name
            create_form.description = 'Test Repository ' + name
            cls.catalogs[name] = cls.svc_mgr.create_repository(create_form)
        cls.svc_mgr.add_root_repository(cls.catalogs['Root'].ident)
        cls.svc_mgr.add_child_repository(cls.catalogs['Root'].ident, cls.catalogs['Child 1'].ident)
        cls.svc_mgr.add_child_repository(cls.catalogs['Root'].ident, cls.catalogs['Child 2'].ident)
        cls.svc_mgr.add_child_repository(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)

    def setUp(self):
        # From test_templates/resource.py::BinHierarchyDesignSession::init_template
        self.session = self.svc_mgr

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::BinHierarchyDesignSession::init_template
        cls.svc_mgr.remove_child_repository(cls.catalogs['Child 1'].ident, cls.catalogs['Grandchild 1'].ident)
        cls.svc_mgr.remove_child_repositories(cls.catalogs['Root'].ident)
        for cat_name in cls.catalogs:
            cls.svc_mgr.delete_repository(cls.catalogs[cat_name].ident)

    def test_get_repository_hierarchy_id(self):
        """Tests get_repository_hierarchy_id"""
        # From test_templates/resource.py::BinHierarchySession::get_bin_hierarchy_id_template
        hierarchy_id = self.svc_mgr.get_repository_hierarchy_id()
        self.assertTrue(isinstance(hierarchy_id, Id))

    def test_get_repository_hierarchy(self):
        """Tests get_repository_hierarchy"""
        # From test_templates/resource.py::BinHierarchySession::get_bin_hierarchy_template
        hierarchy = self.svc_mgr.get_repository_hierarchy()
        self.assertTrue(isinstance(hierarchy, Hierarchy))

    def test_can_modify_repository_hierarchy(self):
        """Tests can_modify_repository_hierarchy"""
        # From test_templates/resource.py::BinHierarchyDesignSession::can_modify_bin_hierarchy_template
        self.assertTrue(isinstance(self.session.can_modify_repository_hierarchy(), bool))

    def test_add_root_repository(self):
        """Tests add_root_repository"""
        # From test_templates/resource.py::BinHierarchyDesignSession::add_root_bin_template
        # this is tested in the setUpClass
        roots = self.session.get_root_repositories()
        self.assertTrue(isinstance(roots, ABCObjects.RepositoryList))
        self.assertEqual(roots.available(), 1)

    def test_remove_root_repository(self):
        """Tests remove_root_repository"""
        # From test_templates/resource.py::BinHierarchyDesignSession::remove_root_bin_template
        roots = self.session.get_root_repositories()
        self.assertEqual(roots.available(), 1)

        create_form = self.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'new root'
        create_form.description = 'Test Repository root'
        new_repository = self.svc_mgr.create_repository(create_form)
        self.svc_mgr.add_root_repository(new_repository.ident)

        roots = self.session.get_root_repositories()
        self.assertEqual(roots.available(), 2)

        self.session.remove_root_repository(new_repository.ident)

        roots = self.session.get_root_repositories()
        self.assertEqual(roots.available(), 1)

    def test_add_child_repository(self):
        """Tests add_child_repository"""
        # From test_templates/resource.py::BinHierarchyDesignSession::add_child_bin_template
        # this is tested in the setUpClass
        children = self.session.get_child_repositories(self.catalogs['Root'].ident)
        self.assertTrue(isinstance(children, ABCObjects.RepositoryList))
        self.assertEqual(children.available(), 2)

    def test_remove_child_repository(self):
        """Tests remove_child_repository"""
        # From test_templates/resource.py::BinHierarchyDesignSession::remove_child_bin_template
        children = self.session.get_child_repositories(self.catalogs['Root'].ident)
        self.assertEqual(children.available(), 2)

        create_form = self.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'test child'
        create_form.description = 'Test Repository child'
        new_repository = self.svc_mgr.create_repository(create_form)
        self.svc_mgr.add_child_repository(
            self.catalogs['Root'].ident,
            new_repository.ident)

        children = self.session.get_child_repositories(self.catalogs['Root'].ident)
        self.assertEqual(children.available(), 3)

        self.session.remove_child_repository(
            self.catalogs['Root'].ident,
            new_repository.ident)

        children = self.session.get_child_repositories(self.catalogs['Root'].ident)
        self.assertEqual(children.available(), 2)

    def test_remove_child_repositories(self):
        """Tests remove_child_repositories"""
        # From test_templates/resource.py::BinHierarchyDesignSession::remove_child_bins_template
        children = self.session.get_child_repositories(self.catalogs['Grandchild 1'].ident)
        self.assertEqual(children.available(), 0)

        create_form = self.svc_mgr.get_repository_form_for_create([])
        create_form.display_name = 'test great grandchild'
        create_form.description = 'Test Repository child'
        new_repository = self.svc_mgr.create_repository(create_form)
        self.svc_mgr.add_child_repository(
            self.catalogs['Grandchild 1'].ident,
            new_repository.ident)

        children = self.session.get_child_repositories(self.catalogs['Grandchild 1'].ident)
        self.assertEqual(children.available(), 1)

        self.session.remove_child_repositories(self.catalogs['Grandchild 1'].ident)

        children = self.session.get_child_repositories(self.catalogs['Grandchild 1'].ident)
        self.assertEqual(children.available(), 0)
