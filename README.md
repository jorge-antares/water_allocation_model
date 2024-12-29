# Multi-Objective Optimization for Water Resources #

This model allocates water resources to different activities having two goals: 
* reduce the deficit in water supply to users and
* avoid overextraction from different water sources,

along with water quality and budget contrants.

# Model #

$$\min z = \sum_{u} \alpha_{u} DWD_{u} + \sum_{s} \beta_{s} DWD_{s}$$

$$\sum_{s} Q_{s,u} \geq WD_{u} - DWD_{u}, \forall u$$

$$\sum_{u} Q_{s,u} \leq WA_{s} - EWA_{s},\hfill \forall s$$

# Publication #
Garcia, J. A., & Alamanos, A. (2023). A Multi-Objective Optimization Framework for Water Resources Allocation Considering Stakeholder Input. Environmental Sciences Proceedings, 25(1), 32. https://doi.org/10.3390/ECWS-7-14227
