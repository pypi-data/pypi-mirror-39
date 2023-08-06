.. -*- coding: utf-8 -*-

Changes
-------

0.8 (2018-12-16)
~~~~~~~~~~~~~~~~

- Use questionary__ instead of whaaaaat_: the latter seems stale, the former is based on
  `prompt_toolkit`_ v2

  __ https://pypi.org/project/questionary/

- Use `ruamel.yaml`__ instead of PyYAML__

  __ https://pypi.org/project/ruamel.yaml/
  __ https://pypi.org/project/PyYAML/

- New option ``--answers-file`` mode, to read answers from a ``YAML`` file


0.7 (2017-06-02)
~~~~~~~~~~~~~~~~

- Use whaaaaat_ instead of inquirer_: being based on `prompt_toolkit`_ it offers a better
  user experience and should be usable also under Windows


0.6 (2017-03-22)
~~~~~~~~~~~~~~~~

- Minor tweak, no externally visible changes


0.5 (2016-11-07)
~~~~~~~~~~~~~~~~

- All steps support a “when” condition


0.4 (2016-06-16)
~~~~~~~~~~~~~~~~

- New changefile tweak to insert a line in a sorted block


0.3 (2016-05-22)
~~~~~~~~~~~~~~~~

- New ability to repeat a list of substeps


0.2 (2016-05-19)
~~~~~~~~~~~~~~~~

- First release on PyPI


0.1 (2016-04-26)
~~~~~~~~~~~~~~~~

- Initial effort
