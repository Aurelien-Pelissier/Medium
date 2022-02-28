omega_R = .3;
omega_lambda = 0.4;
omega_M = .3;

% We must also initialize the array of parameters which we feed into the
% differential equation solver which, in general, vary in time.
ic = [1.0e-10, omega_M, omega_R, omega_lambda]
% ic starts with the initial value of the scale factor. Where does this
% come from, you may ask? Since the Friedmann equation is singular (goes to
% infinity) at a value of a = 0 (scale factor of 0, at birth of universe)
% we must use our knowledge (really given by the fact that we see the CMB)
% that the first stage of the universe post-inflation was radiation
% dominated. The Friedmann equation, when approximated for a radiation
% dominated universe, can be integrated analytically from a=0 to
% a_{0}=1e-10. This also gives our starting time, so we can define the
% entire timespace of our integrated solution to be
tSpan = [1e-15, 1.5];
% For omega total = -1.9, as an example, 0.04 as an upper limit on time gives a decent
% plot for evolution of a closed universe. The scale factor in this case
% follows a cycloid solution, but the way we're integrating you can only
% see the first half of the cycloid.
% Note also that time here is given in units of time*H_{0}, time times the
% Hubble constant (for z=0).

% One may also want to insure a certain degree of accuracy in the numerical
% integration: this can be done by using odeset to set relative and
% absolute error tolerances applying to components of the solution vector
% (a below). Effective, the smaller this number, the more time steps the
% solver will use in finding the solution.
options = odeset('reltol',1e-7,'abstol',1e-9);





% We define the Friedmann equation in numerical form in the function file
% <friedmann.m>.
% Now we integrate:
[t,a] = ode15s('friedmann', tSpan, ic, options);
% t is an array with each time corresponding to a given value in the matrix
% a. Each column in a contains the evolving values of those we initialized
% with ic and which the function 'friedmann' take as input parameters. The
% Omega values, of course, remain constant. The scale factor, in the first
% column, we can plot against time:



[~,indexa] = min(abs(a(:,1)-1));
tindex = t(indexa)
k = 13.8/tindex

figure(1); clf
plot(t*k,a(:,1),'linewidth',2)
xlabel('time [Gy]')
ylabel('scale factor [normalized to present size]')
title('Cosmological Evolution')

figure(2)
loglog(t*k*1e9,a(:,1),'linewidth',2)
xlabel('time [y]')
ylabel('scale factor [normalized to present size]')
title('Cosmological Evolution')
xlim([1e-4,1e11])
