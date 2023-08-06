OMEG'ALPES structure
====================

The models are bases on **energy objects** and other **general classes**.

There are four kinds of energy units:

- ConsumptionUnit

- ProductionUnit

- ConversionUnit

- StorageUnit

The units inherit from the :class:`~omegalpes.energy.units.energy_units.EnergyUnit` object which itself inherit from the
:class:`~omegalpes.general.optimisation.units.Unit` object.

.. toctree::
   :maxdepth: 2

   api/energy


The **general classes** helps to build the units, the model and to plot the results

.. toctree::
   :maxdepth: 2

   api/general


