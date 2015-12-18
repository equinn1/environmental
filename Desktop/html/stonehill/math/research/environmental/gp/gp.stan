data {
  int N_ages;
  vector[N_ages] ages;
  int K[N_ages];
  int N[N_ages];
//  int K_male[N_ages];
//  int N_male[N_ages];
//  int K_female[N_ages];
//  int N_female[N_ages];
}
transformed data{
  vector[N_ages] mu;
  mu <- rep_vector(0, N_ages);
  
}
parameters {
  real<lower=0> theta_1;    //hyperparameters
  real<lower=0> theta_2;
  real<lower=0> theta_3;
  real<lower=0> theta_4;
  vector[N_ages] y;
}
model {
  matrix[N_ages, N_ages] Sigma;
  
  for (i in 1:N_ages) {
    for (j in i:N_ages) {
      Sigma[i,j] <- theta_1*exp(-theta_2*square(ages[i]-ages[j]))+theta_3+theta_4*ages[i]*ages[j];
    }
  }
  for (i in 1:N_ages) {
    for (j in (i+1):N_ages) {
      Sigma[j,i] <- Sigma[i,j];
    }
  }
  //priors
  theta_1 ~ cauchy(0,5);
  theta_2 ~ normal(0,1);
  theta_3 ~ cauchy(0,5);
  theta_4 ~ cauchy(0,5);
//  theta_1 ~ normal(0,2);
//  theta_2 ~ normal(0,2);
//  theta_3 ~ normal(0,2);
//  theta_4 ~ normal(0,2);  
  y ~ multi_normal(mu, Sigma);
  
  //likelihood
  K ~ binomial_logit(N,y);
}
generated quantities {
  vector[N_ages] p_post;
  vector[N_ages] kdn_post;
  
  for(i in 1:N_ages) {
    p_post[i]<-inv_logit(y[i]);
    kdn_post[i]<-1.0*binomial_rng(N[i], p_post[i]) / N[i];
  }
}
