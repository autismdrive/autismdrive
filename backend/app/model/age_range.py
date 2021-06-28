# This class gives us a single location to define th order
# of age ranges, and provides utilities for converting some
# of the bad data from CSV files around Ages into something consistent.


class AgeRange:
    ages = ['pre-k',
            'school',
            'transition',
            'adult',
            'aging']

    age_map = {
         'pre-k (0 - 5 years)': ['pre-k'],
         'school age (6 - 13 years)': ['school'],
         'transition age(14 - 22 years)': ['transition'],
         'transition age (14 - 22 years)': ['transition'],
         'adulthood (23 - 64)': ['adult'],
         'aging(65 +)': ['aging'],
         'aging (65+)': ['aging'],
         'pre-k': ['pre-k'],
         'school': ['school'],
         'transition': ['transition'],
         'adult': ['adult'],
         'aging': ['aging'],
         'childhood(0 - 13 years)': ['pre-k', 'school'],
         'childhood (0 - 13 years)': ['pre-k', 'school'],
         'all ages': ages
    }

    @staticmethod
    def get_age_range_for_csv_data(bad_age):
        clean_age = bad_age.lower().strip()
        if clean_age in AgeRange.age_map.keys():
            return AgeRange.age_map[clean_age]
        else:
            raise Exception('Unknown age range:"' + bad_age + '" see Age Range Class to fix it.')
