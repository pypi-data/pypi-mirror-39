cl__1 = 1;
Point(1) = {-1.3, -0.1, 0, 1};
Point(2) = {-1.4, 0.8, 1, 1};
Point(3) = {-0.5, 0.5, 0, 1};
Point(4) = {-1.6, 0.3, 0, 1};
Line(1) = {2, 3};
Line(2) = {4, 1};
Line(3) = {3, 1};
Line(4) = {2, 4};
Line Loop(6) = {1, 3, -2, -4};
Ruled Surface(6) = {6};

Mesh.ElementOrder = 2;
Mesh.CharacteristicLengthFactor = 0.1;