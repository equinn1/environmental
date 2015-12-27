data { 
  int<lower=0> Nobs;      //number of observations
  real<lower=0> y[Nobs];    //rainfall in mm
} 
parameters {
  real<lower=0> alpha;
  real<lower=0> beta;
} 
model {
  alpha ~ normal(0,5);
  beta  ~ normal(0,5);
  y ~ gamma(alpha,beta);
}
generated quantities{
  real y_rep;
  y_rep <- gamma_rng(alpha,beta);
}
