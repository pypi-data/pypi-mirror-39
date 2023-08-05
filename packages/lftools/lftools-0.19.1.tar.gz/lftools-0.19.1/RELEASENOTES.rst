=======
lftools
=======

.. _lftools_0.0.0:

0.0.0
=====

.. _lftools_0.0.0_New Features:

New Features
------------

.. releasenotes/notes/credential-input-73245c664c98cdc1.yaml @ b'9b3f9748c5ef839e941adef6cc15e9214c598bfa'

- Provide additional methods to pass LFID to lftools than lftools.ini
  
  1. Via explicit ``--password`` parameter
  2. Via environment variable ``LFTOOLS_PASSWORD``
  3. At runtime if ``--interactive`` mode is set

.. releasenotes/notes/debug-e80d591d478e69cc.yaml @ b'2380b4e056c54b0258bffa43972fbc171b4af481'

- Add a new ``--debug`` flag to enable extra troubleshooting information.
  This flag can also be set via environment variable ``DEBUG=True``.

.. releasenotes/notes/deploy_nexus-4feb8fc7e24daaf0.yaml @ b'837552cb3308a4cafaf8b283e6c78739f25410e8'

- Refactored deploy_nexus function
  from shell/deploy to pure Python to be more portable with Windows systems.
  Also added a number of unit tests to cover all executable branches of the
  code.

.. releasenotes/notes/deploy_nexus_stage-e5f6f3e068f88ca4.yaml @ b'd2aca2e11395c596080e6a63ad59acb15abfc61d'

- Refactored deploy_nexus_stage function
  from shell/deploy to pure Python to be more portable with Windows systems.
  Also added a number of unit tests to cover all executable branches of the
  code.

.. releasenotes/notes/jenkins-25629106553ebbd5.yaml @ b'54c0bdb08963841eecd01cc816d485d15f1e9de1'

- Add support to the **jenkins** command to parse ``jenkins_jobs.ini`` for
  configuration if **server** parameter passed is not a URL.

.. releasenotes/notes/jenkins-c247796de6390391.yaml @ b'7d2b155ff78d52a94ada949cf85ffd17512cbc45'

- Add a **jobs** sub-command to **jenkins** command to enable or disable Jenkins
  Jobs that match a regular expression.

.. releasenotes/notes/jenkins-conf-e33db422385a2203.yaml @ b'fe703b4d2360c4d59595aa8f0118ab8b5da2bdb1'

- Add ``--conf`` parameter to jenkins subcommand to allow choosing a jjb
  config outside of the default paths.

.. releasenotes/notes/jenkins-token-cmd-8e5cdce9175f69a1.yaml @ b'9d61520841d6ed796d5e3941740d5800cfde4b54'

- Add new cmd to fetch Jenkins token from user account. An optional
  ``--change`` parameter can be passed to have Jenkins change the API token.
  
  Usage: lftools jenkins token [OPTIONS]
  
    Get API token.
  
  Options:
    --change  Generate a new API token.
    --help    Show this message and exit.

.. releasenotes/notes/jenkins-token-init-4af337e4d79939f1.yaml @ b'698a8bbb93d65158a5ffe4bf6a13a0445a56feac'

- Add jenkins token init command to initialize a new server section in
  jenkins_jobs.ini. This command uses credentials found in lftools.ini to
  initialize the new Jenkins server configuration.
  
  Usage: lftools jenkins token init [OPTIONS] NAME URL

.. releasenotes/notes/jenkins-token-reset-1297047cb9b5804d.yaml @ b'51fe465bee050dae5a02ee7e07bba978cc5d4ea3'

- Add jenkins token reset command to automatically reset API tokens for all
  Jenkins systems configured in jenkins_jobs.ini.
  
  Usage: lftools jenkins token reset [OPTIONS] [SERVER]

.. releasenotes/notes/jjb-ini-839c14f4e500fd56.yaml @ b'fb5ffd18315c55eb2c5625de101a4d42b050406b'

- We now support locating the jenkins_jobs.ini in all the same default search
  paths as JJB supports. Specifically in this order:
  
  #. $PWD/jenkins_jobs.ini
  #. ~/.config/jenkins_jobs/jenkins_jobs.ini
  #. /etc/jenkins_jobs/jenkins_jobs.ini

.. releasenotes/notes/ldap-info-017df79c3c8f9585.yaml @ b'4d7ce295121e166f2fb18417acd8f5193d4b382c'

- $ lftools ldap
  
  Usage: lftools ldap [OPTIONS] COMMAND [ARGS]...
  
  .. code-block:: none
  
     Commands:
       autocorrectinfofile  Verify INFO.yaml against LDAP group.
       csv                  Query an Ldap server.
       inactivecommitters   Check committer participation.
       yaml4info            Build yaml of commiters for your INFO.yaml.

