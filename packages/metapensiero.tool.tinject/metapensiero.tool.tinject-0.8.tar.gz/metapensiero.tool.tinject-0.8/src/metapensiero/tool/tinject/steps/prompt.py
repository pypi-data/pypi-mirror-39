# -*- coding: utf-8 -*-
# :Project:   metapensiero.tool.tinject -- Prompt implementation
# :Created:   gio 21 apr 2016 18:49:11 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2018 Lele Gaifax
#

from questionary import prompt

from . import Step


class Prompt(Step):
    def __init__(self, state, config):
        super().__init__(state, config)

        questions = self.questions = []

        for question in config:
            items = question.items()
            assert len(items) == 1
            for name, details in items:
                pass
            prompt = dict(details)
            prompt['name'] = name
            if 'message' not in details:
                prompt['message'] = name.capitalize()
            else:
                prompt['message'] = details['message']
            prompt['message'] += ' (%s)' % name
            kind = prompt.pop('kind', 'input')
            prompt['type'] = kind

            questions.append(prompt)

    def announce(self):
        pass

    def __call__(self, defaults, prompt_only=False, no_prompt=False):
        if no_prompt:
            return

        result = prompt(self.questions, answers=defaults)
        if not result:
            # questionary.prompt catches KeyboardInterrupt and returns an empty dictionary
            raise KeyboardInterrupt
        return result
