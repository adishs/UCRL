import numpy as np
from .Ucrl import UcrlMdp
from .logging import default_logger
from .evi import SpanConstrainedEVI


class SCAL(UcrlMdp):
    """
    UCRL with bias span constraint.
    """

    def __init__(self, environment, r_max, span_constraint, alpha_r=None, alpha_p=None,
                 bound_type_p="chernoff", bound_type_rew="chernoff",
                 verbose=0, augment_reward=True, operator_type="T",
                 logger=default_logger, random_state=None, relative_vi=True):
        solver = SpanConstrainedEVI(nb_states=environment.nb_states,
                                    actions_per_state=environment.state_actions,
                                    bound_type=bound_type_p,
                                    random_state=random_state,
                                    augmented_reward=1 if augment_reward else 0,
                                    gamma=1.,
                                    span_constraint=span_constraint,
                                    relative_vi=1 if relative_vi else 0,
                                    operator_type=operator_type)
        super(SCAL, self).__init__(
            environment=environment, r_max=r_max,
            alpha_r=alpha_r, alpha_p=alpha_p, solver=solver,
            bound_type_p=bound_type_p,
            bound_type_rew=bound_type_rew,
            verbose=verbose, logger=logger, random_state=random_state)

        # we need to change policy structure since it is stochastic
        self.policy = np.zeros((self.environment.nb_states, 2), dtype=np.float)
        self.policy_indices = np.zeros((self.environment.nb_states, 2), dtype=np.int)

    @property
    def span_constraint(self):
        return self.opt_solver.get_span_constraint()

    def description(self):
        super_desc = super().description()
        desc = {
            "span_constraint": self.span_constraint,
            "operator_type": self.opt_solver.get_operator_type(),
            "relative_vi": self.opt_solver.use_relative_vi()
        }
        super_desc.update(desc)
        return super_desc
