Multi-Agent Insights Documentation
==================================

.. toctree::
   :maxdepth: 2

   agents
   graph
   security
   monitoring

Architecture Diagram
--------------------
.. plantuml::
   @startuml
   actor User
   User -> Planner
   Planner -> Coder
   Coder -> Reviewer
   Reviewer -> Executor
   Executor -> Analyst
   @enduml
