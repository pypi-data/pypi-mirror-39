from oc_wrapper.policy import Policy


class Oc(object):
    ci_mode = True

    def __init__(self):
        super(Oc, self).__init__()
        self.policy = Policy(self.ci_mode)
