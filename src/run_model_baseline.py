# this program runs the optimizer model, and ensures that all the results are
# reasonable using a couple useful checks to make sure there's nothing wacky
# going on:

# 1) check that as time increases, more people can be fed

# 2) check that stored food plus meat is always used at the
# highest rate during the largest food shortage.

import os
import sys
import numpy as np
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from src.optimizer import Optimizer
from src.plotter import Plotter
from src.constants import Constants

constants_loader = Constants()
optimizer = Optimizer()

constants = {}
constants['CHECK_CONSTRAINTS'] = False

inputs_to_optimizer = constants_loader.init_global_food_system_properties()
constants = constants_loader.get_baseline_scenario(inputs_to_optimizer)
constants = constants_loader.set_baseline_nutrition_profile(inputs_to_optimizer)
constants = constants_loader.set_stored_food_usage_as_may_till_minimum(inputs_to_optimizer)
inputs_to_optimizer = constants_loader.set_global_seasonality_baseline(inputs_to_optimizer)
inputs_to_optimizer = constants_loader.set_fish_baseline(inputs_to_optimizer)

inputs_to_optimizer = constants_loader.set_waste_to_zero(inputs_to_optimizer)

inputs_to_optimizer = constants_loader.set_immediate_shutoff(inputs_to_optimizer)

inputs_to_optimizer = constants_loader.set_global_disruption_to_crops_to_zero(inputs_to_optimizer)


# No excess calories
inputs_to_optimizer["EXCESS_CALORIES"] = \
    np.array([0] * inputs_to_optimizer['NMONTHS'])

constants['inputs'] = inputs_to_optimizer
single_valued_constants, multi_valued_constants = \
    constants_loader.computeConstants(constants)

single_valued_constants["CHECK_CONSTRAINTS"] = False
[time_months, time_months_middle, analysis] = \
    optimizer.optimize(single_valued_constants, multi_valued_constants)

print("")
print("Maximum usable kcals/capita/day 2020, no waste, primary production")
print(analysis.people_fed_billions/7.8*2100)
print("")

analysis1 = analysis

inputs_to_optimizer = constants_loader.set_continued_feed_biofuels(inputs_to_optimizer)

inputs_to_optimizer = \
    constants_loader.set_waste_to_baseline_prices(inputs_to_optimizer)

# No excess calories -- excess calories is set when the model is run and needs to be reset each time.
inputs_to_optimizer["EXCESS_CALORIES"] = \
    np.array([0] * inputs_to_optimizer['NMONTHS'])


optimizer = Optimizer()
constants['inputs'] = inputs_to_optimizer
single_valued_constants, multi_valued_constants = \
    constants_loader.computeConstants(constants)
single_valued_constants['CHECK_CONSTRAINTS'] = False
[time_months, time_months_middle, analysis] = optimizer.optimize(single_valued_constants, multi_valued_constants)

analysis2 = analysis

Plotter.plot_fig_s1abcd(analysis1, analysis2, 72)