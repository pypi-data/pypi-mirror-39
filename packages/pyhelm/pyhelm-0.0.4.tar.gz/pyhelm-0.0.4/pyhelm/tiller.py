import grpc
import yaml
import logger

from hapi.services.tiller_pb2 import ReleaseServiceStub, ListReleasesRequest, \
    InstallReleaseRequest, UpdateReleaseRequest, UninstallReleaseRequest, \
    GetReleaseStatusRequest, GetReleaseContentRequest
from hapi.chart.chart_pb2 import Chart
from hapi.chart.config_pb2 import Config

TILLER_PORT = 44134
TILLER_VERSION = b'2.11'
TILLER_TIMEOUT = 300
RELEASE_LIMIT = 64


class Tiller(object):
    '''
    The Tiller class supports communication and requests to the Tiller Helm
    service over gRPC
    '''

    _logger = logger.get_logger('Tiller')

    def __init__(self, host, port=44134, timeout=TILLER_TIMEOUT):

        # init k8s connectivity
        self._host = host
        self._port = port

        # init tiller channel
        self.channel = self.get_channel()

        # init timeout for all requests
        self.timeout = timeout

    @property
    def metadata(self):
        '''
        Return tiller metadata for requests
        '''
        return [(b'x-helm-api-client', TILLER_VERSION)]

    def get_channel(self):
        '''
        Return a tiller channel
        '''
        return grpc.insecure_channel('%s:%s' % (self._host, self._port))

    def tiller_status(self):
        '''
        return if tiller exist or not
        '''
        if self._host:
            return True

        return False

    def list_releases(self):
        '''
        List Helm Releases
        '''
        releases = []

        offset = None
        stub = ReleaseServiceStub(self.channel)

        while (offset is None or len(offset) > 0):
            req = ListReleasesRequest(limit=RELEASE_LIMIT,offset=offset)
            release_list = stub.ListReleases(req, self.timeout,
                                             metadata=self.metadata)
            for y in release_list:
                offset = str(y.next)
                releases.extend(y.releases)
        return releases

    def list_charts(self):
        '''
        List Helm Charts from Latest Releases

        Returns list of (name, version, chart, values)
        '''
        charts = []
        for latest_release in self.list_releases():
            try:
                charts.append((latest_release.name, latest_release.version,
                               latest_release.chart,
                               latest_release.config.raw))
            except IndexError:
                continue
        return charts

    def update_release(self, chart, dry_run, namespace, name=None,
                       disable_hooks=False, values=None, wait=False):
        '''
        Update a Helm Release
        '''

        values = Config(raw=yaml.safe_dump(values or {}))

        # build release install request
        stub = ReleaseServiceStub(self.channel)
        release_request = UpdateReleaseRequest(
            chart=chart,
            dry_run=dry_run,
            disable_hooks=disable_hooks,
            values=values,
            name=name or '',
            wait=wait)

        return stub.UpdateRelease(release_request, self.timeout, metadata=self.metadata)

    def install_release(self, chart, namespace, dry_run=False,
                        name=None, values=None, wait=False):
        """
        Create a Helm Release
        """

        values = Config(raw=yaml.safe_dump(values or {}))

        # build release install request
        stub = ReleaseServiceStub(self.channel)
        release_request = InstallReleaseRequest(
            chart=chart,
            dry_run=dry_run,
            values=values,
            name=name or '',
            namespace=namespace,
            wait=wait)
        return stub.InstallRelease(release_request,
                                   self.timeout,
                                   metadata=self.metadata)

    def uninstall_release(self, release, disable_hooks=False, purge=True):
        """
        :params - release - helm chart release name
        :params - purge - deep delete of chart

        deletes a helm chart from tiller
        """

        # build release install request
        stub = ReleaseServiceStub(self.channel)
        release_request = UninstallReleaseRequest(name=release,
                                                  disable_hooks=disable_hooks,
                                                  purge=purge)
        return stub.UninstallRelease(release_request,
                                     self.timeout,
                                     metadata=self.metadata)

    def get_release_status(self, release, version=None):
        stub = ReleaseServiceStub(self.channel)
        status_request = GetReleaseStatusRequest(name=release,
                                                 version=version)
        return stub.GetReleaseStatus(status_request,
                                     self.timeout,
                                     metadata=self.metadata)

    def get_release_content(self, release, version=None):
        stub = ReleaseServiceStub(self.channel)
        status_request = GetReleaseContentRequest(name=release,
                                                  version=version)
        return stub.GetReleaseContent(status_request,
                                      self.timeout,
                                      metadata=self.metadata)

    def chart_cleanup(self, prefix, charts):
        """
        :params charts - list of yaml charts
        :params known_release - list of releases in tiller

        :result - will remove any chart that is not present in yaml
        """
        def release_prefix(prefix, chart):
            """
            how to attach prefix to chart
            """
            return "{}-{}".format(prefix, chart["chart"]["release_name"])

        valid_charts = [release_prefix(prefix, chart) for chart in charts]
        actual_charts = [x.name for x in self.list_releases()]
        chart_diff = list(set(actual_charts) - set(valid_charts))

        for chart in chart_diff:
            if chart.startswith(prefix):
                self._logger.debug("Release: %s will be removed", chart)
                self.uninstall_release(chart)
