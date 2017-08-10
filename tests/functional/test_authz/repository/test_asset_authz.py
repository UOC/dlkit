"""TestAuthZ implementations of repository.Asset"""

import datetime
import pytest
from tests.utilities.general import is_never_authz, is_no_authz, uses_cataloging
from dlkit.abstract_osid.authorization import objects as ABCObjects
from dlkit.abstract_osid.authorization import queries as ABCQueries
from dlkit.abstract_osid.authorization.objects import Authorization
from dlkit.abstract_osid.authorization.objects import AuthorizationList
from dlkit.abstract_osid.authorization.objects import Vault as ABCVault
from dlkit.abstract_osid.osid import errors
from dlkit.abstract_osid.osid.objects import OsidCatalogForm, OsidCatalog
from dlkit.abstract_osid.osid.objects import OsidForm
from dlkit.primordium.calendaring.primitives import DateTime
from dlkit.primordium.id.primitives import Id
from dlkit.primordium.type.primitives import Type
from dlkit.runtime import PROXY_SESSION, proxy_example
from dlkit.runtime.managers import Runtime
REQUEST = proxy_example.SimpleRequest()
CONDITION = PROXY_SESSION.get_proxy_condition()
CONDITION.set_http_request(REQUEST)
PROXY = PROXY_SESSION.get_proxy(CONDITION)

JANE_REQUEST = proxy_example.SimpleRequest(username='jane_doe')
JANE_CONDITION = PROXY_SESSION.get_proxy_condition()
JANE_CONDITION.set_http_request(JANE_REQUEST)
JANE_PROXY = PROXY_SESSION.get_proxy(JANE_CONDITION)

LOOKUP_ASSET_FUNCTION_ID = Id(**{'identifier': 'lookup', 'namespace': 'repository.Asset', 'authority': 'ODL.MIT.EDU'})
SEARCH_ASSET_FUNCTION_ID = Id(**{'identifier': 'search', 'namespace': 'repository.Asset', 'authority': 'ODL.MIT.EDU'})
CREATE_ASSET_FUNCTION_ID = Id(**{'identifier': 'create', 'namespace': 'repository.Asset', 'authority': 'ODL.MIT.EDU'})
DELETE_ASSET_FUNCTION_ID = Id(**{'identifier': 'delete', 'namespace': 'repository.Asset', 'authority': 'ODL.MIT.EDU'})
ASSIGN_ASSET_FUNCTION_ID = Id(**{'identifier': 'assign', 'namespace': 'repository.AssetRepository', 'authority': 'ODL.MIT.EDU'})
CREATE_REPOSITORY_FUNCTION_ID = Id(**{'identifier': 'create', 'namespace': 'repository.Repository', 'authority': 'ODL.MIT.EDU'})
DELETE_REPOSITORY_FUNCTION_ID = Id(**{'identifier': 'delete', 'namespace': 'repository.Repository', 'authority': 'ODL.MIT.EDU'})
LOOKUP_REPOSITORY_FUNCTION_ID = Id(**{'identifier': 'lookup', 'namespace': 'repository.Repository', 'authority': 'ODL.MIT.EDU'})
ACCESS_REPOSITORY_HIERARCHY_FUNCTION_ID = Id(**{'identifier': 'access', 'namespace': 'repository.Repository', 'authority': 'ODL.MIT.EDU'})
MODIFY_REPOSITORY_HIERARCHY_FUNCTION_ID = Id(**{'identifier': 'modify', 'namespace': 'repository.Repository', 'authority': 'ODL.MIT.EDU'})
ROOT_QUALIFIER_ID = Id('repository.Repository%3AROOT%40ODL.MIT.EDU')
BOOTSTRAP_VAULT_TYPE = Type(authority='ODL.MIT.EDU', namespace='authorization.Vault', identifier='bootstrap_vault')
OVERRIDE_VAULT_TYPE = Type(authority='ODL.MIT.EDU', namespace='authorization.Vault', identifier='override_vault')
DEFAULT_TYPE = Type(**{'identifier': 'DEFAULT', 'namespace': 'DEFAULT', 'authority': 'DEFAULT'})
DEFAULT_GENUS_TYPE = Type(**{'identifier': 'DEFAULT', 'namespace': 'GenusType', 'authority': 'DLKIT.MIT.EDU'})
ALIAS_ID = Id(**{'identifier': 'ALIAS', 'namespace': 'ALIAS', 'authority': 'ALIAS'})
AGENT_ID = Id(**{'identifier': 'jane_doe', 'namespace': 'osid.agent.Agent', 'authority': 'MIT-ODL'})
NEW_TYPE = Type(**{'identifier': 'NEW', 'namespace': 'MINE', 'authority': 'YOURS'})
NEW_TYPE_2 = Type(**{'identifier': 'NEW 2', 'namespace': 'MINE', 'authority': 'YOURS'})
BLUE_TYPE = Type(authority='BLUE', namespace='BLUE', identifier='BLUE')


