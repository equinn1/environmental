data {
  int<lower=1> K;
  int<lower=1> N;
  real y[N];
  real mu[K];
}
parameters {
  simplex[K] theta;
  real<lower=0> sigma;
}
model {
  real ps[K];
  sigma ~ cauchy(0,2.5);
  mu ~ normal(0,10);
  for (n in 1:N) {
    for (k in 1:K) {
      ps[k] <- log(theta[k]) + normal_log(y[n], mu[k], sigma);
    }
    increment_log_prob(log_sum_exp(ps));
  }
}
generated quantities {
  matrix[N,K] p;
  for (n in 1:N){
    vector[K] p_raw; 
    for (k in 1:K){
      p_raw[k] <- theta[k]*exp(normal_log(y[n], mu[k], sigma));
    }
    for (k in 1:K){
      p[n,k] <- p_raw[k]/sum(p_raw);
    }
  }
}
