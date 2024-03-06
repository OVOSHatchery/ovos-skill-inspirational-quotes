# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

import requests
from ovos_workshop.intents import IntentBuilder
from ovos_workshop.skills import OVOSSkill

__author__ = 'oliveralonzo'


class InspirationalQuotesSkill(OVOSSkill):

    # Loads the files needed, creates and registers intents
    def initialize(self):

        inspirational_quote_intent = IntentBuilder(
            "InspirationalQuoteIntent").require(
            "InspirationalQuoteKeyword").build()
        self.register_intent(inspirational_quote_intent,
                             self.handle_inspirational_quote_intent)

        quote_intent = IntentBuilder("QuoteIntent").require(
            "QuoteKeyword").build()
        self.register_intent(quote_intent, self.handle_quote_intent)

    # Defines Mycroft's behavior for the inspirational quote intent
    def handle_inspirational_quote_intent(self, message):
        quote, author = self.get_quote()
        if quote and author:
            self.speak_dialog("inspirational.quote",
                              data={
                                  'quote': quote,
                                  'author': author
                              })
        else:
            self.speak_dialog("not.found")

    # Defines Mycroft's behavior for the quote intent
    def handle_quote_intent(self, message):
        quote, author = self.get_quote()
        if quote and author:
            self.speak_dialog("quote", data={'quote': quote, 'author': author})
        else:
            self.speak_dialog("not.found")

    def get_quote(self):
        try:
            parameters = {'method': 'getQuote', 'format': 'json', 'lang': 'en'}
            url = "http://api.forismatic.com/api/1.0/"
            response = requests.get(url, params=parameters).json()
            quote = response["quoteText"].strip(' ."\'\t\r\n')
            author = response["quoteAuthor"].strip(' ."\'\t\r\n')
            return quote, author
        except:
            return "", ""
