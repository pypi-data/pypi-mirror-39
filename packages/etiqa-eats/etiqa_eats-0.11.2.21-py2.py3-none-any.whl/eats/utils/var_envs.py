class VarEnvs(object):

    def __getitem__(self, key):
        return getattr(self, key)

    def keys(self):
        return [k for k, v in vars(type(self)).items() if type(v) is property]


def replace_scenario_variables_in_steps(scenario, variables):
    variables = dict((k, variables[k]) for k in variables.keys())
    for step in scenario.all_steps:
        tmp_step = step.set_values(variables)
        step.name = tmp_step.name
        step.text = tmp_step.text
        step.table = tmp_step.table
