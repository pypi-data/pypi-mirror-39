How to contribute
#################

Please, feel free to contribute to OMEGAlpes library.

Issues & Feedback
=================
Please, have a look first to the former issues on  
    https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes/issues   
Otherwise new issues must be described on the former repository 
The following issues template are available :
    - *Bug*

New functionalities can be requested either as an *New functionalities* issue.

Please, feel free to send feedback using the following mailing list.
 omegalpes-users@groupes.renater.fr


Code contribution
=================

In order to contribute to OMEGAlpes library, you must fork the project then use
https://gricad-gitlab.univ-grenoble-alpes.fr/omegalpes/omegalpes
Your code will be reviewed, tested and inserted into the master branch.

Your code style must follow some rules, described in the following section.

Please, write unittest with your code to increase the chance and reducing the
time of integrating your code in OMEGAlpes lib.

Note that your contributions must be released under the project's license


Code Style
==========

Overall, try to respect PEP-8 
<https://www.python.org/dev/peps/pep-0008/>

If you use PyCharm or VS Code, most of the rules described here are already
checked.

General
-------

* Your code must be compatible with Python 3.3+.
* Remove unused imports.
* Imports must be after module documentation and before anything else.
* All modules must have a ``__version_info__`` tuple and a matching
  ``__version__`` string.

Formatting
----------

* Avoid inline comments; use 2 spaces when using them (mainly for type hinting)
* Break long lines after **80** characters. Exception for URLs and type hinting
  as they don't support line breaks
* Delete trailing whitespace.
* Don't include spaces after ``(``, ``[``, ``{`` or before ``}``, ``]``, ``)``.
* Don't misspell in method names.
* Don't vertically align tokens on consecutive lines.
* Use 4 spaces indentation (no tabs).
* Use an empty line between methods.
* Use 2 empty lines before class definitions.
* Use spaces around operators.
* Use spaces after commas and colons.
* Use Unix-style line endings (``\n``).
* Use 3 double-quotes (``"""``) for documentation


Naming
------

* Use ``CamelCase`` for class names.
* Use ``SNAKE_UPPERCASE`` for constants.
* Use ``snake_case`` for method names.
* ``CamelCase`` is allowed for decorator methods.
* First argument of:

  * instance methods must be ``self``
  * class methods must be ``cls``


Organization
------------

Documentation about a new functionalities should be added to a new file in
``docs/new_functionalities``.

Tests should be added to either an existing or a new sub-folder of ``tests``.
Unit tests are based on ``unittest``.
