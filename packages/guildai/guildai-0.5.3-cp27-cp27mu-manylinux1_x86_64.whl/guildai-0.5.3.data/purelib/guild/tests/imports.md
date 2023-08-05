# Imports

    >>> import importlib
    >>> import os
    >>> import guild

    >>> def iter_mods():
    ...   guild_root = os.path.dirname(guild.__file__)
    ...   for root, dirs, files in os.walk(guild_root, topdown=True):
    ...     if "tests" in dirs: dirs.remove("tests")
    ...     if "external" in dirs: dirs.remove("external")
    ...     for name in files:
    ...       if name.endswith(".py"):
    ...         mod_path = os.path.join(root, name)
    ...         mod_relpath = os.path.relpath(mod_path, guild_root)
    ...         mod_name = "guild." + mod_relpath.replace(os.path.sep, ".")[:-3]
    ...         yield importlib.import_module(mod_name)

    >>> for name in sorted([m.__name__ for m in iter_mods()]):
    ...   print(name) # doctest: +REPORT_UDIFF
    guild.__init__
    guild._api
    guild._test
    guild.cli
    guild.click_util
    guild.cmd_impl_support
    guild.commands.__init__
    guild.commands.cat
    guild.commands.cat_impl
    guild.commands.check
    guild.commands.check_impl
    guild.commands.compare
    guild.commands.compare_impl
    guild.commands.diff
    guild.commands.diff_impl
    guild.commands.download
    guild.commands.download_impl
    guild.commands.export
    guild.commands.help
    guild.commands.help_impl
    guild.commands.import_
    guild.commands.index
    guild.commands.index_impl
    guild.commands.init
    guild.commands.init_impl
    guild.commands.install
    guild.commands.label
    guild.commands.ls
    guild.commands.ls_impl
    guild.commands.main
    guild.commands.main_impl
    guild.commands.models
    guild.commands.models_impl
    guild.commands.new
    guild.commands.new_impl
    guild.commands.open_
    guild.commands.open_impl
    guild.commands.operations
    guild.commands.operations_impl
    guild.commands.package
    guild.commands.package_impl
    guild.commands.packages
    guild.commands.packages_delete
    guild.commands.packages_impl
    guild.commands.packages_info
    guild.commands.packages_list
    guild.commands.pull
    guild.commands.push
    guild.commands.remote
    guild.commands.remote_impl
    guild.commands.remote_impl_support
    guild.commands.remote_start
    guild.commands.remote_status
    guild.commands.remote_stop
    guild.commands.remote_support
    guild.commands.remotes
    guild.commands.remotes_impl
    guild.commands.run
    guild.commands.run_impl
    guild.commands.runs
    guild.commands.runs_delete
    guild.commands.runs_diff
    guild.commands.runs_export
    guild.commands.runs_impl
    guild.commands.runs_import
    guild.commands.runs_info
    guild.commands.runs_label
    guild.commands.runs_list
    guild.commands.runs_pull
    guild.commands.runs_purge
    guild.commands.runs_push
    guild.commands.runs_restore
    guild.commands.runs_stop
    guild.commands.runs_support
    guild.commands.s3_sync
    guild.commands.s3_sync_impl
    guild.commands.search
    guild.commands.search_impl
    guild.commands.server_support
    guild.commands.service_impl_support
    guild.commands.shell
    guild.commands.shell_impl
    guild.commands.shutdown_timer
    guild.commands.shutdown_timer_impl
    guild.commands.stop
    guild.commands.sync
    guild.commands.sync_impl
    guild.commands.sys
    guild.commands.tensorboard
    guild.commands.tensorboard_impl
    guild.commands.tensorflow
    guild.commands.tensorflow_check_main
    guild.commands.tensorflow_impl
    guild.commands.tensorflow_inspect
    guild.commands.test
    guild.commands.test_impl
    guild.commands.uninstall
    guild.commands.view
    guild.commands.view_impl
    guild.commands.view_tester
    guild.commands.watch
    guild.commands.watch_impl
    guild.commands.workflow_impl
    guild.config
    guild.deps
    guild.entry_point_util
    guild.guildfile
    guild.help
    guild.index
    guild.init
    guild.log
    guild.main
    guild.main_bootstrap
    guild.model
    guild.namespace
    guild.op
    guild.op_main
    guild.op_util
    guild.opref
    guild.package
    guild.package_main
    guild.pip_util
    guild.plugin
    guild.plugins.__init__
    guild.plugins.cloudml
    guild.plugins.cloudml_op_main
    guild.plugins.cpu
    guild.plugins.disk
    guild.plugins.gpu
    guild.plugins.keras
    guild.plugins.keras_op_main
    guild.plugins.memory
    guild.plugins.perf
    guild.plugins.tensorflow_util
    guild.plugins.training_pkg_main
    guild.python_util
    guild.remote
    guild.remote_run_support
    guild.remote_util
    guild.remotes.__init__
    guild.remotes.ec2
    guild.remotes.s3
    guild.remotes.ssh
    guild.remotes.ssh_util
    guild.remotes.tpu
    guild.resolver
    guild.resource
    guild.resourcedef
    guild.run
    guild.service
    guild.serving_util
    guild.tabview
    guild.tensorboard
    guild.test
    guild.uat
    guild.util
    guild.var
    guild.view
    guild.workflow.__init__
    guild.workflow.deps
    guild.workflow.op_node
    guild.workflow.sources_node
