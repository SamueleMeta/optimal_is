from torch import Tensor

from .abstract_td_target import AbstractTDTarget

class ReTrace(AbstractTDTarget):
    def correction(self, pi_log_p: Tensor, mu_log_p: Tensor) -> Tensor: ...
