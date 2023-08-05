import warnings

import pytest
import tests.conftest as conftest

@pytest.fixture(scope="session", autouse=True)
def before_all_tests():
    global kiali_client, swagger_method_list, tested_method_list
    kiali_client = conftest.get_kiali_https_auth_client()
    swagger = kiali_client.swagger_parser.swagger

    swagger_method_list= []
    tested_method_list = ['Root','jaegerInfo', 'grafanaInfo', 'getStatus', 'getConfig', 'GetToken',
                          'namespaceList', 'namespaceMetrics','namespaceHealth','namespaceValidations',
                          'istioConfigList', 'istioConfigDetails', 'objectValidations', ''
                          'serviceList', 'serviceDetails', 'serviceMetrics', 'serviceHealth', 'serviceValidations',
                          'appHealth', 'appList', 'appDetails', 'appMetrics',
                          'workloadList', 'workloadDetails', 'workloadHealth', 'workloadMetrics',
                          'graphNamespaces', 'graphService', 'graphWorkload', 'graphApp', 'graphAppVersion', 'istioConfigAdapterTemplateDetails']

    for key in swagger.operation:
        swagger_method_list.append(key)



def get_method_from_method_list(method_name):
    try:
        return tested_method_list[tested_method_list.index(method_name)]
    except ValueError:
        pytest.fail('Method not available on Tested Method List')


def evaluate_response(method_name, path=None, params=None, status_code_expected=200):
    response = kiali_client.request(method_name=get_method_from_method_list(method_name), path=path, params=params)
    assert response is not None
    try:
        assert response.status_code == status_code_expected
    except AssertionError:
        pytest.fail(response.content)
    assert response.json() is not None


def test_swagger_coverage():
    difference_set = set(swagger_method_list) - set(tested_method_list)
    if len(difference_set) > 0:
        pytest.fail('Missing {0} Api Methods to Validate:'.format(str(len(difference_set))) + str(difference_set))
    else:
        pass

def test_root():
    evaluate_response(method_name='Root')


def test_jaeger_info():
    evaluate_response(method_name='jaegerInfo')


def test_grafana_info():
    evaluate_response(method_name='grafanaInfo')


def test_get_status():
    evaluate_response(method_name='getStatus')


def test_get_config():
    evaluate_response(method_name='getConfig')


def test_get_token():
    evaluate_response(method_name='GetToken')


def test_namespace_list():
    evaluate_response(method_name='namespaceList')

def test_namespace_metrics():
    evaluate_response(method_name='namespaceMetrics', path={'namespace': 'istio-system'})


def test_namespace_health():
    evaluate_response(method_name='namespaceHealth', path={'namespace': 'istio-system'})


def test_namespace_validations():
    evaluate_response(method_name='namespaceValidations', path={'namespace': 'istio-system'})


def test_istio_config_list():
    evaluate_response(method_name='istioConfigList', path={'namespace': 'istio-system'})


def test_istio_config_details():
    evaluate_response(method_name='istioConfigDetails', path={'namespace': 'istio-system', 'object_type': 'rules', 'object': 'promtcp'})


def test_object_validations():
    evaluate_response(method_name='objectValidations', path={'namespace': 'bookinfo', 'object_type': 'service', 'object': 'productpage'}, status_code_expected=400)
    evaluate_response(method_name='objectValidations', path={'namespace': 'istio-system', 'object_type': 'rules', 'object': 'promtcp'})


def test_istio_config_adapter_template_details():
    evaluate_response(method_name='istioConfigAdapterTemplateDetails', path={'namespace': 'istio-system', 'object_type': 'templates', 'object_subtype': 'metrics', 'object': 'tcpbytereceived'} )

def test_service_list():
    evaluate_response(method_name='serviceList', path={'namespace': 'istio-system'})


def test_service_details():
    evaluate_response(method_name='serviceDetails',
                                           path={'namespace': 'istio-system', 'service': 'kiali'})

def test_service_metrics():
    evaluate_response(method_name='serviceMetrics',
                                        path={'namespace': 'istio-system', 'service': 'kiali'})

def test_service_health():
    evaluate_response(method_name='serviceHealth', path={'namespace': 'istio-system', 'service': 'kiali'})


