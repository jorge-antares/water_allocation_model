# Multi-Objective Optimization for Water Resources #

This model allocates water resources to different activities having two goals: 
* reduce the deficit in water supply to users and
* avoid overextraction from different water sources,

along with water quality and budget contrants. For an explanation of the model, please consult the publication below.

# Model #

$$\min z = \sum_{u} \alpha_{u} DWD_{u} + \sum_{s} \beta_{s} DWD_{s}$$

$$\sum_{s} Q_{s,u} \geq WD_{u} - DWD_{u}\quad\quad \forall u$$

$$\sum_{u} Q_{s,u} \leq WA_{s} - EWA_{s}\quad\quad \forall s$$

$$\sum_{s} WQ_{s,q} Q_{s,u} \leq AQ_{u,q} \Big( \sum_{s} Q_{s,u} \Big)\quad\quad \forall u,q$$

$$\sum_{s} \Bigg( cost_{s} \Big( \sum_{u} Q_{s,u} \Big) \Bigg) \leq \text{budget}$$

$$ Q_{s,u} \leq \delta_{s,u} M\quad\quad \forall s,u$$

$$M = \sum_{s} \sum_{u} Q_{s,u}$$

# Publication #
Garcia, J. A., & Alamanos, A. (2023). A Multi-Objective Optimization Framework for Water Resources Allocation Considering Stakeholder Input. Environmental Sciences Proceedings, 25(1), 32. https://doi.org/10.3390/ECWS-7-14227
