class StableMatching:
    def __init__(self):
        self.ranking_in_the_order_of_preferences_for_men = {
            "Victor": ['Bertha', 'Amy', 'Diane', 'Erika', 'Clare'],
            "Wyatt": ['Diane', 'Bertha', 'Amy', 'Clare', 'Erika'],
            "Xavier": ['Bertha', 'Erika', 'Clare', 'Bertha', 'Erika'],
            "Yancey": ['Amy', 'Diane', 'Clare', 'Bertha', 'Erika'],
            "Zeus": ['Bertha', 'Diane', 'Amy', 'Erika', 'Clare']
        }
        self.ranking_in_the_order_of_preferences_for_women = {
            "Amy": ["Zeus", "Victor", "Wyatt", "Yancey", "Xavier"],
            "Bertha": ['Xavier', 'Wyatt', 'Yancey', 'Victor', 'Zeus'],
            "Clare": ['Wyatt', 'Xavier', 'Yancey', 'Zeus', 'Victor'],
            "Diane": ['Victor', 'Zeus', 'Yancey', 'Xavier', 'Wyatt'],
            "Erika": ['Yancey', 'Wyatt', 'Zeus', 'Xavier', 'Victor']
        }
        self.temporarily_engaged = list()

    def accept_if_priority_of_the_proposed_partner_is_higher_than_current_partner(self, couple, forMan):
        if forMan:
            priority_index_proposed_partner = self.ranking_in_the_order_of_preferences_for_women[couple['woman']].index(
                couple['man'])
            current_partner = self.return_current_partner(couple['woman'])
            priority_index_current_partner = self.ranking_in_the_order_of_preferences_for_women[couple['woman']].index(
                current_partner)
            if priority_index_current_partner < priority_index_proposed_partner:
                return False
            else:
                return True

        else:
            priority_index_proposed_partner = self.ranking_in_the_order_of_preferences_for_men[couple['man']].index(
                couple['man'])
            current_partner = self.return_current_partner(couple['man'])
            priority_index_current_partner = self.ranking_in_the_order_of_preferences_for_men[couple['man']].index(
                current_partner)
            if priority_index_current_partner < priority_index_proposed_partner:
                return False
            else:
                return True

    def return_current_partner(self, person):
        import copy
        copy_of_temporarily_engaged_couple = copy.deepcopy(self.temporarily_engaged)
        match = [couple for couple in copy_of_temporarily_engaged_couple if person in couple]
        if match:
            match[0].remove(person)
            return match[0][0]

    def remove_couple_from_temporarily_engaged_list(self, person):
        for couple in self.temporarily_engaged:
            if person in couple:
                couple.remove(person)
                self.temporarily_engaged.remove(couple)
                return couple[0]
        return


class MenProposingWomen(StableMatching):

    def __init__(self):
        super(MenProposingWomen, self).__init__()
        self.men_with_no_partner = list(self.ranking_in_the_order_of_preferences_for_men.keys())

    def continue_matching_until(self):
        while len(self.men_with_no_partner) > 0:
            for man in self.men_with_no_partner:
                self.start_your_matching(man)
        print("Final Matching When Men Propose:  ", self.temporarily_engaged)

    def start_your_matching(self, man):
        print("Matching In Progress For: ", man)
        for woman in self.ranking_in_the_order_of_preferences_for_men[man]:
            the_woman_is_taken = [couple for couple in self.temporarily_engaged if woman in couple]
            if the_woman_is_taken:
                proposed_couple = {
                    "man": man,
                    "woman": woman
                }
                value = self.accept_if_priority_of_the_proposed_partner_is_higher_than_current_partner(
                    couple=proposed_couple, forMan=True)
                if value:
                    man_to_be_removed = self.remove_couple_from_temporarily_engaged_list(woman)
                    self.men_with_no_partner.append(man_to_be_removed)
                    self.temporarily_engaged.append([man, woman])
                    self.men_with_no_partner.remove(man)
                    return
            else:
                self.temporarily_engaged.append([man, woman])
                self.men_with_no_partner.remove(man)
                return


class WomenProposingMen(StableMatching):

    def __init__(self):
        super(WomenProposingMen, self).__init__()
        self.women_with_no_partner = list(self.ranking_in_the_order_of_preferences_for_women.keys())

    def continue_matching_until(self):
        while len(self.women_with_no_partner) > 0:
            for woman in self.women_with_no_partner:
                self.start_your_matching(woman)

        print("Final Matching When Woman Propose:   ", self.temporarily_engaged)

    def start_your_matching(self, woman):
        print("Matching In Progress For:   ", woman)
        for man in self.ranking_in_the_order_of_preferences_for_women[woman]:
            the_man_is_taken = [couple for couple in self.temporarily_engaged if man in couple]
            if the_man_is_taken:
                proposed_couple = {
                    "man": man,
                    "woman": woman
                }
                value = self.accept_if_priority_of_the_proposed_partner_is_higher_than_current_partner(
                    couple=proposed_couple, forMan=False)
                if value:
                    woman_to_be_removed = self.remove_couple_from_temporarily_engaged_list(man)
                    self.women_with_no_partner.append(woman_to_be_removed)
                    self.temporarily_engaged.append([man, woman])
                    self.women_with_no_partner.remove(woman)
            else:
                self.temporarily_engaged.append([man, woman])
                self.women_with_no_partner.remove(woman)
                return


stable_matching_men = MenProposingWomen()
stable_matching_men.continue_matching_until()

stable_matching_woman = WomenProposingMen()
stable_matching_woman.continue_matching_until()