def test_service_validations():
    evaluate_response(method_name='serviceValidations', path={'namespace': 'istio-system', 'service': 'kiali'})


def test_app_list():
    evaluate_response(method_name='appList', path={'namespace': 'istio-system'})

def test_app_metrics():
    evaluate_response(method_name='appMetrics', path={'namespace': 'istio-system', 'app': 'kiali'})


def test_app_details():
    evaluate_response(method_name='appDetails', path={'namespace': 'istio-system', 'app': 'kiali'})

def test_app_health():
    evaluate_response(method_name='appHealth', path={'namespace': 'istio-system', 'app': 'kiali'})


def test_workload_list():
    evaluate_response(method_name='workloadList', path={'namespace': 'istio-system'})


def test_workload_details():
    evaluate_response(method_name='workloadDetails', path={'namespace': 'bookinfo', 'workload':'details-v1'})

def test_workload_health():
    evaluate_response(method_name='workloadHealth', path={'namespace': 'bookinfo', 'workload':'details-v1'})

def test_workload_metrics():
    evaluate_response(method_name='workloadMetrics', path={'namespace': 'bookinfo', 'workload':'details-v1'})

def test_graph_namespaces():
    VERSIONED_APP_PARAMS = {'namespace': 'bookinfo', 'graphType': 'versionedApp', 'duration': '60s'}
    WORKLOAD_PARAMS = {'namespace': 'bookinfo', 'graphType': 'workload', 'duration': '60s'}
    APP_PARAMS = {'namespace': 'bookinfo','graphType': 'app', 'duration': '60s'}

    evaluate_response(method_name='graphNamespaces', params=VERSIONED_APP_PARAMS)
    evaluate_response(method_name='graphNamespaces', params=WORKLOAD_PARAMS)
    evaluate_response(method_name='graphNamespaces', params=APP_PARAMS)


def test_graph_service():
    GRAPH_SERVICE_PATH = {'namespace': 'bookinfo', 'service': 'mongodb'}
    evaluate_response(method_name='graphService', path=GRAPH_SERVICE_PATH)


def test_graph_workload():
    GRAPH_WORKLOAD_PATH = {'namespace': 'bookinfo', 'workload': 'mongodb-v1'}
    evaluate_response(method_name='graphWorkload', path=GRAPH_WORKLOAD_PATH)

def test_graph_app_and_graph_app_version():
    GRAPH_APP_PARAMS_NOT_VALID = {'graphType': 'notValid'}
    GRAPH_APP_PARAMS_APP = {'graphType': 'app'}
    GRAPH_APP_PARAMS_VERSION = {'graphType': 'versionedApp'}
    GRAPH_APP_PARAMS_WORKLOAD = {'graphType': 'workload'}
    GRAPH_APP_PARAMS_SERVICE = {'graphType': 'service'}
    
    
    GRAPH_APP_PATH = {'namespace': 'bookinfo', 'app': 'reviews'}

    for method_name in ['graphApp', 'graphAppVersion']:

        # Default Request (It is expected because the graphType is set to Workload as default it will fail for default case)
        evaluate_response(method_name=method_name, path=GRAPH_APP_PATH, status_code_expected=500)

        # Workload (also equals to Default)
        evaluate_response(method_name=method_name, path=GRAPH_APP_PATH, status_code_expected=500,
                        params=GRAPH_APP_PARAMS_WORKLOAD)

        # Service
        evaluate_response(method_name=method_name, path=GRAPH_APP_PATH, status_code_expected=500,
                        params=GRAPH_APP_PARAMS_SERVICE)

        # Invalid Value
        evaluate_response(method_name=method_name, path=GRAPH_APP_PATH,
                        params=GRAPH_APP_PARAMS_NOT_VALID, status_code_expected=500)

        # App Graph
        evaluate_response(method_name=method_name, path=GRAPH_APP_PATH, status_code_expected=200,
                        params=GRAPH_APP_PARAMS_APP)

        # Versioned App Graph
        evaluate_response(method_name=method_name, path=GRAPH_APP_PATH, status_code_expected=200,
                        params=GRAPH_APP_PARAMS_VERSION)