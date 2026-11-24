# Native sketch revolve

Qualification for #843. A closed radial profile creates an editable native
SolidCraft Revolve, not an extrude or a primitive approximation. The initial
full sweep has analytic volume pi * radius^2 * length. Changing radius and
sweep in the saved design must recompute the corresponding sector volume.
