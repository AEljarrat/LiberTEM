import scipy.sparse as sp
from libertem.viz import visualize_simple
from .base import AnalysisResult, AnalysisResultSet
from .masks import BaseMasksAnalysis


class PointMaskAnalysis(BaseMasksAnalysis):
    def get_results(self, job_results):
        data = job_results[0]
        return AnalysisResultSet([
            AnalysisResult(raw_data=data, visualized=visualize_simple(data),
                           key="intensity", title="intensity",
                           desc="intensity of the integration over the selected point"),
        ])

    def get_use_sparse(self):
        return True

    def get_mask_factories(self):
        (detector_y, detector_x) = self.dataset.shape[2:]

        cx = self.parameters.get('x', detector_x / 2)
        cy = self.parameters.get('y', detector_y / 2)

        def _point_inner():
            a = sp.csr_matrix(([1], ([int(cy)], [int(cx)])),
                    dtype=self.dtype, shape=self.dataset.shape[2:])
            return a
        return [_point_inner]
