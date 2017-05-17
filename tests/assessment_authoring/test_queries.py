"""Unit tests of assessment.authoring queries."""


import unittest


class TestAssessmentPartQuery(unittest.TestCase):
    """Tests for AssessmentPartQuery"""

    @classmethod
    def setUpClass(cls):
        cls.svc_mgr = Runtime().get_service_manager('ASSESSMENT', proxy=PROXY, implementation='TEST_SERVICE')
        create_form = cls.svc_mgr.get_bank_form_for_create([])
        create_form.display_name = 'Test catalog'
        create_form.description = 'Test catalog description'
        cls.catalog = cls.svc_mgr.create_bank(create_form)

        cls.query = cls.catalog.get_assessment_part_query()

    @classmethod
    def tearDownClass(cls):
        cls.svc_mgr.delete_bank(cls.catalog.ident)

    @unittest.skip('unimplemented test')
    def test_match_assessment_id(self):
        """Tests match_assessment_id"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_assessment_id_terms(self):
        """Tests clear_assessment_id_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_supports_assessment_query(self):
        """Tests supports_assessment_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_assessment_query(self):
        """Tests get_assessment_query"""
        pass

    def test_clear_assessment_terms(self):
        """Tests clear_assessment_terms"""
        

    @unittest.skip('unimplemented test')
    def test_match_parent_assessment_part_id(self):
        """Tests match_parent_assessment_part_id"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_parent_assessment_part_id_terms(self):
        """Tests clear_parent_assessment_part_id_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_supports_parent_assessment_part_query(self):
        """Tests supports_parent_assessment_part_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_parent_assessment_part_query(self):
        """Tests get_parent_assessment_part_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_any_parent_assessment_part(self):
        """Tests match_any_parent_assessment_part"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_parent_assessment_part_terms(self):
        """Tests clear_parent_assessment_part_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_section(self):
        """Tests match_section"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_section_terms(self):
        """Tests clear_section_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_weight(self):
        """Tests match_weight"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_any_weight(self):
        """Tests match_any_weight"""
        pass

    def test_clear_weight_terms(self):
        """Tests clear_weight_terms"""
        

    @unittest.skip('unimplemented test')
    def test_match_allocated_time(self):
        """Tests match_allocated_time"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_any_allocated_time(self):
        """Tests match_any_allocated_time"""
        pass

    def test_clear_allocated_time_terms(self):
        """Tests clear_allocated_time_terms"""
        

    @unittest.skip('unimplemented test')
    def test_match_child_assessment_part_id(self):
        """Tests match_child_assessment_part_id"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_child_assessment_part_id_terms(self):
        """Tests clear_child_assessment_part_id_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_supports_child_assessment_part_query(self):
        """Tests supports_child_assessment_part_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_child_assessment_part_query(self):
        """Tests get_child_assessment_part_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_any_child_assessment_part(self):
        """Tests match_any_child_assessment_part"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_child_assessment_part_terms(self):
        """Tests clear_child_assessment_part_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_bank_id(self):
        """Tests match_bank_id"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_bank_id_terms(self):
        """Tests clear_bank_id_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_supports_bank_query(self):
        """Tests supports_bank_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_bank_query(self):
        """Tests get_bank_query"""
        pass

    def test_clear_bank_terms(self):
        """Tests clear_bank_terms"""
        

    @unittest.skip('unimplemented test')
    def test_get_assessment_part_query_record(self):
        """Tests get_assessment_part_query_record"""
        pass


class TestSequenceRuleQuery(unittest.TestCase):
    """Tests for SequenceRuleQuery"""

    @unittest.skip('unimplemented test')
    def test_match_assessment_part_id(self):
        """Tests match_assessment_part_id"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_assessment_part_id_terms(self):
        """Tests clear_assessment_part_id_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_supports_assessment_part_query(self):
        """Tests supports_assessment_part_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_assessment_part_query(self):
        """Tests get_assessment_part_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_assessment_part_terms(self):
        """Tests clear_assessment_part_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_next_assessment_part_id(self):
        """Tests match_next_assessment_part_id"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_next_assessment_part_id_terms(self):
        """Tests clear_next_assessment_part_id_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_supports_next_assessment_part_query(self):
        """Tests supports_next_assessment_part_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_next_assessment_part_query(self):
        """Tests get_next_assessment_part_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_next_assessment_part_terms(self):
        """Tests clear_next_assessment_part_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_minimum_score(self):
        """Tests match_minimum_score"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_any_minimum_score(self):
        """Tests match_any_minimum_score"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_minimum_score_terms(self):
        """Tests clear_minimum_score_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_maximum_score(self):
        """Tests match_maximum_score"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_any_maximum_score(self):
        """Tests match_any_maximum_score"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_maximum_score_terms(self):
        """Tests clear_maximum_score_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_cumulative(self):
        """Tests match_cumulative"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_cumulative_terms(self):
        """Tests clear_cumulative_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_applied_assessment_part_id(self):
        """Tests match_applied_assessment_part_id"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_applied_assessment_part_id_terms(self):
        """Tests clear_applied_assessment_part_id_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_supports_applied_assessment_part_query(self):
        """Tests supports_applied_assessment_part_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_applied_assessment_part_query(self):
        """Tests get_applied_assessment_part_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_any_applied_assessment_part(self):
        """Tests match_any_applied_assessment_part"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_applied_assessment_part_terms(self):
        """Tests clear_applied_assessment_part_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_match_bank_id(self):
        """Tests match_bank_id"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_bank_id_terms(self):
        """Tests clear_bank_id_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_supports_bank_query(self):
        """Tests supports_bank_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_bank_query(self):
        """Tests get_bank_query"""
        pass

    @unittest.skip('unimplemented test')
    def test_clear_bank_terms(self):
        """Tests clear_bank_terms"""
        pass

    @unittest.skip('unimplemented test')
    def test_get_sequence_rule_query_record(self):
        """Tests get_sequence_rule_query_record"""
        pass
