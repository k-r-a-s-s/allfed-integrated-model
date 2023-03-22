"""
This is a function used to quickly estimate the feed usage and resulting meat when
breeding is changed and slaughter is increased somewhat (or whatever reasonable result
is to be expected in the scenario in question).


"""

import pathlib
import pandas as pd
import numpy as np

"""
Start main function
"""
# Create dataframes

class CalculateAnimalOutputs:
    def __init__(self):
        self.animal_inputs = ModelAnimalInputs(df_animals)
        self.slaughter_inputs = ModelAnimalInputs(df_fao_slaughter)
        self.population_inputs = ModelAnimalInputs(df_fao_animals)
        self.feed_inputs = ModelAnimalInputs(df_feed_country)

    def calculate_country_specifc_per_species_feed_consumption(self,country_code): 
        """
        This function is used to calculate the total feed usage for a country
        """

        # Per country stuff from FAO (head)
        small_animals = df_fao_animals.at[country_code, "small_animals"]
        medium_animals = df_fao_animals.at[country_code, "medium_animals"]
        large_animals = df_fao_animals.at[country_code, "large_animals"]
        dairy_cows = df_fao_animals.at[country_code, "dairy_cows"]

        # Per country stuff from mike's data (million tonnes)
        country_feed_caloric_annual = df_feed_country.at[
            country_code, "Animal feed caloric consumption in 2020 (million dry caloric tons)"
        ]
        country_feed_fat_annual = df_feed_country.at[
            country_code, "Animal feed fat consumption in 2020 (million tonnes)"
        ]
        country_feed_protein_annual = df_feed_country.at[
            country_code, "Animal feed protein consumption in 2020 (million tonnes)"
        ]
        country_total_feed_tonnes_annual = (
            country_feed_caloric_annual + country_feed_fat_annual + country_feed_protein_annual
        )

        # Fractional values of feed type, 
        fractional_caloric = country_feed_caloric_annual / country_total_feed_tonnes_annual
        fractional_fat = country_feed_fat_annual / country_total_feed_tonnes_annual
        fractional_protein = country_feed_protein_annual / country_total_feed_tonnes_annual

        # Monthly values, not all are used, can remove the calroic, protein, and fat.
        # instead of these monthly values, the function uses the fractional values above to calculate the country_specific_feed_per_animal_head_pm
        country_feed_caloric_monthly = country_feed_caloric_annual / 12
        country_feed_fat_monthly = country_feed_fat_annual / 12
        country_feed_protein_monthly = country_feed_protein_annual / 12
        country_total_feed_tonnes_monthly = country_total_feed_tonnes_annual / 12


        # Feed per animal per month calculated from bottom up assortment of papers in roam
        # this is not the actual feed used, rather the feed requirements (and the requirements could be met from other means such as foraging/grazing non-feed food sources)
        # Could also use LSUs from FAO, per country basis. Infact, we probably should.
        small_animals_feed_pm_per_animal = 1.824
        medium_animal_feed_pm_per_animal = 68.4
        large_animal_feed_pm_per_animal = 296.4
        dairy_feed_pm_per_cow = 475

        # ratio of how much more do animals eat compared to a small animal
        small_ratio = 1
        medium_ratio = medium_animal_feed_pm_per_animal / small_animals_feed_pm_per_animal
        large_ratio = large_animal_feed_pm_per_animal / small_animals_feed_pm_per_animal
        dairy_ratio = dairy_feed_pm_per_cow / small_animals_feed_pm_per_animal

        # weighted feed per animal per month (bottom up)
        weighted_small_animal_feed = small_animals_feed_pm_per_animal * small_animals
        weighted_medium_animal_feed = medium_animal_feed_pm_per_animal * medium_animals
        weighted_large_animal_feed = large_animal_feed_pm_per_animal * large_animals
        weighted_dairy_feed = dairy_feed_pm_per_cow * dairy_cows
        weighted_total_feed = (
            weighted_small_animal_feed
            + weighted_medium_animal_feed
            + weighted_large_animal_feed
            + weighted_dairy_feed
        )

        # species feed as a fraction of total feed per animal. Sum of these should be 1
        fractional_small_animal_feed = weighted_small_animal_feed / weighted_total_feed
        fractional_medium_animal_feed = weighted_medium_animal_feed / weighted_total_feed
        fractional_large_animal_feed = weighted_large_animal_feed / weighted_total_feed
        fractional_dairy_feed = weighted_dairy_feed / weighted_total_feed

        # feed per species per month country specific (not a per animal basis, it's a per species basis)
        monthly_feed_consumption_small_animals = (
            country_total_feed_tonnes_monthly * fractional_small_animal_feed
        )
        monthly_feed_consumption_medium_animals = (
            country_total_feed_tonnes_monthly * fractional_medium_animal_feed
        )
        monthly_feed_consumption_large_animals = (
            country_total_feed_tonnes_monthly * fractional_large_animal_feed
        )
        monthly_feed_consumption_dairy_cows = (
            country_total_feed_tonnes_monthly * fractional_dairy_feed
        )

        # feed per *animal* per month country specific. This is technically the same value as the feed per animal per month calculated from the bottom up,
        # but it instead uses those ratios to calaculate the feed, and then uses the country-specific animal feed usage to estimate the actual feed used.
        # this is a combination of the bottom up and top down approach
        country_specific_feed_per_small_animal_head_pm = (
            monthly_feed_consumption_small_animals / small_animals
        )
        country_specific_feed_per_medium_animal_head_pm = (
            monthly_feed_consumption_medium_animals / medium_animals
        )
        country_specific_feed_per_large_animal_head_pm = (
            monthly_feed_consumption_large_animals / large_animals
        )
        country_specific_feed_per_dairy_cow_head_pm = (
            monthly_feed_consumption_dairy_cows / dairy_cows
        )

        # create dict from the above, also use the fractional values to calculate the caloric, fat, and protein values
        country_specific_feed_per_animal_head_pm = {
            "small_animals": country_specific_feed_per_small_animal_head_pm,
            "medium_animals": country_specific_feed_per_medium_animal_head_pm,
            "large_animals": country_specific_feed_per_large_animal_head_pm,
            "dairy_cows": country_specific_feed_per_dairy_cow_head_pm,
            "small_animals_caloric": fractional_caloric * country_specific_feed_per_small_animal_head_pm,
            "small_animals_fat": fractional_fat * country_specific_feed_per_small_animal_head_pm,
            "small_animals_protein": fractional_protein * country_specific_feed_per_small_animal_head_pm,
            "medium_animals_caloric": fractional_caloric * country_specific_feed_per_medium_animal_head_pm,
            "medium_animals_fat": fractional_fat * country_specific_feed_per_medium_animal_head_pm,
            "medium_animals_protein": fractional_protein * country_specific_feed_per_medium_animal_head_pm,
            "large_animals_caloric": fractional_caloric * country_specific_feed_per_large_animal_head_pm,
            "large_animals_fat": fractional_fat * country_specific_feed_per_large_animal_head_pm,
            "large_animals_protein": fractional_protein * country_specific_feed_per_large_animal_head_pm,
            "dairy_cows_caloric": fractional_caloric * country_specific_feed_per_dairy_cow_head_pm,
            "dairy_cows_fat": fractional_fat * country_specific_feed_per_dairy_cow_head_pm,
            "dairy_cows_protein": fractional_protein * country_specific_feed_per_dairy_cow_head_pm,
        }

        return country_specific_feed_per_animal_head_pm

    def calculate_feed_and_animals(
        self,
        data
    ):        
        """
        This function calculates the feed and animal populations for a given country

        Parameters
        ----------
        data : dict
            Dictionary containing the country code and the animal populations

        Returns
        -------
        df_out : pandas.DataFrame
            Dataframe containing the animal populations and the feed used for each species

        """
        # Here are the two functions that are called
        # The first one calculates the feed per animal per month for each species
        # The second one calculates the animal populations
        feed_dict = self.calculate_country_specifc_per_species_feed_consumption(data["country_code"])
        df_out = self.calculate_animal_populations(data)

        # now combine the two in and calculate feed usage along different dimensions
        df_out["small_animal_total_feed"] = df_out["Poultry Pop"] * feed_dict["small_animals"]
        df_out["medium_animal_total_feed"] = df_out["Pigs Pop"] * feed_dict["medium_animals"]
        df_out["large_animal_total_feed"] = df_out["Beef Pop"] * feed_dict["large_animals"]
        df_out["dairy_cow_total_feed"] = df_out["Dairy Pop"] * feed_dict["dairy_cows"]
        df_out["small_animals_caloric"] = df_out["Poultry Pop"] * feed_dict["small_animals_caloric"]
        df_out["small_animals_fat"] = df_out["Poultry Pop"] * feed_dict["small_animals_fat"]
        df_out["small_animals_protein"] = df_out["Poultry Pop"] * feed_dict["small_animals_protein"]
        df_out["medium_animals_caloric"] = df_out["Pigs Pop"] * feed_dict["medium_animals_caloric"]
        df_out["medium_animals_fat"] = df_out["Pigs Pop"] * feed_dict["medium_animals_fat"]
        df_out["medium_animals_protein"] = df_out["Pigs Pop"] * feed_dict["medium_animals_protein"]
        df_out["large_animals_caloric"] = df_out["Beef Pop"] * feed_dict["large_animals_caloric"]
        df_out["large_animals_fat"] = df_out["Beef Pop"] * feed_dict["large_animals_fat"]
        df_out["large_animals_protein"] = df_out["Beef Pop"] * feed_dict["large_animals_protein"]
        df_out["dairy_cows_caloric"] = df_out["Dairy Pop"] * feed_dict["dairy_cows_caloric"]
        df_out["dairy_cows_fat"] = df_out["Dairy Pop"] * feed_dict["dairy_cows_fat"]
        df_out["dairy_cows_protein"] = df_out["Dairy Pop"] * feed_dict["dairy_cows_protein"]
        # totals
        df_out["total_feed"] = (
            df_out["small_animal_total_feed"]
            + df_out["medium_animal_total_feed"]
            + df_out["large_animal_total_feed"]
            + df_out["dairy_cow_total_feed"]
        )
        df_out["total_caloric"] = (
            df_out["small_animals_caloric"]
            + df_out["medium_animals_caloric"]
            + df_out["large_animals_caloric"]
            + df_out["dairy_cows_caloric"]
        )
        df_out["total_fat"] = (
            df_out["small_animals_fat"]
            + df_out["medium_animals_fat"]
            + df_out["large_animals_fat"]
            + df_out["dairy_cows_fat"]
        )
        df_out["total_protein"] = (
            df_out["small_animals_protein"]
            + df_out["medium_animals_protein"]
            + df_out["large_animals_protein"]
            + df_out["dairy_cows_protein"]
        )


        return df_out

    def calculate_animal_populations(
        self,
        data
    ):
        """

        Parameters
        ----------
        data : dict
            Dictionary containing the country code and the animal populations

        Returns
        -------
        df_out : pandas.DataFrame
            Dataframe containing the animal populations Slaughter numbers

        Inputs with "data":

        country_code: Country Code
        reduction_in_beef_calves: Reduction in Beef Birth Rate
        reduction_in_dairy_calves: Reduction in Dairy Birth Rate

        increase_in_slaughter: So 20% indicates an 80% drop in baseline sluaghter rates
        in slaughterhouses

        reduction_in_pig_breeding: Reduction Pig Breeding
        100(=100% reduction) means that all insemination and breeding stops on day 0 (
        with the corresponding drop in birth rate happening 9 months later for cows, 1
         month for chickens, 4 months pigs (as per gestation variables))
        reduction_in_poultry_breeding: Reduction Poultry Breeding

        months: Months to simulate
        discount_rate: discount_rate: Discount Rate for Labour/Technology Transfer
        between species

        mother_slaughter: Proportion of Slaughter which is mothers
        (In a normal slaughtering regime pregnant animals are not killed.
        mother_slaughter is a percentage of how much of the slaughtering capacity
        will be used on pregnant animals.)

        use_grass_and_residues_for_dairy: Whether to Use Residues for Dairy
        """

        #unpack input dict
        country_code, reduction_in_beef_calves, reduction_in_dairy_calves, increase_in_slaughter, reduction_in_pig_breeding, reduction_in_poultry_breeding, months, discount_rate, mother_slaughter, use_grass_and_residues_for_dairy, keep_dairy = data.values()

        steady_state_births = 1

        other_cow_death_rate_annual = (
            self.animal_inputs.dataframe.at["Other cow death", "Qty"] / 100
        )
        other_pig_death_rate_annual = (
            self.animal_inputs.dataframe.at["Other pig death", "Qty"] / 100
        )
        other_poultry_death_rate_annual = (
            self.animal_inputs.dataframe.at["Other poultry death", "Qty"] / 100
        )

        other_poultry_death_rate_monthly = other_poultry_death_rate_annual / 12
        other_pig_death_rate_monthly = other_pig_death_rate_annual / 12
        other_cow_death_rate_monthly = other_cow_death_rate_annual / 12

        # unpack all the dataframe information for ease of use
        # pigs
        total_pigs = self.population_inputs.dataframe.at[country_code, "medium_animals"]
        pigs_slaughter_pm = self.slaughter_inputs.dataframe.at[country_code, "medium_animal_slaughter"]/12
        pigGestation = self.animal_inputs.dataframe.at["pigGestation", "Qty"]
        piglets_per_litter = self.animal_inputs.dataframe.at["PigsPerLitter", "Qty"]

        # poultry
        total_poultry = self.population_inputs.dataframe.at[
            country_code, "small_animals"
        ]
        poultry_slaughter_pm = self.slaughter_inputs.dataframe.at[
            country_code, "small_animal_slaughter"
        ]/12
        poultryGestation = self.animal_inputs.dataframe.at["Chicken Gestation", "Qty"]
        # USDA  # actaully 21 days, let's round to 1 month

        # cows (more complex, as need to split dairy and beef)
        total_dairy_cows = self.population_inputs.dataframe.at[
            country_code, "dairy_cows"
        ]
        total_beef_cows = self.population_inputs.dataframe.at[
            country_code, "large_animals"
        ]
        cow_slaughter_pm = self.slaughter_inputs.dataframe.at[country_code, "large_animal_slaughter"]/12
        cowGestation = self.animal_inputs.dataframe.loc["cowGestation", "Qty"]
        calves_per_mother = 1

        # life expetency values
        dairy_life_expectancy = (
            5.87  # https://www.frontiersin.org/articles/10.3389/fvets.2021.646672/full
        )
        dairy_start_milking_age = 2
        dairy_track_milk_ready_percent = (
            dairy_life_expectancy - dairy_start_milking_age
        ) / dairy_life_expectancy
        dairy_cows_end_of_life_annual = (
            total_dairy_cows / dairy_life_expectancy
            + total_dairy_cows * other_cow_death_rate_annual
        )  # first terms are thoise being slaughtered once milking is done, then combine this with other death

        # calculate expected death rates, day 0 (normal conditions)
        poultry_total_death_pm = (
            poultry_slaughter_pm + total_poultry * other_poultry_death_rate_monthly
        )
        pig_total_death_pm = (
            pigs_slaughter_pm + total_pigs * other_pig_death_rate_monthly
        )  # assume replacement rate
        dairy_total_death_pm = dairy_cows_end_of_life_annual / 12
        beef_total_death_pm = (
            cow_slaughter_pm
            + total_beef_cows * other_cow_death_rate_monthly
            - dairy_total_death_pm
        )

        # assume steady state popualtion, define birth rates from death rates
        new_pigs_pm = pig_total_death_pm
        new_poultry_pm = poultry_total_death_pm
        new_dairy_calves_pm = dairy_total_death_pm
        new_beef_calves_pm = beef_total_death_pm

        # interventions, scale appropriately for maths (i.e convert sliders from % to
        # decimal)
        reduction_in_beef_calves *= 0.01
        reduction_in_dairy_calves *= 0.01
        reduction_in_pig_breeding *= 0.01
        reduction_in_poultry_breeding *= 0.01
        increase_in_slaughter *= 0.01

        # pregnant animals
        current_pregnant_sows = new_pigs_pm / piglets_per_litter
        current_pregnant_cows = new_beef_calves_pm / calves_per_mother
        sow_slaughter_percent = (
            mother_slaughter / 100
        )  # of total percent of pig slaughter
        mother_cow_slaughter_percent = (
            mother_slaughter / 100  # of total percent of cow slaughter
        )

        # ### Slaughtering ####
        # ## Slaughtering variables (currently hardcoded !!)
        # total slaughter capacity
        cow_slaughter_hours = (
            4  # resources/hours of single person hours for slaughter of cow
        )
        pig_slaughter_hours = (
            4  # resources/hours of single person hours for slaughter of pig
        )
        poultry_slaughter_hours = (
            0.08  # resources/hours of single person hours for slaughter of poultry
        )
        total_slaughter_cap_hours = (
            cow_slaughter_pm * cow_slaughter_hours
            + pigs_slaughter_pm * pig_slaughter_hours
            + poultry_slaughter_pm * poultry_slaughter_hours
        )
        skill_transfer_discount_chickens_to_pigs = (100 - discount_rate) / 100  #
        skill_transfer_discount_pigs_to_cows = (100 - discount_rate) / 100  #

        # # Slaughtering Updates, increases from slider
        total_slaughter_cap_hours *= increase_in_slaughter  # measured in hours
        current_cow_slaughter = (
            cow_slaughter_pm * increase_in_slaughter
        )  # measured in head
        current_poultry_slaughter = (
            poultry_slaughter_pm * increase_in_slaughter
        )  # measured in head
        current_pig_slaughter = (
            pigs_slaughter_pm * increase_in_slaughter
        )  # measured in head
        spare_slaughter_hours = 0

        # # define current totals
        # current_beef_feed_cattle = cattle_on_feed
        current_beef_cattle = total_beef_cows
        current_dairy_cattle = total_dairy_cows
        current_total_pigs = total_pigs
        current_total_poultry = total_poultry

        d = []  # create empty list to place variables in to in loop

        # simulate x months
        for i in range(months):

            if steady_state_births == 1:

                new_pigs_pm = current_pregnant_sows * piglets_per_litter
                new_beef_calves_pm = current_pregnant_cows * calves_per_mother

            # determine birth rates
            if np.abs(i - cowGestation) <= 0.5:
                new_beef_calves_pm *= 1 - reduction_in_beef_calves
                new_dairy_calves_pm *= 1 - reduction_in_dairy_calves
                current_pregnant_cows *= 1 - reduction_in_beef_calves

            if np.abs(i - pigGestation) <= 0.5:
                new_pigs_pm *= 1 - reduction_in_pig_breeding
                current_pregnant_sows *= 1 - reduction_in_pig_breeding

            if np.abs(i - poultryGestation) <= 0.5:
                new_poultry_pm *= 1 - reduction_in_poultry_breeding

            if new_pigs_pm < 0:
                new_pigs_pm = 0

            if new_beef_calves_pm < 0:
                new_beef_calves_pm = 0

            # Transfer excess slaughter capacity to next animal, current coding method
            # only allows poultry -> pig -> cow, there are some small erros here due to
            # rounding, and the method is not 100% water tight but errors are within the
            # noise

            #### This is where the issue was!
            # added the new_poultry_pm and new_pigs_pm to the current totals. These were left out and meant that the populations would grow but the slaughter
            if current_total_poultry < current_poultry_slaughter:
                spare_slaughter_hours = (
                    current_poultry_slaughter - current_total_poultry - new_poultry_pm
                ) * poultry_slaughter_hours
                current_poultry_slaughter = current_total_poultry + new_poultry_pm
                current_pig_slaughter += (
                    spare_slaughter_hours
                    * skill_transfer_discount_chickens_to_pigs
                    / pig_slaughter_hours
                )
            if current_total_pigs < current_pig_slaughter:
                spare_slaughter_hours = (
                    current_pig_slaughter - current_total_pigs - new_pigs_pm
                ) * pig_slaughter_hours
                current_pig_slaughter = current_total_pigs + new_pigs_pm
                current_cow_slaughter += (
                    spare_slaughter_hours
                    * skill_transfer_discount_pigs_to_cows
                    / cow_slaughter_hours
                )

            # this set up only kills dairy cows when they are getting to the end of
            # their life.
            current_dairy_slaughter = current_dairy_cattle / (
                dairy_life_expectancy
            ) /12
            current_beef_slaughter = current_cow_slaughter - current_dairy_slaughter
            if current_beef_cattle < current_beef_slaughter:
                # line below required due to the difference between actual slaughter
                # and 'slaughter capacity' consider a rewrite of the whole method to
                # distinuguish between these two. For now, this is thr workaround.
                actual_beef_slaughter = current_beef_cattle

                if keep_dairy == 0:
                    current_dairy_slaughter = (
                        current_cow_slaughter - actual_beef_slaughter
                    )

            else:
                actual_beef_slaughter = current_beef_slaughter

            other_beef_death = other_cow_death_rate_monthly * current_beef_cattle
            other_dairy_death = other_cow_death_rate_monthly * current_dairy_cattle
            other_pig_death = current_total_pigs * other_pig_death_rate_monthly
            other_poultry_death = (
                current_total_poultry * other_poultry_death_rate_monthly
            )

            # ## Generate list (before new totals have been calculated)
            # magnitude adjust moves the numbers from per thousnad head to per head (or
            # other)
            # feed adjust turns lbs in to tons
            d.append(
                {
                    "Beef Pop": current_beef_cattle,
                    "Beef Born": new_beef_calves_pm,
                    "Beef Slaughtered": actual_beef_slaughter,
                    "Beef Slaughtered Hours": actual_beef_slaughter
                    * cow_slaughter_hours,
                    "Beef Slaughtered Hours %": actual_beef_slaughter
                    * cow_slaughter_hours
                    / total_slaughter_cap_hours,
                    "Beef Other Death": other_beef_death,
                    "Dairy Pop": current_dairy_cattle,
                    "Dairy Cow Pop": current_dairy_cattle,
                    "Dairy Milk Ready Pop": current_dairy_cattle
                    * dairy_track_milk_ready_percent,
                    "Dairy Born": new_dairy_calves_pm,
                    "Dairy Slaughtered": current_dairy_slaughter,
                    "Dairy Slaughtered Hours": current_dairy_slaughter
                    * cow_slaughter_hours,
                    "Dairy Slaughtered Hours %": current_dairy_slaughter
                    * cow_slaughter_hours
                    / total_slaughter_cap_hours,
                    "Dairy Other Death": other_dairy_death,
                    "Pigs Pop": current_total_pigs,
                    "Pig Born": new_pigs_pm,
                    "Pig Slaughtered": current_pig_slaughter,
                    "Pig Slaughtered Hours": current_pig_slaughter
                    * pig_slaughter_hours,
                    "Pig Slaughtered Hours %": current_pig_slaughter
                    * pig_slaughter_hours
                    / total_slaughter_cap_hours,
                    "Poultry Pop": current_total_poultry,
                    "Poultry Born": new_poultry_pm,
                    "Poultry Slaughtered": current_poultry_slaughter,
                    "Poultry Slaughtered Hours": current_poultry_slaughter
                    * poultry_slaughter_hours,
                    "Poultry Slaughtered Hours %": current_poultry_slaughter
                    * poultry_slaughter_hours
                    / total_slaughter_cap_hours,
                    "Month": i,
                }
            )

            # some up new totals
            current_beef_cattle += (
                new_beef_calves_pm - current_beef_slaughter - other_beef_death
            )
            current_dairy_cattle += (
                new_dairy_calves_pm - current_dairy_slaughter - other_dairy_death
            )
            current_total_poultry += (
                new_poultry_pm - current_poultry_slaughter - other_poultry_death
            )
            current_total_pigs += new_pigs_pm - current_pig_slaughter - other_pig_death

            current_pregnant_sows -= sow_slaughter_percent * (
                current_pig_slaughter + other_pig_death
            )
            current_pregnant_cows -= mother_cow_slaughter_percent * (
                current_beef_slaughter + other_beef_death
            )

            # values might be very slightly negative due to overshoot, so set to zero
            if current_beef_cattle < 0:
                current_beef_cattle = 0
            if current_dairy_cattle < 0:
                current_dairy_cattle = 0
            if current_total_poultry < 0:
                current_total_poultry = 0
            if current_total_pigs < 0:
                current_total_pigs = 0

        # ## End of loop, start summary

        df_final = pd.DataFrame(d)

        return df_final

class ModelAnimalInputs:
    def __init__(self, dataframe):
        self.dataframe = dataframe


"""
Start main script
"""
# Import CSV to dataframes
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath(".").resolve()

df_animals = pd.read_csv(
    DATA_PATH.joinpath("InputDataAndSources.csv"), index_col="Variable"
)
df_feed_country = pd.read_csv(
    DATA_PATH.joinpath("country_feed_data.csv"), index_col="ISO3 Country Code"
)
df_fao_animals = pd.read_csv(DATA_PATH.joinpath("head_count_csv.csv"), index_col="iso3")
df_fao_slaughter = pd.read_csv(DATA_PATH.joinpath("FAO_stat_slaughter_counts_processed.csv"), index_col="iso3")

# ## Create class instance
ao = CalculateAnimalOutputs()