@pytest.fixture(scope="class",
                params=['TEST_SERVICE'])
def authz_adapter_class_fixture(request):
    request.cls.service_config = request.param
    request.cls.authz_mgr = Runtime().get_manager(
        'AUTHORIZATION',
        implementation='TEST_SERVICE')
    if not is_never_authz(request.cls.service_config):
        request.cls.vault_admin_session = request.cls.authz_mgr.get_vault_admin_session()
        request.cls.vault_lookup_session = request.cls.authz_mgr.get_vault_lookup_session()

        create_form = request.cls.vault_admin_session.get_vault_form_for_create([])
        create_form.display_name = 'Test Vault'
        create_form.description = 'Test Vault for AuthorizationSession tests'
        create_form.genus_type = BOOTSTRAP_VAULT_TYPE
        request.cls.vault = request.cls.vault_admin_session.create_vault(create_form)

        create_form = request.cls.vault_admin_session.get_vault_form_for_create([])
        create_form.display_name = 'Test Override Vault'
        create_form.description = 'Test Override Vault for AuthorizationSession tests'
        create_form.genus_type = OVERRIDE_VAULT_TYPE
        request.cls.override_vault = request.cls.vault_admin_session.create_vault(create_form)

        request.cls.authz_admin_session = request.cls.authz_mgr.get_authorization_admin_session_for_vault(request.cls.vault.ident)
        request.cls.override_authz_admin_session = request.cls.authz_mgr.get_authorization_admin_session_for_vault(request.cls.override_vault.ident)
        request.cls.authz_lookup_session = request.cls.authz_mgr.get_authorization_lookup_session_for_vault(request.cls.vault.ident)

        request.cls.repository_list = list()
        request.cls.repository_id_list = list()
        request.cls.authz_list = list()
        request.cls.authz_id_list = list()
        request.cls.repository_mgr = Runtime().get_service_manager(
            'REPOSITORY',
            proxy=PROXY,
            implementation='TEST_SERVICE')
        for num in [0, 1, 2, 3, 4, 5, 6, 7]:
            create_form = request.cls.repository_mgr.get_repository_form_for_create([])
            create_form.display_name = 'Test Repository ' + str(num)
            create_form.description = 'Test Repository for Testing Authorization Number: ' + str(num)
            repository = request.cls.repository_mgr.create_repository(create_form)
            request.cls.repository_list.append(repository)
            request.cls.repository_id_list.append(repository.ident)

        request.cls.repository_mgr.add_root_repository(request.cls.repository_id_list[0])
        request.cls.repository_mgr.add_child_repository(request.cls.repository_id_list[0], request.cls.repository_id_list[1])
        request.cls.repository_mgr.add_child_repository(request.cls.repository_id_list[0], request.cls.repository_id_list[2])
        request.cls.repository_mgr.add_child_repository(request.cls.repository_id_list[1], request.cls.repository_id_list[3])
        request.cls.repository_mgr.add_child_repository(request.cls.repository_id_list[1], request.cls.repository_id_list[4])
        request.cls.repository_mgr.add_child_repository(request.cls.repository_id_list[2], request.cls.repository_id_list[5])

        # The hierarchy should look like this. (t) indicates where lookup is
        # explicitely authorized:
        #
        #            _____ 0 _____
        #           |             |
        #        _ 1(t) _         2     not in hierarchy
        #       |        |        |
        #       3        4       5(t)      6     7(t)   (the 'blue' asset in repository 2 is also assigned to repository 7)

        request.cls.svc_mgr = Runtime().get_service_manager(
            'AUTHORIZATION',
            proxy=PROXY,
            implementation=request.cls.service_config)
        request.cls.catalog = request.cls.svc_mgr.get_vault(request.cls.vault.ident)

        # Set up Repository lookup authorization for Jane
        create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
            AGENT_ID,
            LOOKUP_REPOSITORY_FUNCTION_ID,
            ROOT_QUALIFIER_ID,
            [])
        create_form.display_name = 'Jane Lookup Authorization'
        create_form.description = 'Test Authorization for AuthorizationSession tests'
        jane_lookup_authz = request.cls.authz_admin_session.create_authorization(create_form)
        request.cls.authz_list.append(jane_lookup_authz)
        request.cls.authz_id_list.append(jane_lookup_authz.ident)

        # Set up Asset lookup authorizations for Jane
        for num in [1, 5]:
            create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_ASSET_FUNCTION_ID,
                request.cls.repository_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationSession tests'
            authz = request.cls.authz_admin_session.create_authorization(create_form)
            request.cls.authz_list.append(authz)
            request.cls.authz_id_list.append(authz.ident)

        # Set up Asset lookup override authorizations for Jane
        for num in [7]:
            create_form = request.cls.override_authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                LOOKUP_ASSET_FUNCTION_ID,
                request.cls.repository_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num) + ' (override)'
            create_form.description = 'Test Authorization for AuthorizationSession tests'
            authz = request.cls.override_authz_admin_session.create_authorization(create_form)
            request.cls.authz_list.append(authz)
            request.cls.authz_id_list.append(authz.ident)

        # Set up Asset search override authorizations for Jane
        for num in [7]:
            create_form = request.cls.override_authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                SEARCH_ASSET_FUNCTION_ID,
                request.cls.repository_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num) + ' (override)'
            create_form.description = 'Test Authorization for AuthorizationSession tests'
            authz = request.cls.override_authz_admin_session.create_authorization(create_form)
            request.cls.authz_list.append(authz)
            request.cls.authz_id_list.append(authz.ident)

        # Set up Asset search authorizations for Jane
        for num in [1, 5]:
            create_form = request.cls.authz_admin_session.get_authorization_form_for_create_for_agent(
                AGENT_ID,
                SEARCH_ASSET_FUNCTION_ID,
                request.cls.repository_id_list[num],
                [])
            create_form.display_name = 'Test Authorization ' + str(num)
            create_form.description = 'Test Authorization for AuthorizationSession tests'
            authz = request.cls.authz_admin_session.create_authorization(create_form)
            request.cls.authz_list.append(authz)
            request.cls.authz_id_list.append(authz.ident)

    else:
        request.cls.catalog = request.cls.svc_mgr.get_authorization_session(proxy=PROXY)

    def class_tear_down():
        if not is_never_authz(request.cls.service_config):
            for catalog in request.cls.repository_mgr.get_repositories():
                for obj in catalog.get_assets():
                    catalog.delete_asset(obj.ident)
                request.cls.repository_mgr.delete_repository(catalog.ident)
            for vault in request.cls.vault_lookup_session.get_vaults():
                lookup_session = request.cls.authz_mgr.get_authorization_lookup_session_for_vault(vault.ident)
                admin_session = request.cls.authz_mgr.get_authorization_admin_session_for_vault(vault.ident)
                for authz in lookup_session.get_authorizations():
                    admin_session.delete_authorization(authz.ident)
                request.cls.vault_admin_session.delete_vault(vault.ident)

    request.addfinalizer(class_tear_down)


