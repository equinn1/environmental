//  zigamma.stan  zero-inflated gamma
   data {
        int<lower=0> N;                 // number of cases
        int<lower=1> J;                 // number of clusters
        real<lower=0> y[N];             // observed outcome
        int<lower=0,upper=1> iszero[N]; // indicates a zero outcome
        int<lower=1> id[N];             // cluster number for each case
        cov_matrix[2] Omega;            // diagonal prior
    }
    parameters {
        vector[2] mu;                   // means of varying effects
        cov_matrix[2] Sigma;            // var-cov matrix for varying effects
        vector[2] alpha[J];             // varying effects for each cluster
        real theta;                     // log scale
    }
    model {
        real pi;                        // probability of zero GLM
        real mugamma;                   // mean of gamma GLM
        Sigma ~ inv_wishart( 3 , Omega );
        mu[1] ~ normal( 0 , 100 );
        mu[2] ~ normal( 0 , 100 );
        theta ~ normal( 0 , 100 );
        for (j in 1:J) alpha[j] ~ multi_normal( mu , Sigma );
        for (n in 1:N) {
            pi <- inv_logit( alpha[ id[n] , 1 ] );
            mugamma <- exp( alpha[ id[n] , 2 ] );
            increment_log_prob(if_else( iszero[n] , log(pi) , log1m(pi) + gamma_log( y[n] , mugamma*exp(theta) , exp(theta) ) ));
        }
    }
    generated quantities {
        real dev;                       // deviance of each set of samples
        real pi;                        // temp for computing dev
        real mugamma;                   // temp for computing dev
        real rho;                       // correlation btw varying intercepts
        real sdi[2];                     // sd of varying intercepts
        dev <- 0;                       // not sure need to init to zero
        for ( n in 1:N ) {
            pi <- inv_logit( alpha[ id[n] , 1 ] );
            mugamma <- exp( alpha[ id[n] , 2 ] );
            dev <- dev + (-2) * if_else( iszero[n] , log(pi) , log1m(pi) + gamma_log( y[n] , mugamma*exp(theta) , exp(theta) ) );
        }
        for( k in 1:2 ) sdi[k] <- sqrt( Sigma[k,k] );
        rho <- Sigma[1,2] / sqrt( Sigma[1,1] * Sigma[2,2] );
    }