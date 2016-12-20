model OilDrop "Model of the oil drop in the chamber"
	import SI = Modelica.SIunits;
	parameter SI.Charge q=-1.602e-19 "Default value is the elementary charge";
	parameter SI.Mass m=1.0e-15 "Mass of the drop";
	parameter SI.DynamicViscosity mu=1.846e-5 "Dynamic viscosity of air";
	parameter SI.Density rho=850 "Density of the oil";
	parameter SI.Distance d=6.0e-3 "Plate separation";
	parameter SI.Radius r=(3*m/(4*3.1415926*rho))^(1/3) "Radius of the drop";

	SI.Velocity v "Vertical velocity";
	SI.Acceleration a "Vertical acceleration";

	SI.Force F_g "Force of gravity";
	SI.Force F_d "Drag force";
	SI.Force F_c "Coulomb force";
	SI.Voltage V "Voltage between the plates";

	input Real V_comm "Commanded voltage";
	output Real v_obs "Observed velocity";

initial equation
	der(v) = 0 "Start at terminal velocity";

equation
	a = der(v);

	F_g = -9.8*m;
	F_c = -V*q/d;
	F_d = -6*3.1415926*mu*r*v;
	m*a = F_g + F_c + F_d;

	v_obs = v;
	V = V_comm;

end OilDrop;

model OilDropControl "Model of the drop, chamber, and controller"
	OilDrop drop;
	Modelica.Blocks.Discrete.Sampler sampler(samplePeriod=0.25);
	Modelica.Blocks.Discrete.ZeroOrderHold hold(samplePeriod=0.25);
	Modelica.Blocks.Continuous.Integrator integrator(k=-5e7);

equation
	//connect(drop.v_obs, integrator.u);
	connect(drop.v_obs, sampler.u);
	connect(sampler.y, integrator.u);
	connect(integrator.y, hold.u);
	connect(hold.y, drop.V_comm);

end OilDropControl;