.. releasenotes/notes/ldap-info-017df79c3c8f9585.yaml @ b'4d7ce295121e166f2fb18417acd8f5193d4b382c'

- $ lftools infofile
  
  .. code-block:: none
  
     Commands:
       get-committers   Extract Committer info from INFO.yaml or LDAP...
       sync-committers  Sync committer information from LDAP into...

.. releasenotes/notes/nexus-docker-cmds-2ea1515887e0ab00.yaml @ b'cd546f4628c5b9c09656b1a99112ff6feedbbfbd'

- Docker list and delete commands for Nexus docker repos.
  
  Usage: lftools nexus docker [OPTIONS] COMMAND [ARGS]...
  
  .. code-block:: none
  
     Commands:
       delete  Delete all images matching the PATTERN.
       list    List images matching the PATTERN.

.. releasenotes/notes/openstack-delete-stale-stacks-bec3f2c27cd7cbe5.yaml @ b'a440a11bfa4d8f603589b1cf66caa26ccc57ce1d'

- Add a new ``delete-stale`` option to the **stack** command.
  
  This function compares running builds in Jenkins to active stacks in
  OpenStack and determines if there are orphaned stacks and removes them.

.. releasenotes/notes/openstack-stack-08f643f16b75bfb8.yaml @ b'de992398836117670b1271f63871755f8cac46a7'

- Add stack command.
  https://jira.linuxfoundation.org/browse/RELENG-235

.. releasenotes/notes/openstack-stack-08f643f16b75bfb8.yaml @ b'de992398836117670b1271f63871755f8cac46a7'

- Add stack create sub-command.
  https://jira.linuxfoundation.org/browse/RELENG-235
  
  Usage: lftools openstack stack create NAME TEMPLATE_FILE PARAMETER_FILE

.. releasenotes/notes/openstack-stack-08f643f16b75bfb8.yaml @ b'de992398836117670b1271f63871755f8cac46a7'

- Add stack delete sub-command.
  https://jira.linuxfoundation.org/browse/RELENG-235
  
  Usage: lftools openstack stack create NAME

.. releasenotes/notes/refactor-copy-archives-b5e7ee75fc7bf271.yaml @ b'a889de0e5c9891e58bb99cc1d2e6dbff4e125885'

- The shell/deploy file's copy_archives() function has been reimplemented in
  pure Python for better portability to Windows systems.

.. releasenotes/notes/refactor-deploy-archives-5f86cfbe8415defc.yaml @ b'0fcafa53a92105954afa47397d6b815bd9cc9f5d'

- Refactored deploy_archives() function from shell/deploy to pure Python to
  be more portable with Windows systems.

.. releasenotes/notes/refactor-deploy-logs-8631ffcf7eb7cad2.yaml @ b'dfab0ddcb3378c9fcaa21d2757babab4999ebf3e'

- Refactored deploy_logs() function from shell/deploy to pure Python to
  be more portable with Windows systems.

.. releasenotes/notes/refactor-deploy-nexus-zip-018f7e5ced9f558d.yaml @ b'de342e6c2e5197934377fb610e9dbb4019aec792'

- Refactored deploy_nexus_zip() function from shell/deploy to pure Python to
  be more portable with Windows systems.

.. releasenotes/notes/refactor-deploy-stage-create-close-7b3fcc911023a318.yaml @ b'8aa95360e93db3d8122920313786794215a158eb'

- Refactored nexus_stage_repo_close(), and nexus_repo_stage_create() function
  from shell/deploy to pure Python to be more portable with Windows systems.
  Also added a number of unit tests to cover all executable branches of the
  code.

.. releasenotes/notes/share-openstack-images-4f1e3d18fdcb488b.yaml @ b'50ce256a1e792c82f409c7b66b7b8bad1a9b5a37'

- Add an ``openstack image share`` sub-command to handle sharing images
  between multiple tenants. Command accepts a space-separated list of tenants
  to share the provided image with.
  
  Usage: ``lftools openstack image share [OPTIONS] IMAGE [DEST]...``

.. releasenotes/notes/upload-openstack-images-99d86c78044850b0.yaml @ b'2aa73e8b4efaa399002983f04bc5a85089402301'

- Add an ``openstack image upload`` sub-command to handle uploading images
  to openstack.
  
  Usage: ``Usage: lftools openstack image upload [OPTIONS] IMAGE NAME...``

.. releasenotes/notes/upload_maven_file_to_nexus-f31b14521e4a0aca.yaml @ b'06f9c845e0bdc1bcbd80a61460c06eb670c378f4'

