# Changelog

<!-- towncrier release notes start -->

## 2.0.0 (unreleased)


- Breaking: replace the `pkg_resources` namespace of `collective` with a
  PEP 420 native namespace, and move the package to a `src/` layout.
  Support Plone 6.1 and 6.2 only, on Python 3.10 to 3.13. Use 1.1 for
  Plone 4.3 to 6.0 and Python 2.7.
  [remdub]

- Add unit tests for `ComplexRecordsProxy` (the package had none), and
  list it in `__all__`.
  [remdub]

- Configure the package with plone.meta 2.12.0 (test matrix on Plone 6.2.3
  and 6.1), move its metadata to `pyproject.toml`, convert the documentation
  to Markdown and add a development environment on Plone 6.2.3 with uv.
  [remdub]


## 1.1 (2022-01-13)

- Add Python 3 & Plone 5.2 / 6.0 compatibility
  [boulch, laulaz]


## 1.0 (2016-01-29)

- Initial release
  [sunew, tomgross]
