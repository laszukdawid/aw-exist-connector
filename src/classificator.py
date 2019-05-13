import json
import re

from collections import defaultdict


class Classificator:

    UNKNOWN_CATEGORY = "UNKNOWN"

    def __init__(self, filepath="rules/categorization.json"):
        self.productivity_map = self.load_productivity_map(filepath)
        self.rules_for_categories = self.parse_productivity_map(self.productivity_map)

    def load_productivity_map(self, filepath=None):
        with open(filepath) as f:
            prod_map = json.load(f)
        return prod_map
    
    def parse_productivity_map(self, categories_and_rules):
        parsed = defaultdict(list)
        for category_name, category_entry in categories_and_rules.items():
            for subcategory_name, entry in category_entry.items():
                productivity = entry["Productivity"]
                parsed[productivity] += self.compiled_regex(entry["Rules"])
        return parsed

    def compiled_regex(self, rules):
        out = []
        for rule in rules:
            compiled_rule = {}
            for key, value in rule.items():
                compiled_rule[key] = re.compile(value)
            out.append(compiled_rule)
        return out

    def _check_category(self, compiled_rules: list, test_entry: object):
        for compiled_rule in compiled_rules:
            if self._match_rules(compiled_rule, test_entry):
                return True
        return False

    def _match_rules(self, compiled_rule: object, test_entry: object):
        for key, value in compiled_rule.items():
            if (key not in test_entry) or (not value.search(test_entry[key])):
                return False
        return True
    
    def check_productivity(self, event: object):
        data = event['data']

        for category, compiled_rules in self.rules_for_categories.items():
            if self._check_category(compiled_rules, data):
                return category

        return self.UNKNOWN_CATEGORY 
        