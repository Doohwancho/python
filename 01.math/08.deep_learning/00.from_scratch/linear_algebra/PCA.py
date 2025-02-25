class PCA:
    """
    Principal Component Analysis using SVD
    """
    def __init__(self, n_components: Optional[int] = None, tolerance: float = 1e-10):
        self.n_components = n_components
        self.tolerance = tolerance
        self.components_ = None
        self.explained_variance_ = None
        self.explained_variance_ratio_ = None
        self.mean_ = None
        self.singular_values_ = None

    def fit(self, X: Matrix):
        n_samples = X.rows
        n_features = X.cols
        
        # Set number of components if not specified
        if self.n_components is None:
            self.n_components = min(n_samples, n_features)
        
        # Center the data
        self.mean_ = X.mean(axis=0)
        X_centered = X - Matrix([self.mean_._data[0]] * n_samples)
        
        # Perform SVD
        U, S, Vt = X_centered.svd(tolerance=self.tolerance)
        
        # Extract singular values
        self.singular_values_ = [S[i][i] for i in range(min(S.rows, S.cols))]
        
        # Compute explained variance
        self.explained_variance_ = [s * s / (n_samples - 1) 
                                  for s in self.singular_values_]
        total_var = sum(self.explained_variance_)
        self.explained_variance_ratio_ = [var / total_var 
                                        for var in self.explained_variance_]
        
        # Store components (right singular vectors)
        self.components_ = Matrix([Vt._data[i] 
                                 for i in range(self.n_components)])
        return self

    def transform(self, X: Matrix) -> Matrix:
        # Center the data using mean from fit
        X_centered = X - Matrix([self.mean_._data[0]] * X.rows)
        # Project data onto principal components
        return X_centered @ self.components_.transpose()
