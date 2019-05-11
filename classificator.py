import json
import re


class Classificator:

    UNKNOWN_CATEGORY = "UNKNOWN"

    def __init__(self, filepath="productivity.json"):
        self.productivity_map = self.load_productivity_map(filepath)

        ## TODO: Is it worth to have custom tags? self.setattr(self, key, compiled_regex(f(key)) ?
        self.rules_for_categories = self.parse_productivity_map(self.productivity_map)
    
    def parse_productivity_map(self, categories_and_rules):
        parsed = {}
        for category, rules in categories_and_rules.items():
            parsed[category] = self.compiled_regex(rules)
        return parsed

    def load_productivity_map(self, filepath=None):
        with open(filepath) as f:
            prod_map = json.load(f)
        return prod_map

    def compiled_regex(self, rules):
        out = []
        for rule in rules:
            compiled_rule = {}
            for key, value in rule.items():
                print("{}: {}".format(key, value))
                compiled_rule[key] = re.compile(value)
            out.append(compiled_rule)
        return out

    def check_category(self, compiled_rules, test_entry):
        for compiled_rule in compiled_rules:
            if self._match_rules(compiled_rule, test_entry):
                return True
        return False

    def _match_rules(self, compiled_rule, test_entry):
        for key, value in test_entry.items():
            if key not in compiled_rule or (not compiled_rule[key].search(value)):
                return False
        return True

    
    def check_productivity(self, event):
        data = event['data']

        for category, compiled_rules in self.rules_for_categories.items():
            if self.check_category(compiled_rules, data):
                return category

        return self.UNKNOWN_CATEGORY 
        