@pytest.fixture(scope="function")
def authz_adapter_test_fixture(request):
    request.cls.asset_id_lists = []
    count = 0
    if not is_never_authz(request.cls.service_config):
        for repository_ in request.cls.repository_list:
            request.cls.asset_id_lists.append([])
            for color in ['Red', 'Blue', 'Red']:
                create_form = repository_.get_asset_form_for_create([])
                create_form.display_name = color + ' ' + str(count) + ' Asset'
                create_form.description = color + ' asset for authz adapter tests from Repository number ' + str(count)
                if color == 'Blue':
                    create_form.genus_type = BLUE_TYPE
                asset = repository_.create_asset(create_form)
                if count == 2 and color == 'Blue':
                    request.cls.repository_mgr.assign_asset_to_repository(
                        asset.ident,
                        request.cls.repository_id_list[7])
                request.cls.asset_id_lists[count].append(asset.ident)
            count += 1

    def test_tear_down():
        if not is_never_authz(request.cls.service_config):
            for index, repository_ in enumerate(request.cls.repository_list):
                for asset_id in request.cls.asset_id_lists[index]:
                    repository_.delete_asset(asset_id)

    request.addfinalizer(test_tear_down)


@pytest.mark.usefixtures("authz_adapter_class_fixture", "authz_adapter_test_fixture")
class TestAssetAuthzAdapter(object):

    def test_lookup_repository_0_plenary_isolated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[0])
            repository.use_isolated_repository_view()
            repository.use_plenary_asset_view()
            # with pytest.raises(errors.NotFound):
            #     assets = repository.get_assets()
            # with pytest.raises(errors.NotFound):
            #     assets = repository.get_assets_by_genus_type(BLUE_TYPE)
            # for asset_id in self.asset_id_lists[0]:
            #     with pytest.raises(errors.NotFound):
            #         asset = repository.get_asset(asset_id)
            # with pytest.raises(errors.NotFound):
            #     assets = repository.get_assets_by_ids(self.asset_id_lists[0])

    def test_lookup_repository_0_plenary_federated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[0])
            repository.use_federated_repository_view()
            repository.use_plenary_asset_view()
            assert repository.can_lookup_assets()
            assert repository.get_assets().available() == 1
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 1
            assert repository.get_assets_by_genus_type(BLUE_TYPE).next().ident == self.asset_id_lists[2][1]
            repository.get_asset(self.asset_id_lists[2][1])
            for asset_num in [0, 2]:
                with pytest.raises(errors.NotFound):  # Is this right?  Perhaps PermissionDenied
                    asset = repository.get_asset(self.asset_id_lists[2][asset_num])

    def test_lookup_repository_0_comparative_federated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[0])
            repository.use_federated_repository_view()
            repository.use_comparative_asset_view()
            # print "START"
            assert repository.get_assets().available() == 13
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 5
            for asset in repository.get_assets():
                repository.get_asset(asset.ident)
            asset_ids = [asset.ident for asset in repository.get_assets()]
            repository.get_assets_by_ids(asset_ids)
            for asset_id in self.asset_id_lists[0]:
                with pytest.raises(errors.NotFound):
                    asset = repository.get_asset(asset_id)
            asset = repository.get_asset(self.asset_id_lists[2][1])
            for asset_num in [0, 2]:
                with pytest.raises(errors.NotFound):
                    asset = repository.get_asset(self.asset_id_lists[2][asset_num])
            for asset_id in self.asset_id_lists[1]:
                    asset = repository.get_asset(asset_id)
            for asset_id in self.asset_id_lists[3]:
                    asset = repository.get_asset(asset_id)
            for asset_id in self.asset_id_lists[4]:
                    asset = repository.get_asset(asset_id)
            for asset_id in self.asset_id_lists[5]:
                    asset = repository.get_asset(asset_id)

    def test_lookup_repository_0_comparative_isolated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[0])
            repository.use_isolated_repository_view()
            repository.use_comparative_asset_view()
            assert repository.get_assets().available() == 0
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 0

    def test_lookup_repository_1_plenary_isolated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[1])
            repository.use_isolated_repository_view()
            repository.use_plenary_asset_view()
            assert repository.get_assets().available() == 3
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 1

    def test_lookup_repository_1_plenary_federated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[1])
            repository.use_federated_repository_view()
            repository.use_plenary_asset_view()
            assert repository.get_assets().available() == 9
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 3

    def test_lookup_repository_1_comparative_federated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[1])
            repository.use_federated_repository_view()
            repository.use_comparative_asset_view()
            assert repository.get_assets().available() == 9
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 3

    def test_lookup_repository_1_comparative_isolated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[1])
            repository.use_isolated_repository_view()
            repository.use_comparative_asset_view()
            assert repository.get_assets().available() == 3
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 1

    def test_lookup_repository_2_plenary_isolated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[2])
            repository.use_isolated_repository_view()
            repository.use_plenary_asset_view()
            assert repository.get_assets().available() == 1
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 1
            # with pytest.raises(errors.PermissionDenied):
            #     assets = repository.get_assets()
            # with pytest.raises(errors.PermissionDenied):
            #     assets = repository.get_assets_by_genus_type(BLUE_TYPE)

    def test_lookup_repository_2_plenary_federated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[2])
            repository.use_federated_repository_view()
            repository.use_plenary_asset_view()
            assert repository.get_assets().available() == 1
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 1
            # with pytest.raises(errors.PermissionDenied):
            #     assets = repository.get_assets()
            # with pytest.raises(errors.PermissionDenied):
            #     assets = repository.get_assets_by_genus_type(BLUE_TYPE)

    def test_lookup_repository_2_comparative_federated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[2])
            repository.use_federated_repository_view()
            repository.use_comparative_asset_view()
            assert repository.get_assets().available() == 4
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 2
            # self.assertEqual(repository.get_assets().available(), 3)
            # self.assertEqual(repository.get_assets_by_genus_type(BLUE_TYPE).available(), 1)

    def test_lookup_repository_2_comparative_isolated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[2])
            repository.use_isolated_repository_view()
            repository.use_comparative_asset_view()
            assert repository.get_assets().available() == 1
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 1
            # with pytest.raises(errors.PermissionDenied):
            #     assets = repository.get_assets()
            # with pytest.raises(errors.PermissionDenied):
            #     assets = repository.get_assets_by_genus_type(BLUE_TYPE)

    def test_lookup_repository_3_plenary_isolated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[3])
            repository.use_isolated_repository_view()
            repository.use_plenary_asset_view()
            assert repository.get_assets().available() == 3
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 1

    def test_lookup_repository_3_plenary_federated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[3])
            repository.use_federated_repository_view()
            repository.use_plenary_asset_view()
            assert repository.get_assets().available() == 3
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 1

    def test_lookup_repository_3_comparative_federated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[3])
            repository.use_federated_repository_view()
            repository.use_comparative_asset_view()
            assert repository.get_assets().available() == 3
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 1

    def test_lookup_repository_3_comparative_isolated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[3])
            repository.use_isolated_repository_view()
            repository.use_comparative_asset_view()
            assert repository.get_assets().available() == 3
            assert repository.get_assets_by_genus_type(BLUE_TYPE).available() == 1

    def test_query_repository_0_isolated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[0])
            repository.use_isolated_repository_view()
            with pytest.raises(errors.PermissionDenied):
                query = repository.get_asset_query()

    def test_query_repository_0_federated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[0])
            repository.use_federated_repository_view()
            query = repository.get_asset_query()
            query.match_display_name('red')
            assert repository.get_assets_by_query(query).available() == 8
            query.clear_display_name_terms()
            query.match_display_name('blue')
            assert repository.get_assets_by_query(query).available() == 5

    def test_query_repository_1_isolated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[1])
            repository.use_isolated_repository_view()
            query = repository.get_asset_query()
            query.match_display_name('red')
            assert repository.get_assets_by_query(query).available() == 2

    def test_query_repository_1_federated(self):
        if not is_never_authz(self.service_config):
            janes_repository_mgr = Runtime().get_service_manager(
                'REPOSITORY',
                proxy=JANE_PROXY,
                implementation='TEST_SERVICE_JSON_AUTHZ')
            repository = janes_repository_mgr.get_repository(self.repository_id_list[1])
            repository.use_federated_repository_view()
            query = repository.get_asset_query()
            query.match_display_name('red')
            assert repository.get_assets_by_query(query).available() == 6
