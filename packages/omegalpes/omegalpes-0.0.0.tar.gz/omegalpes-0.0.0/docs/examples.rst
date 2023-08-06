OMEG'ALPES Examples
===================

Please find a short description to detail the steps to create a model.
This description is followed by three examples to learn the kinds of energy systems OMEG'ALPES can model.

.. contents::
    :depth: 1
    :local:

Steps to create a model
-----------------------
You can create a new file on the folder examples and put you data files on the folder examples.data

1. Imports
++++++++++
You will have mandatory imports like:

.. code-block:: python

    from OMEGALPES.energy.energy_nodes import EnergyNode

    from OMEGALPES.general.optimisation.model import OptimisationModel

    from OMEGALPES.general.time import TimeUnit

The others imports will depend on the model you have modeled.

For instance:

.. code-block:: python

    from pulp import LpStatus, GUROBI_CMD

    from OMEGALPES.energy.units.production_units import VariableProductionUnit

    from OMEGALPES.energy.units.consumption_units import FixedConsumptionUnit

    from OMEGALPES.general.utils import plot_quantity, plt

2. Empty model and Time operation
+++++++++++++++++++++++++++++++++
You need first to create an empty model.

.. code-block:: python

   model = OptimisationModel(name='name_of_your_model')

You also have to define your time operation for your model.

.. code-block:: python

   time = TimeUnit(start='DD/MM/YYYY', periods=length_of_the_operation, dt=1_if_hours)

3. Energy units
+++++++++++++++
3.1 Data files
~~~~~~~~~~~~~~
You have the possibility to extra data from files.
We recommend you to put your data files in the folder examples.data.
To read the data from the files:

.. code-block:: python

   data_file = open("data/file_name.txt", "r")

Then, put your data in objects to be able to use them for the energy unit definition

.. code-block:: python

   energy_data = [e_value for e_value in map(float, data_file)]

3.2 Energy units
~~~~~~~~~~~~~~~~
You have three types of energy units

* consumption_units

    * :class:`~energy.units.consumption_units.ConsumptionUnit`

    * :class:`~energy.units.consumption_units.FixedConsumptionUnit`

    * :class:`~energy.units.consumption_units.VariableConsumptionUnit`

* production_units

    * :class:`~energy.units.production_units.ProductionUnit`

    * :class:`~energy.units.production_units.FixedProductionUnit`

    * :class:`~energy.units.production_units.VariableProductionUnit`

* conversion_unit

    * :class:`~energy.units.conversion_units.ConversionUnits`

    * :class:`~energy.units.conversion_units.ElectricalToHeatConversionUnits`

    * :class:`~energy.units.conversion_units.HeatPump`

* storage_unit

    * :class:`~energy.units.storage_units.StorageUnit`

These energy units inherited from :class:`~energy.units.energy_units.EnergyUnit` itself inherited from
:class:`~general.optimisation.units.Unit`

Please find a fixed load consumption unit and a variable production unit examples

.. code-block:: python

   consumption_unit = FixedConsumptionUnit(time=time, 'comsumption_unit_name', energy_type='Electrical',
                                                p=energy_data)
   production_unit = VariableProductionUnit(time=time, name='production_unit_name', energy_type='Electrical')

4. Energy nodes
+++++++++++++++
The units are linked with  nodes. You first need to create a node, at least one per energy type, and then to connect
the units you have created to the nodes.

.. code-block:: python

   node = EnergyNode(time, 'node_name', energy_type='Electrical')
   node.connect_units(consumption_unit, production_unit)

5. Objective
++++++++++++
You need to add at least one objective. You already have some objective methods linked to energy unit.
example:

.. code-block:: python

   production_unit.minimize_operating_cost()

You can also create your own objective, linked to an energy unit or on a node,
using the :class:`~general.optimisation.elements.Objective` defined in the folder general\optimisation\elements

If there are more than one objective they are summed.

6. Model and resolution
+++++++++++++++++++++++
Do not forget to add the energy nodes to the model

.. code-block:: python

   model.addNode(time, node)

.. note::
   you may need to add the energy units if a flow is created with a unit but not connected to a node

To finish, write the problem as LP formulation and solve the problem using a solver

.. code-block:: python

   model.writeLP('optim_models\elec_prod_simple_example.lp')
   model.solve_and_update(solver_name)

7. Graphical Results
++++++++++++++++++++
If you want graphical results, you can use the following classes

* :class:`~general.plots.Plot_energetic_flows`

* :class:`~general.plots.Plot_quantity`

* :class:`~general.plots.Plot_energy_mix`

or matplotlib


**Please have a look to the examples code**


Example 1. Electrical system operation
--------------------------------------
This first module is an example of decision support for electrical system operations.
The electrical system operator needs to decide whether to provide electricity from the grid_production A or B
depending on their operating costs. The two grid productions are providing energy to a dwelling with a fixed
electricity consumption profile.

.. figure::  images/example_electrical_system_operation_presentation.jpg
   :align:   center

   *Figure 1: Principle diagram of the electrical system operation example*


Example 2. Storage design
-------------------------
The storage_design module is an example of storage capacity optimization. A production unit and a storage system power a
load with a fixed consumption profile. The production unit has a maximum power value and the storage system has maximum
charging and discharging power values. The objective is to minimize the capacity of the storage system while meeting
the load during the whole time horizon.

.. figure::  images/example_storage_design_presentation.jpg
   :align:   center

   *Figure 2: principle diagram of the storage design example*

Example 3. Waste heat recovery
------------------------------
In the waste_heat_recovery module, an electro-intensive industrial process consumes electricity and
rejects heat. This waste heat is recovered by a system composed of a heat pump in order to increase
the heat temperature, and a thermal storage that is used to recover more energy and have a more
constant use of the heat pump. This way, the waste heat is whether recovered or dissipated depending
on the waste heat recovery system sizing. The heat is then injected on a district heat network to
provide energy to a district heat load. A production unit of the district heat network provides the extra
heat.

.. figure::  images/example_waste_heat_recovery_presentation.jpg
   :align:   center

   *Figure 3: principle diagram of the waste heat recovery example*