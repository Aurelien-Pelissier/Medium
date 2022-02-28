% MJA 2011
function adot = friedmann( t, parms )
% This function takes in two parameters, t the time, and parms, an array of
% four parameters, the first giving the scale factor at time t, followed by
% the three energy densities, normalized by the critical density of the
% universe in the order: matter, radiation, cosmological constant/dark
% energy. It returns an array of [instantaneous derivative of scale factor,
% matter density, rad. density, cosm. constant density]

adot = [sqrt( parms(2)/parms(1) + parms(3)/ parms(1)^2 + parms(4)*parms(1)^2 - (1-sum(parms(2:4)))); parms(2); parms(3); parms(4)];
end