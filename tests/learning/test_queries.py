"""Unit tests of learning queries."""


import unittest


from dlkit.abstract_osid.osid import errors
from dlkit.json_.learning.queries import ActivityQuery
from dlkit.json_.learning.queries import ObjectiveBankQuery
from dlkit.primordium.id.primitives import Id
from dlkit.primordium.type.primitives import Type
from dlkit.runtime import PROXY_SESSION, proxy_example
from dlkit.runtime.managers import Runtime


REQUEST = proxy_example.SimpleRequest()
CONDITION = PROXY_SESSION.get_proxy_condition()
CONDITION.set_http_request(REQUEST)
PROXY = PROXY_SESSION.get_proxy(CONDITION)

DEFAULT_TYPE = Type(**{'identifier': 'DEFAULT', 'namespace': 'DEFAULT', 'authority': 'DEFAULT'})


class TestObjectiveQuery(unittest.TestCase):
    """Tests for ObjectiveQuery"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceQuery::init_template
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

    def setUp(self):
        # From test_templates/resource.py::ResourceQuery::init_template
        self.query = self.catalog.get_objective_query()

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceQuery::init_template
        cls.svc_mgr.delete_objective_bank(cls.catalog.ident)

    def test_match_assessment_id(self):
        """Tests match_assessment_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('assessmentId', self.query._query_terms)
        self.query.match_assessment_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['assessmentId'], {
            '$in': [str(test_id)]
        })

    def test_clear_assessment_id_terms(self):
        """Tests clear_assessment_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_assessment_id(test_id, match=True)
        self.assertIn('assessmentId',
                      self.query._query_terms)
        self.query.clear_assessment_id_terms()
        self.assertNotIn('assessmentId',
                         self.query._query_terms)

    def test_supports_assessment_query(self):
        """Tests supports_assessment_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_assessment_query()

    def test_get_assessment_query(self):
        """Tests get_assessment_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_assessment_query()

    def test_match_any_assessment(self):
        """Tests match_any_assessment"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_assessment(True)

    def test_clear_assessment_terms(self):
        """Tests clear_assessment_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['assessment'] = 'foo'
        self.query.clear_assessment_terms()
        self.assertNotIn('assessment',
                         self.query._query_terms)

    def test_match_knowledge_category_id(self):
        """Tests match_knowledge_category_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('knowledgeCategoryId', self.query._query_terms)
        self.query.match_knowledge_category_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['knowledgeCategoryId'], {
            '$in': [str(test_id)]
        })

    def test_clear_knowledge_category_id_terms(self):
        """Tests clear_knowledge_category_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_knowledge_category_id(test_id, match=True)
        self.assertIn('knowledgeCategoryId',
                      self.query._query_terms)
        self.query.clear_knowledge_category_id_terms()
        self.assertNotIn('knowledgeCategoryId',
                         self.query._query_terms)

    def test_supports_knowledge_category_query(self):
        """Tests supports_knowledge_category_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_knowledge_category_query()

    def test_get_knowledge_category_query(self):
        """Tests get_knowledge_category_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_knowledge_category_query()

    def test_match_any_knowledge_category(self):
        """Tests match_any_knowledge_category"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_knowledge_category(True)

    def test_clear_knowledge_category_terms(self):
        """Tests clear_knowledge_category_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['knowledgeCategory'] = 'foo'
        self.query.clear_knowledge_category_terms()
        self.assertNotIn('knowledgeCategory',
                         self.query._query_terms)

    def test_match_cognitive_process_id(self):
        """Tests match_cognitive_process_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('cognitiveProcessId', self.query._query_terms)
        self.query.match_cognitive_process_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['cognitiveProcessId'], {
            '$in': [str(test_id)]
        })

    def test_clear_cognitive_process_id_terms(self):
        """Tests clear_cognitive_process_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_cognitive_process_id(test_id, match=True)
        self.assertIn('cognitiveProcessId',
                      self.query._query_terms)
        self.query.clear_cognitive_process_id_terms()
        self.assertNotIn('cognitiveProcessId',
                         self.query._query_terms)

    def test_supports_cognitive_process_query(self):
        """Tests supports_cognitive_process_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_cognitive_process_query()

    def test_get_cognitive_process_query(self):
        """Tests get_cognitive_process_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_cognitive_process_query()

    def test_match_any_cognitive_process(self):
        """Tests match_any_cognitive_process"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_cognitive_process(True)

    def test_clear_cognitive_process_terms(self):
        """Tests clear_cognitive_process_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['cognitiveProcess'] = 'foo'
        self.query.clear_cognitive_process_terms()
        self.assertNotIn('cognitiveProcess',
                         self.query._query_terms)

    def test_match_activity_id(self):
        """Tests match_activity_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('activityId', self.query._query_terms)
        self.query.match_activity_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['activityId'], {
            '$in': [str(test_id)]
        })

    def test_clear_activity_id_terms(self):
        """Tests clear_activity_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_activity_id(test_id, match=True)
        self.assertIn('activityId',
                      self.query._query_terms)
        self.query.clear_activity_id_terms()
        self.assertNotIn('activityId',
                         self.query._query_terms)

    def test_supports_activity_query(self):
        """Tests supports_activity_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_activity_query()

    def test_get_activity_query(self):
        """Tests get_activity_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_activity_query()

    def test_match_any_activity(self):
        """Tests match_any_activity"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_activity(True)

    def test_clear_activity_terms(self):
        """Tests clear_activity_terms"""
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_activity_terms()

    def test_match_requisite_objective_id(self):
        """Tests match_requisite_objective_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('requisiteObjectiveId', self.query._query_terms)
        self.query.match_requisite_objective_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['requisiteObjectiveId'], {
            '$in': [str(test_id)]
        })

    def test_clear_requisite_objective_id_terms(self):
        """Tests clear_requisite_objective_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_requisite_objective_id(test_id, match=True)
        self.assertIn('requisiteObjectiveId',
                      self.query._query_terms)
        self.query.clear_requisite_objective_id_terms()
        self.assertNotIn('requisiteObjectiveId',
                         self.query._query_terms)

    def test_supports_requisite_objective_query(self):
        """Tests supports_requisite_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_requisite_objective_query()

    def test_get_requisite_objective_query(self):
        """Tests get_requisite_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_requisite_objective_query()

    def test_match_any_requisite_objective(self):
        """Tests match_any_requisite_objective"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_requisite_objective(True)

    def test_clear_requisite_objective_terms(self):
        """Tests clear_requisite_objective_terms"""
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_requisite_objective_terms()

    def test_match_dependent_objective_id(self):
        """Tests match_dependent_objective_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('dependentObjectiveId', self.query._query_terms)
        self.query.match_dependent_objective_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['dependentObjectiveId'], {
            '$in': [str(test_id)]
        })

    def test_clear_dependent_objective_id_terms(self):
        """Tests clear_dependent_objective_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_dependent_objective_id(test_id, match=True)
        self.assertIn('dependentObjectiveId',
                      self.query._query_terms)
        self.query.clear_dependent_objective_id_terms()
        self.assertNotIn('dependentObjectiveId',
                         self.query._query_terms)

    def test_supports_depndent_objective_query(self):
        """Tests supports_depndent_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_depndent_objective_query()

    def test_get_dependent_objective_query(self):
        """Tests get_dependent_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_dependent_objective_query()

    def test_match_any_dependent_objective(self):
        """Tests match_any_dependent_objective"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_dependent_objective(True)

    def test_clear_dependent_objective_terms(self):
        """Tests clear_dependent_objective_terms"""
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_dependent_objective_terms()

    def test_match_equivalent_objective_id(self):
        """Tests match_equivalent_objective_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('equivalentObjectiveId', self.query._query_terms)
        self.query.match_equivalent_objective_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['equivalentObjectiveId'], {
            '$in': [str(test_id)]
        })

    def test_clear_equivalent_objective_id_terms(self):
        """Tests clear_equivalent_objective_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_equivalent_objective_id(test_id, match=True)
        self.assertIn('equivalentObjectiveId',
                      self.query._query_terms)
        self.query.clear_equivalent_objective_id_terms()
        self.assertNotIn('equivalentObjectiveId',
                         self.query._query_terms)

    def test_supports_equivalent_objective_query(self):
        """Tests supports_equivalent_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_equivalent_objective_query()

    def test_get_equivalent_objective_query(self):
        """Tests get_equivalent_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_equivalent_objective_query()

    def test_match_any_equivalent_objective(self):
        """Tests match_any_equivalent_objective"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_equivalent_objective(True)

    def test_clear_equivalent_objective_terms(self):
        """Tests clear_equivalent_objective_terms"""
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_equivalent_objective_terms()

    def test_match_ancestor_objective_id(self):
        """Tests match_ancestor_objective_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('ancestorObjectiveId', self.query._query_terms)
        self.query.match_ancestor_objective_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['ancestorObjectiveId'], {
            '$in': [str(test_id)]
        })

    def test_clear_ancestor_objective_id_terms(self):
        """Tests clear_ancestor_objective_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_ancestor_objective_id(test_id, match=True)
        self.assertIn('ancestorObjectiveId',
                      self.query._query_terms)
        self.query.clear_ancestor_objective_id_terms()
        self.assertNotIn('ancestorObjectiveId',
                         self.query._query_terms)

    def test_supports_ancestor_objective_query(self):
        """Tests supports_ancestor_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_ancestor_objective_query()

    def test_get_ancestor_objective_query(self):
        """Tests get_ancestor_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_ancestor_objective_query()

    def test_match_any_ancestor_objective(self):
        """Tests match_any_ancestor_objective"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_ancestor_objective(True)

    def test_clear_ancestor_objective_terms(self):
        """Tests clear_ancestor_objective_terms"""
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_ancestor_objective_terms()

    def test_match_descendant_objective_id(self):
        """Tests match_descendant_objective_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('descendantObjectiveId', self.query._query_terms)
        self.query.match_descendant_objective_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['descendantObjectiveId'], {
            '$in': [str(test_id)]
        })

    def test_clear_descendant_objective_id_terms(self):
        """Tests clear_descendant_objective_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_descendant_objective_id(test_id, match=True)
        self.assertIn('descendantObjectiveId',
                      self.query._query_terms)
        self.query.clear_descendant_objective_id_terms()
        self.assertNotIn('descendantObjectiveId',
                         self.query._query_terms)

    def test_supports_descendant_objective_query(self):
        """Tests supports_descendant_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_descendant_objective_query()

    def test_get_descendant_objective_query(self):
        """Tests get_descendant_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_descendant_objective_query()

    def test_match_any_descendant_objective(self):
        """Tests match_any_descendant_objective"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_descendant_objective(True)

    def test_clear_descendant_objective_terms(self):
        """Tests clear_descendant_objective_terms"""
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_descendant_objective_terms()

    def test_match_objective_bank_id(self):
        """Tests match_objective_bank_id"""
        # From test_templates/resource.py::ResourceQuery::match_bin_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_objective_bank_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['assignedObjectiveBankIds'], {
            '$in': [str(test_id)]
        })

    def test_clear_objective_bank_id_terms(self):
        """Tests clear_objective_bank_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_bin_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_objective_bank_id(test_id, match=True)
        self.assertIn('assignedObjectiveBankIds',
                      self.query._query_terms)
        self.query.clear_objective_bank_id_terms()
        self.assertNotIn('assignedObjectiveBankIds',
                         self.query._query_terms)

    def test_supports_objective_bank_query(self):
        """Tests supports_objective_bank_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_objective_bank_query()

    def test_get_objective_bank_query(self):
        """Tests get_objective_bank_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_objective_bank_query()

    def test_clear_objective_bank_terms(self):
        """Tests clear_objective_bank_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['objectiveBank'] = 'foo'
        self.query.clear_objective_bank_terms()
        self.assertNotIn('objectiveBank',
                         self.query._query_terms)

    def test_get_objective_query_record(self):
        """Tests get_objective_query_record"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_objective_query_record(True)


