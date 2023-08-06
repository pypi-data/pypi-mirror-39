# Guild tests

Guild tests can be run with the `check` command using the `-T` option
(`-n` here skips the general check info as we're just interested in
tests).

    >>> run("guild check -nT") # doctest: +REPORT_UDIFF
    internal tests:
      config:                    ok
      cpu-plugin:                ok
      cross-package-inheritance: ok
      dependencies:              ok
      disk-plugin:               ok
      entry-points:              ok
      guild-test:                ok
      guildfiles:                ok
      help:                      ok
      imports:                   ok
      includes:                  ok
      init:                      ok
      logging:                   ok
      ls-cmd:                    ok
      main-bootstrap:            ok
      memory-plugin:             ok
      models:                    ok
      namespaces:                ok
      nx:                        ok
      op-utils:                  ok
      ops:                       ok
      package:                   ok
      plugins:                   ok
      python-utils:              ok
      run-flags:                 ok
      run-output:                ok
      runs:                      ok
      tables:                    ok
      tfevents:                  ok
      utils:                     ok
      var:                       ok
      workflow:                  ok
    <exit 0>
