qmesh-containers
=================

This repository is aimed at facilitating isolated containers, in turn used to test, develop or use `qmesh <https://www.qmesh.org>`_.

The files in this repository are used to create docker containers for:

* Using qmesh in various platforms with minimal installation; only docker and basic python packages are required.
* Testing qmesh packages. The container set-up files are used in the qmesh CI/CD infrastructure.
* Developing qmesh. The containers include all necessary dependencies for qmesh, and provide a clean sandbox environment ideal for development.



Installation & Dependencies
-----------------------------

To use the qmesh container utility you must have docker installed on your machine. Please follow the docker installation instructions.



Development, Maintenance and Licence
------------------------------------

qmesh-containers was developed and is maintained by `Alexandros Avdis <https://orcid.org/0000-0002-2695-3358>`_ and `Jon Hill  <https://orcid.org/0000-0003-1340-4373>`_.
Please see file `AUTHORS.md <https://bitbucket.org/qmesh-developers/qmesh-containers/raw/HEAD/AUTHORS.md>`_ for more information.

qmesh-containers is an open-source project distributed under the GNU General Public Licence v3 (`GPL v3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_)
The file `LICENCE <https://bitbucket.org/qmesh-developers/qmesh-containers/raw/HEAD/LICENSE>`_ contains a complete copy of the licence.

The source code is freely available to download and adapt, under the conditions stated in the `LICENCE <https://bitbucket.org/qmesh-developers/qmesh-containers/raw/HEAD/LICENSE>`_ file.
However, we follow a closed-development approach, where maintenance and development is carried out by the package originators.
We have opted for this approach to limit the resources needed for development: A larger development team necessitates larger management structures and significant CI/CD expenditure.
Larger management structures will absorb time intended for other exciting and useful research.
CI/CD expenditure could threaten our aim to offer a focused package, at no monetary costs to the users.



Documentation 
---------------

You can access relevant documentation through the following avenues:

* The `qmesh website <https://www.qmesh.org>`_.
* The `qmesh synoptic manual <https://qmesh-synoptic-manual.readthedocs.io/en/latest>`_.
