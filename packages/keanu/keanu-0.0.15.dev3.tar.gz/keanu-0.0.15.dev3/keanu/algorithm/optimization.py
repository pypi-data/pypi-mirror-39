from py4j.java_gateway import java_import
from keanu.context import KeanuContext
from keanu.net import BayesNet
from keanu.vertex.base import Vertex
from typing import Union, Any, Optional

k = KeanuContext()

java_import(k.jvm_view(), "io.improbable.keanu.algorithms.variational.optimizer.gradient.GradientOptimizer")
java_import(k.jvm_view(), "io.improbable.keanu.algorithms.variational.optimizer.nongradient.NonGradientOptimizer")


class Optimizer:

    def __init__(self, optimizer: Any, net: Union[BayesNet, Vertex]) -> None:
        self.optimizer = optimizer
        self.net = net

    def max_a_posteriori(self) -> float:
        return self.optimizer.maxAPosteriori()

    def max_likelihood(self) -> float:
        return self.optimizer.maxLikelihood()

    @staticmethod
    def _build_bayes_net(builder: Any, net: Union[BayesNet, Vertex]) -> Any:

        if not (isinstance(net, BayesNet) or isinstance(net, Vertex)):
            raise TypeError("net must be a Vertex or a BayesNet. Was given {}".format(type(net)))
        elif isinstance(net, Vertex):
            net = BayesNet(net.get_connected_graph())
        return builder.bayesianNetwork(net.unwrap()), net


class GradientOptimizer(Optimizer):

    def __init__(self,
                 net: Union[BayesNet, Vertex],
                 max_evaluations: Optional[int] = None,
                 relative_threshold: Optional[float] = None,
                 absolute_threshold: Optional[float] = None) -> None:
        builder = k.jvm_view().GradientOptimizer.builder()
        builder, net = Optimizer._build_bayes_net(builder, net)
        if max_evaluations is not None:
            builder.maxEvaluations(max_evaluations)
        if relative_threshold is not None:
            builder.relativeThreshold(relative_threshold)
        if absolute_threshold is not None:
            builder.absoluteThreshold(absolute_threshold)

        super(GradientOptimizer, self).__init__(builder.build(), net)


class NonGradientOptimizer(Optimizer):

    def __init__(self,
                 net: Union[BayesNet, Vertex],
                 max_evaluations: Optional[int] = None,
                 bounds_range: Optional[float] = None,
                 initial_trust_region_radius: Optional[float] = None,
                 stopping_trust_region_radius: Optional[float] = None) -> None:
        builder = k.jvm_view().NonGradientOptimizer.builder()
        builder, net = Optimizer._build_bayes_net(builder, net)
        if max_evaluations is not None:
            builder.maxEvaluations(max_evaluations)
        if bounds_range is not None:
            builder.boundsRange(bounds_range)
        if initial_trust_region_radius is not None:
            builder.initialTrustRegionRadius(initial_trust_region_radius)
        if stopping_trust_region_radius is not None:
            builder.stoppingTrustRegionRadius(stopping_trust_region_radius)

        super(NonGradientOptimizer, self).__init__(builder.build(), net)