class TestActivityQuery(unittest.TestCase):
    """Tests for ActivityQuery"""

    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test ObjectiveBank'
        create_form.description = 'Test ObjectiveBank for ActivityLookupSession tests'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        create_form = cls.catalog.get_objective_form_for_create([])
        create_form.display_name = 'Test Objective for Activity Lookup'
        create_form.description = 'Test Objective for ActivityLookupSession tests'
        cls.objective = cls.catalog.create_objective(create_form)

    def setUp(self):
        # Since the session isn't implemented, we just construct an ActivityQuery directly
        self.query = ActivityQuery(runtime=self.catalog._runtime)

    @classmethod
    def tearDownClass(cls):
        for catalog in cls.svc_mgr.get_objective_banks():
            for obj in catalog.get_activities():
                catalog.delete_activity(obj.ident)
            for obj in catalog.get_objectives():
                catalog.delete_objective(obj.ident)
            cls.svc_mgr.delete_objective_bank(catalog.ident)

    def test_match_objective_id(self):
        """Tests match_objective_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('objectiveId', self.query._query_terms)
        self.query.match_objective_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['objectiveId'], {
            '$in': [str(test_id)]
        })

    def test_clear_objective_id_terms(self):
        """Tests clear_objective_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_objective_id(test_id, match=True)
        self.assertIn('objectiveId',
                      self.query._query_terms)
        self.query.clear_objective_id_terms()
        self.assertNotIn('objectiveId',
                         self.query._query_terms)

    def test_supports_objective_query(self):
        """Tests supports_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_objective_query()

    def test_get_objective_query(self):
        """Tests get_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_objective_query()

    def test_clear_objective_terms(self):
        """Tests clear_objective_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['objective'] = 'foo'
        self.query.clear_objective_terms()
        self.assertNotIn('objective',
                         self.query._query_terms)

    def test_match_asset_id(self):
        """Tests match_asset_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('assetId', self.query._query_terms)
        self.query.match_asset_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['assetId'], {
            '$in': [str(test_id)]
        })

    def test_clear_asset_id_terms(self):
        """Tests clear_asset_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_asset_id(test_id, match=True)
        self.assertIn('assetId',
                      self.query._query_terms)
        self.query.clear_asset_id_terms()
        self.assertNotIn('assetId',
                         self.query._query_terms)

    def test_supports_asset_query(self):
        """Tests supports_asset_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_asset_query()

    def test_get_asset_query(self):
        """Tests get_asset_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_asset_query()

    def test_match_any_asset(self):
        """Tests match_any_asset"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_asset(True)

    def test_clear_asset_terms(self):
        """Tests clear_asset_terms"""
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_asset_terms()

    def test_match_course_id(self):
        """Tests match_course_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('courseId', self.query._query_terms)
        self.query.match_course_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['courseId'], {
            '$in': [str(test_id)]
        })

    def test_clear_course_id_terms(self):
        """Tests clear_course_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_course_id(test_id, match=True)
        self.assertIn('courseId',
                      self.query._query_terms)
        self.query.clear_course_id_terms()
        self.assertNotIn('courseId',
                         self.query._query_terms)

    def test_supports_course_query(self):
        """Tests supports_course_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_course_query()

    def test_get_course_query(self):
        """Tests get_course_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_course_query()

    def test_match_any_course(self):
        """Tests match_any_course"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_course(True)

    def test_clear_course_terms(self):
        """Tests clear_course_terms"""
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_course_terms()

    def test_match_assessment_id(self):
        """Tests match_assessment_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('assessmentId', self.query._query_terms)
        self.query.match_assessment_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['assessmentId'], {
            '$in': [str(test_id)]
        })

    def test_clear_assessment_id_terms(self):
        """Tests clear_assessment_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_assessment_id(test_id, match=True)
        self.assertIn('assessmentId',
                      self.query._query_terms)
        self.query.clear_assessment_id_terms()
        self.assertNotIn('assessmentId',
                         self.query._query_terms)

    def test_supports_assessment_query(self):
        """Tests supports_assessment_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_assessment_query()

    def test_get_assessment_query(self):
        """Tests get_assessment_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_assessment_query()

    def test_match_any_assessment(self):
        """Tests match_any_assessment"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_assessment(True)

    def test_clear_assessment_terms(self):
        """Tests clear_assessment_terms"""
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_assessment_terms()

    def test_match_objective_bank_id(self):
        """Tests match_objective_bank_id"""
        # From test_templates/resource.py::ResourceQuery::match_bin_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_objective_bank_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['assignedObjectiveBankIds'], {
            '$in': [str(test_id)]
        })

    def test_clear_objective_bank_id_terms(self):
        """Tests clear_objective_bank_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_bin_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_objective_bank_id(test_id, match=True)
        self.assertIn('assignedObjectiveBankIds',
                      self.query._query_terms)
        self.query.clear_objective_bank_id_terms()
        self.assertNotIn('assignedObjectiveBankIds',
                         self.query._query_terms)

    def test_supports_objective_bank_query(self):
        """Tests supports_objective_bank_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_objective_bank_query()

    def test_get_objective_bank_query(self):
        """Tests get_objective_bank_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_objective_bank_query()

    def test_clear_objective_bank_terms(self):
        """Tests clear_objective_bank_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['objectiveBank'] = 'foo'
        self.query.clear_objective_bank_terms()
        self.assertNotIn('objectiveBank',
                         self.query._query_terms)

    def test_get_activity_query_record(self):
        """Tests get_activity_query_record"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_activity_query_record(True)


class TestProficiencyQuery(unittest.TestCase):
    """Tests for ProficiencyQuery"""

    @classmethod
    def setUpClass(cls):
        # From test_templates/resource.py::ResourceQuery::init_template
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)

    def setUp(self):
        # From test_templates/resource.py::ResourceQuery::init_template
        self.query = self.catalog.get_proficiency_query()

    @classmethod
    def tearDownClass(cls):
        # From test_templates/resource.py::ResourceQuery::init_template
        cls.svc_mgr.delete_objective_bank(cls.catalog.ident)

    def test_match_resource_id(self):
        """Tests match_resource_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('resourceId', self.query._query_terms)
        self.query.match_resource_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['resourceId'], {
            '$in': [str(test_id)]
        })

    def test_clear_resource_id_terms(self):
        """Tests clear_resource_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_resource_id(test_id, match=True)
        self.assertIn('resourceId',
                      self.query._query_terms)
        self.query.clear_resource_id_terms()
        self.assertNotIn('resourceId',
                         self.query._query_terms)

    def test_supports_resource_query(self):
        """Tests supports_resource_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_resource_query()

    def test_get_resource_query(self):
        """Tests get_resource_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_resource_query()

    def test_clear_resource_terms(self):
        """Tests clear_resource_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['resource'] = 'foo'
        self.query.clear_resource_terms()
        self.assertNotIn('resource',
                         self.query._query_terms)

    def test_match_objective_id(self):
        """Tests match_objective_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('objectiveId', self.query._query_terms)
        self.query.match_objective_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['objectiveId'], {
            '$in': [str(test_id)]
        })

    def test_clear_objective_id_terms(self):
        """Tests clear_objective_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_objective_id(test_id, match=True)
        self.assertIn('objectiveId',
                      self.query._query_terms)
        self.query.clear_objective_id_terms()
        self.assertNotIn('objectiveId',
                         self.query._query_terms)

    def test_supports_objective_query(self):
        """Tests supports_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_objective_query()

    def test_get_objective_query(self):
        """Tests get_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_objective_query()

    def test_match_any_objective(self):
        """Tests match_any_objective"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_objective(True)

    def test_clear_objective_terms(self):
        """Tests clear_objective_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['objective'] = 'foo'
        self.query.clear_objective_terms()
        self.assertNotIn('objective',
                         self.query._query_terms)

    def test_match_completion(self):
        """Tests match_completion"""
        start = float(0.0)
        end = float(100.0)
        self.assertNotIn('completion', self.query._query_terms)
        self.query.match_completion(start, end, True)
        self.assertEqual(self.query._query_terms['completion'], {
            '$gte': start,
            '$lte': end
        })

    def test_clear_completion_terms(self):
        """Tests clear_completion_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['completion'] = 'foo'
        self.query.clear_completion_terms()
        self.assertNotIn('completion',
                         self.query._query_terms)

    def test_match_minimum_completion(self):
        """Tests match_minimum_completion"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_minimum_completion(float(50.0), True)

    def test_clear_minimum_completion_terms(self):
        """Tests clear_minimum_completion_terms"""
        with self.assertRaises(errors.Unimplemented):
            self.query.clear_minimum_completion_terms()

    def test_match_level_id(self):
        """Tests match_level_id"""
        # From test_templates/resource.py::ResourceQuery::match_avatar_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.assertNotIn('levelId', self.query._query_terms)
        self.query.match_level_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['levelId'], {
            '$in': [str(test_id)]
        })

    def test_clear_level_id_terms(self):
        """Tests clear_level_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_avatar_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_level_id(test_id, match=True)
        self.assertIn('levelId',
                      self.query._query_terms)
        self.query.clear_level_id_terms()
        self.assertNotIn('levelId',
                         self.query._query_terms)

    def test_supports_level_query(self):
        """Tests supports_level_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_level_query()

    def test_get_level_query(self):
        """Tests get_level_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_level_query()

    def test_match_any_level(self):
        """Tests match_any_level"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_level(True)

    def test_clear_level_terms(self):
        """Tests clear_level_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['level'] = 'foo'
        self.query.clear_level_terms()
        self.assertNotIn('level',
                         self.query._query_terms)

    def test_match_objective_bank_id(self):
        """Tests match_objective_bank_id"""
        # From test_templates/resource.py::ResourceQuery::match_bin_id_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_objective_bank_id(test_id, match=True)
        self.assertEqual(self.query._query_terms['assignedObjectiveBankIds'], {
            '$in': [str(test_id)]
        })

    def test_clear_objective_bank_id_terms(self):
        """Tests clear_objective_bank_id_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_bin_id_terms_template
        test_id = Id('osid.Osid%3Afake%40ODL.MIT.EDU')
        self.query.match_objective_bank_id(test_id, match=True)
        self.assertIn('assignedObjectiveBankIds',
                      self.query._query_terms)
        self.query.clear_objective_bank_id_terms()
        self.assertNotIn('assignedObjectiveBankIds',
                         self.query._query_terms)

    def test_supports_objective_bank_query(self):
        """Tests supports_objective_bank_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_objective_bank_query()

    def test_get_objective_bank_query(self):
        """Tests get_objective_bank_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_objective_bank_query()

    def test_clear_objective_bank_terms(self):
        """Tests clear_objective_bank_terms"""
        # From test_templates/resource.py::ResourceQuery::clear_group_terms_template
        self.query._query_terms['objectiveBank'] = 'foo'
        self.query.clear_objective_bank_terms()
        self.assertNotIn('objectiveBank',
                         self.query._query_terms)

    def test_get_proficiency_query_record(self):
        """Tests get_proficiency_query_record"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_proficiency_query_record(True)


class TestObjectiveBankQuery(unittest.TestCase):
    """Tests for ObjectiveBankQuery"""

    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('LEARNING', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_objective_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_objective_bank(create_form)
        cls.fake_id = Id('resource.Resource%3A1%40ODL.MIT.EDU')

    def setUp(self):
        # Since the session isn't implemented, we just construct an ObjectiveBankQuery directly
        self.query = ObjectiveBankQuery(runtime=self.catalog._runtime)

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_objective_bank(cls.catalog.ident)

    def test_match_objective_id(self):
        """Tests match_objective_id"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_objective_id(True, True)

    def test_clear_objective_id_terms(self):
        """Tests clear_objective_id_terms"""
        # From test_templates/resource.py::BinQuery::clear_group_terms_template
        self.query._query_terms['objectiveId'] = 'foo'
        self.query.clear_objective_id_terms()
        self.assertNotIn('objectiveId',
                         self.query._query_terms)

    def test_supports_objective_query(self):
        """Tests supports_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_objective_query()

    def test_get_objective_query(self):
        """Tests get_objective_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_objective_query()

    def test_match_any_objective(self):
        """Tests match_any_objective"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_objective(True)

    def test_clear_objective_terms(self):
        """Tests clear_objective_terms"""
        # From test_templates/resource.py::BinQuery::clear_group_terms_template
        self.query._query_terms['objective'] = 'foo'
        self.query.clear_objective_terms()
        self.assertNotIn('objective',
                         self.query._query_terms)

    def test_match_activity_id(self):
        """Tests match_activity_id"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_activity_id(True, True)

    def test_clear_activity_id_terms(self):
        """Tests clear_activity_id_terms"""
        # From test_templates/resource.py::BinQuery::clear_group_terms_template
        self.query._query_terms['activityId'] = 'foo'
        self.query.clear_activity_id_terms()
        self.assertNotIn('activityId',
                         self.query._query_terms)

    def test_supports_activity_query(self):
        """Tests supports_activity_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_activity_query()

    def test_get_activity_query(self):
        """Tests get_activity_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_activity_query()

    def test_match_any_activity(self):
        """Tests match_any_activity"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_activity(True)

    def test_clear_activity_terms(self):
        """Tests clear_activity_terms"""
        # From test_templates/resource.py::BinQuery::clear_group_terms_template
        self.query._query_terms['activity'] = 'foo'
        self.query.clear_activity_terms()
        self.assertNotIn('activity',
                         self.query._query_terms)

    def test_match_ancestor_objective_bank_id(self):
        """Tests match_ancestor_objective_bank_id"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_ancestor_objective_bank_id(True, True)

    def test_clear_ancestor_objective_bank_id_terms(self):
        """Tests clear_ancestor_objective_bank_id_terms"""
        # From test_templates/resource.py::BinQuery::clear_group_terms_template
        self.query._query_terms['ancestorObjectiveBankId'] = 'foo'
        self.query.clear_ancestor_objective_bank_id_terms()
        self.assertNotIn('ancestorObjectiveBankId',
                         self.query._query_terms)

    def test_supports_ancestor_objective_bank_query(self):
        """Tests supports_ancestor_objective_bank_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_ancestor_objective_bank_query()

    def test_get_ancestor_objective_bank_query(self):
        """Tests get_ancestor_objective_bank_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_ancestor_objective_bank_query()

    def test_match_any_ancestor_objective_bank(self):
        """Tests match_any_ancestor_objective_bank"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_ancestor_objective_bank(True)

    def test_clear_ancestor_objective_bank_terms(self):
        """Tests clear_ancestor_objective_bank_terms"""
        # From test_templates/resource.py::BinQuery::clear_group_terms_template
        self.query._query_terms['ancestorObjectiveBank'] = 'foo'
        self.query.clear_ancestor_objective_bank_terms()
        self.assertNotIn('ancestorObjectiveBank',
                         self.query._query_terms)

    def test_match_descendant_objective_bank_id(self):
        """Tests match_descendant_objective_bank_id"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_descendant_objective_bank_id(True, True)

    def test_clear_descendant_objective_bank_id_terms(self):
        """Tests clear_descendant_objective_bank_id_terms"""
        # From test_templates/resource.py::BinQuery::clear_group_terms_template
        self.query._query_terms['descendantObjectiveBankId'] = 'foo'
        self.query.clear_descendant_objective_bank_id_terms()
        self.assertNotIn('descendantObjectiveBankId',
                         self.query._query_terms)

    def test_supports_descendant_objective_bank_query(self):
        """Tests supports_descendant_objective_bank_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.supports_descendant_objective_bank_query()

    def test_get_descendant_objective_bank_query(self):
        """Tests get_descendant_objective_bank_query"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_descendant_objective_bank_query()

    def test_match_any_descendant_objective_bank(self):
        """Tests match_any_descendant_objective_bank"""
        with self.assertRaises(errors.Unimplemented):
            self.query.match_any_descendant_objective_bank(True)

    def test_clear_descendant_objective_bank_terms(self):
        """Tests clear_descendant_objective_bank_terms"""
        # From test_templates/resource.py::BinQuery::clear_group_terms_template
        self.query._query_terms['descendantObjectiveBank'] = 'foo'
        self.query.clear_descendant_objective_bank_terms()
        self.assertNotIn('descendantObjectiveBank',
                         self.query._query_terms)

    def test_get_objective_bank_query_record(self):
        """Tests get_objective_bank_query_record"""
        with self.assertRaises(errors.Unimplemented):
            self.query.get_objective_bank_query_record(True)
