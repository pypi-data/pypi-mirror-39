*************************
Importing SDSS_Catl_Utils
*************************

In order to encourage consistency amongst users in importing and using ``SDSS_Catl_Utils``
functionality, we have put together the following guidelines.

Since most of the functionality in ``SDSS_Catl_Utils`` resides in sub-packages, importing
astropy as::

    >>> import sdss_catl_utils

is not very useful. Instead, it is best to import the desired sub-package
with the syntax::

    >>> from sdss_catl_utils import subpackage  # doctest: +SKIP
