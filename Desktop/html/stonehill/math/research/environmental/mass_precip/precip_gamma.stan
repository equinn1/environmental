data { 
  int<lower=0> Nobs;      //number of observations
  real<lower=0> y[Nobs];    //rainfall in mm
} 
parameters {
  real<lower=0> alpha;
  real<lower=0> beta;
} 
model {
  alpha ~ cauchy(0,5);
  beta  ~ cauchy(0,5);
  y ~ gamma(alpha,beta);
//  y ~ weibull(alpha,beta);
}
generated quantities{
  real y_rep;
  y_rep <- gamma_rng(alpha,beta);
//  y_rep <- weibull_rng(alpha,beta);
}
