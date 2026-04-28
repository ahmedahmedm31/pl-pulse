"""Match outcome prediction model."""
import os
import pickle
from typing import Dict, Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from app.core.logger import logger
from app.config import settings


class MatchPredictor:
    """Match outcome predictor using Random Forest."""

    def __init__(self, model_path: str | None = None):
        """Initialize predictor.
        
        Args:
            model_path: Path to saved model file.
        """
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
        )
        self.model_path = model_path or os.path.join(
            settings.MODEL_PATH, "match_predictor.pkl"
        )
        self.is_trained = False

    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
        test_size: float = 0.2,
    ) -> Dict[str, float]:
        """Train the model.
        
        Args:
            X: Feature matrix.
            y: Target labels (0=away win, 1=draw, 2=home win).
            test_size: Test set size.
            
        Returns:
            Training metrics.
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        logger.info(f"Training model on {len(X_train)} samples...")
        self.model.fit(X_train, y_train)
        
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        logger.info(f"Train accuracy: {train_score:.3f}")
        logger.info(f"Test accuracy: {test_score:.3f}")
        
        self.is_trained = True
        
        return {
            "train_accuracy": train_score,
            "test_accuracy": test_score,
            "n_samples": len(X),
        }

    def predict(self, features: Dict[str, float]) -> Tuple[float, float, float]:
        """Predict match outcome probabilities.
        
        Args:
            features: Match features dictionary.
            
        Returns:
            Tuple of (home_win_prob, draw_prob, away_win_prob).
        """
        if not self.is_trained:
            # Return default probabilities if model not trained
            return (0.4, 0.3, 0.3)
        
        # Convert features to array
        feature_values = [
            features.get("home_form", 1.5),
            features.get("away_form", 1.5),
            features.get("home_position", 10),
            features.get("away_position", 10),
            features.get("position_diff", 0),
            features.get("home_goals_avg", 1.0),
            features.get("away_goals_avg", 1.0),
            features.get("home_conceded_avg", 1.0),
            features.get("away_conceded_avg", 1.0),
            features.get("home_advantage", 1.0),
        ]
        
        X = np.array([feature_values])
        probabilities = self.model.predict_proba(X)[0]
        
        # probabilities order: [away_win, draw, home_win]
        if len(probabilities) == 3:
            away_win_prob = probabilities[0]
            draw_prob = probabilities[1]
            home_win_prob = probabilities[2]
        else:
            # Fallback if model doesn't have all classes
            home_win_prob = 0.4
            draw_prob = 0.3
            away_win_prob = 0.3
        
        return (home_win_prob, draw_prob, away_win_prob)

    def save(self) -> None:
        """Save model to disk."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved to {self.model_path}")

    def load(self) -> bool:
        """Load model from disk.
        
        Returns:
            True if loaded successfully, False otherwise.
        """
        if os.path.exists(self.model_path):
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
            self.is_trained = True
            logger.info(f"Model loaded from {self.model_path}")
            return True
        return False
