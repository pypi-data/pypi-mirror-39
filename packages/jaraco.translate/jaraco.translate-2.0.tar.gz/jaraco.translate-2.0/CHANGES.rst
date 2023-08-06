2.0
===

* In pmxbot plugin, drop support for legacy config variable.
  Any applications still using ``google_translate_API_key``
  should instead supply that value with ``Google API key``.

* Drop support for Python 3.5 and earlier.

1.3
===

Prefer the 'Google API key' config variable for the
pmxbot plugin, matching the expectation in pmxbot
1115.2 for the search function.
