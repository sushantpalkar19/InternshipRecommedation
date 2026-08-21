"""
Centralized data loading and preprocessing module.
"""

import pandas as pd
import os
from typing import Optional
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing import normalize_skills, clean_skill_string


class DataLoader:
    """Centralized data loader for internship recommendations."""
    
    def __init__(self, data_path: str = None):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the internship dataset. If None, uses default processed path.
        """
        if data_path is None:
            data_path = "data/processed/internships_clean.csv"
        
        self.data_path = data_path
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """Load and preprocess the dataset."""
        try:
            self.df = pd.read_csv(self.data_path)
            self._preprocess_data()
            print(f"Loaded {len(self.df)} internships from {self.data_path}")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Dataset not found at {self.data_path}. "
                "Please ensure the clean dataset exists or run generate_clean_dataset.py"
            )
    
    def _preprocess_data(self):
        """Preprocess the loaded data."""
        # Handle missing values
        self.df["Skills"] = self.df["Skills"].fillna("")
        self.df["Description"] = self.df["Description"].fillna("")
        self.df["Location"] = self.df["Location"].fillna("Not Specified")
        self.df["Duration"] = self.df["Duration"].fillna("Not Specified")
        self.df["Stipend"] = self.df["Stipend"].fillna("Not Specified")
        self.df["Mode"] = self.df["Mode"].fillna("Not Specified")
        
        # Normalize skills
        self.df["Skills_Normalized"] = self.df["Skills"].apply(normalize_skills)
        
        # Remove duplicates based on Title, Company, and Skills
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates(subset=["Title", "Company", "Skills"], keep="first")
        duplicates_removed = initial_count - len(self.df)
        
        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate records")
        
        # Reset index
        self.df = self.df.reset_index(drop=True)
    
    def get_data(self) -> pd.DataFrame:
        """
        Get the preprocessed dataframe.
        
        Returns:
            Preprocessed internship dataframe
        """
        return self.df.copy()
    
    def get_internship_by_id(self, internship_id: int) -> Optional[pd.Series]:
        """
        Get a specific internship by ID.
        
        Args:
            internship_id: Internship ID
            
        Returns:
            Internship record or None if not found
        """
        internship = self.df[self.df["Internship_ID"] == internship_id]
        if len(internship) > 0:
            return internship.iloc[0]
        return None
    
    def filter_by_location(self, locations: list) -> pd.DataFrame:
        """
        Filter internships by location(s).
        
        Args:
            locations: List of location names
            
        Returns:
            Filtered dataframe
        """
        if "Remote" in locations:
            # Include both Remote and records with Remote in location
            mask = self.df["Location"].isin(locations) | (self.df["Mode"] == "Remote")
        else:
            mask = self.df["Location"].isin(locations)
        
        return self.df[mask].copy()
    
    def filter_by_mode(self, modes: list) -> pd.DataFrame:
        """
        Filter internships by work mode(s).
        
        Args:
            modes: List of work modes (Remote, Hybrid, In-Office)
            
        Returns:
            Filtered dataframe
        """
        return self.df[self.df["Mode"].isin(modes)].copy()
    
    def filter_by_domain(self, domains: list) -> pd.DataFrame:
        """
        Filter internships by domain(s).
        
        Args:
            domains: List of domain names
            
        Returns:
            Filtered dataframe
        """
        return self.df[self.df["Domain"].isin(domains)].copy()
    
    def filter_by_stipend(self, min_stipend: int = None, max_stipend: int = None) -> pd.DataFrame:
        """
        Filter internships by stipend range.
        
        Args:
            min_stipend: Minimum stipend (optional)
            max_stipend: Maximum stipend (optional)
            
        Returns:
            Filtered dataframe
        """
        df = self.df.copy()
        
        # Extract numeric stipend values
        def extract_stipend(stipend_str):
            if pd.isna(stipend_str) or stipend_str == "Not Specified" or stipend_str == "Unpaid":
                return 0
            # Extract numeric value from string like "₹15,000/month"
            import re
            match = re.search(r'[\d,]+', str(stipend_str))
            if match:
                return int(match.group().replace(',', ''))
            return 0
        
        df["Stipend_Numeric"] = df["Stipend"].apply(extract_stipend)
        
        if min_stipend is not None:
            df = df[df["Stipend_Numeric"] >= min_stipend]
        
        if max_stipend is not None:
            df = df[df["Stipend_Numeric"] <= max_stipend]
        
        return df.drop(columns=["Stipend_Numeric"])
    
    def filter_by_duration(self, durations: list) -> pd.DataFrame:
        """
        Filter internships by duration(s).
        
        Args:
            durations: List of duration strings (e.g., ["3 Months", "6 Months"])
            
        Returns:
            Filtered dataframe
        """
        return self.df[self.df["Duration"].isin(durations)].copy()
    
    def filter_by_status(self, status: str = "Open") -> pd.DataFrame:
        """
        Filter internships by status.
        
        Args:
            status: Status to filter by (default: "Open")
            
        Returns:
            Filtered dataframe
        """
        return self.df[self.df["Status"] == status].copy()
    
    def get_unique_locations(self) -> list:
        """Get list of unique locations."""
        return sorted(self.df["Location"].unique().tolist())
    
    def get_unique_modes(self) -> list:
        """Get list of unique work modes."""
        return sorted(self.df["Mode"].unique().tolist())
    
    def get_unique_domains(self) -> list:
        """Get list of unique domains."""
        return sorted(self.df["Domain"].unique().tolist())
    
    def get_unique_durations(self) -> list:
        """Get list of unique durations."""
        return sorted(self.df["Duration"].unique().tolist())
    
    def get_statistics(self) -> dict:
        """
        Get dataset statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            "total_internships": len(self.df),
            "unique_companies": self.df["Company"].nunique(),
            "unique_locations": self.df["Location"].nunique(),
            "unique_domains": self.df["Domain"].nunique(),
            "open_internships": len(self.df[self.df["Status"] == "Open"]),
            "remote_internships": len(self.df[self.df["Mode"] == "Remote"]),
            "domain_distribution": self.df["Domain"].value_counts().to_dict(),
            "location_distribution": self.df["Location"].value_counts().to_dict(),
            "mode_distribution": self.df["Mode"].value_counts().to_dict()
        }


# Global data loader instance
_data_loader = None


def get_data_loader(data_path: str = None) -> DataLoader:
    """
    Get or create the global data loader instance.
    
    Args:
        data_path: Optional path to the dataset
        
    Returns:
        DataLoader instance
    """
    global _data_loader
    
    if _data_loader is None:
        _data_loader = DataLoader(data_path)
    
    return _data_loader


def reload_data(data_path: str = None):
    """
    Reload the data with a new path.
    
    Args:
        data_path: Path to the dataset
    """
    global _data_loader
    _data_loader = DataLoader(data_path)