- Refactored upload_maven_file_to_nexus function
  from shell/deploy to pure Python to be more portable with Windows systems.
  Also added a number of unit tests to cover all executable branches of the
  code.


.. _lftools_0.0.0_Deprecation Notes:

Deprecation Notes
-----------------

.. releasenotes/notes/deploy_nexus-4feb8fc7e24daaf0.yaml @ b'837552cb3308a4cafaf8b283e6c78739f25410e8'

- shell/deploy script's deploy_nexus
  function is now deprecated and will be removed in a future release.

.. releasenotes/notes/deploy_nexus_stage-e5f6f3e068f88ca4.yaml @ b'd2aca2e11395c596080e6a63ad59acb15abfc61d'

- shell/deploy script's deploy_nexus_stage
  function is now deprecated and will be removed in a future release.

.. releasenotes/notes/logger-1aa26520f6d39fcb.yaml @ b'28fc57084d22dd96db149069666e945b039b474a'

- Remove support for modifying the logger via logging.ini. It was a good idea
  but in practice this is not really used and adds extra complexity to
  lftools.

.. releasenotes/notes/refactor-copy-archives-b5e7ee75fc7bf271.yaml @ b'a889de0e5c9891e58bb99cc1d2e6dbff4e125885'

- The shell/deploy script's copy_archives() function is now deprecated and
  will be removed in a later version. We recommend migrating to the lftools
  pure Python implementation of this function.

.. releasenotes/notes/refactor-deploy-archives-5f86cfbe8415defc.yaml @ b'0fcafa53a92105954afa47397d6b815bd9cc9f5d'

- shell/deploy script's deploy_archives() function is now deprecated and will
  be removed in a future release.

.. releasenotes/notes/refactor-deploy-logs-8631ffcf7eb7cad2.yaml @ b'dfab0ddcb3378c9fcaa21d2757babab4999ebf3e'

- shell/deploy script's deploy_logs() function is now deprecated and will
  be removed in a future release.

.. releasenotes/notes/refactor-deploy-nexus-zip-018f7e5ced9f558d.yaml @ b'de342e6c2e5197934377fb610e9dbb4019aec792'

- shell/deploy script's deploy_nexus_zip() function is now deprecated and will
  be removed in a future release.

.. releasenotes/notes/refactor-deploy-stage-create-close-7b3fcc911023a318.yaml @ b'8aa95360e93db3d8122920313786794215a158eb'

- shell/deploy script's nexus_stage_repo_close() and nexus_stage_repo_create()
  function is now deprecated and will be removed in a future release.

.. releasenotes/notes/upload_maven_file_to_nexus-f31b14521e4a0aca.yaml @ b'06f9c845e0bdc1bcbd80a61460c06eb670c378f4'

- shell/deploy script's upload_maven_file_to_nexus
  function is now deprecated and will be removed in a future release.


.. _lftools_0.0.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/docs-cad1f396741b9526.yaml @ b'32275fd2e51e759b4b2c4c4b5f6c6ea4baaffa6c'

- Fix broken openstack and sign help command output in docs.

.. releasenotes/notes/fix-get-credentials-6759fee7366c5602.yaml @ b'e7009cb9e38b694a4515b9124654d6400e7e1d09'

- The get-credentials command is now fixed since it was was broken after
  refactoring done in Gerrit patch I2168adf9bc992b719da6c0350a446830015e6df6.

.. releasenotes/notes/ldap-b50f699fc066890f.yaml @ b'3a409e15b5ad16715525fc86ad163f61b890645f'

- The v0.16.0 pulled in a new ldap module which breaks if the ldap devel
  libraries are not available on the system trying to use it. This hotfix
  makes the ldap module optional.

.. releasenotes/notes/unnecessary-sign-dir-35677f94e948d2a8.yaml @ b'92b39c9e0c6033cff0535393f7a089312f0b15a9'

- Running the lftools CLI was unexpectedly creating unnecessary
  gpg-signatures directories in the /tmp directory and not cleaning
  them up.


.. _lftools_0.0.0_Other Notes:

Other Notes
-----------

.. releasenotes/notes/jenkins-class-refactor-91250f2bba941c26.yaml @ b'c15e450508a4b34abcc208a87f32a9873e44f4a3'

- Refactored the Jenkins object into a class to allow us to reuse it outside
  of the Jenkins command group.

.. releasenotes/notes/logger-c53984ef7b1da53f.yaml @ b'4edf459161faeaebe1614ff16f18101f0785adc6'

- Enhance logger subsystem to work better as a CLI program. This is a first
  step to migrating all lftools subsystems to use the logger instead of print
  statements everywhere.

