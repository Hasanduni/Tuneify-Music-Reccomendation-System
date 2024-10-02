# Content-Based Music Recommendation System

### Overview

This Content-Based Music Recommendation System recommends songs by analyzing both textual (lyrics and artist) and numerical (popularity and sentiment) features. The system leverages these combined features to deliver highly relevant song suggestions that align with the user's musical tastes.

### Features

#### Textual Features

Lyrics-Based Recommendations: Recommends songs with similar lyrical content by analyzing the text of the lyrics using natural language processing techniques.

Artist Matching: Suggests songs by similar or related artists based on artist information.

#### Numerical Features

Popularity-Based Filtering: Considers song popularity to recommend tracks that are widely liked or align with the user's preference for popular/unpopular music.

Sentiment Analysis: Recommends songs based on the overall sentiment of the lyrics (e.g., happy, sad, or upbeat) using sentiment scores.

#### Feature Combination

Textual Features Combined: Lyrics and artist information are analyzed together to match songs based on content similarity.

Numerical Features Combined: Popularity and sentiment are treated as numerical features and processed together to rank songs based on numerical similarity.

## How It Works

Data Collection: The system uses a dataset containing songs with both textual (lyrics, artist) and numerical (popularity, sentiment) features.

#### Feature Extraction:

Textual Features: Lyrics and artist information are vectorized and compared for similarity.
Numerical Features: Popularity and sentiment are normalized and processed for ranking.
Content Similarity Calculation:

Textual: Cosine similarity (or a similar metric) is used to compare lyrics and artist text features.
Numerical: Euclidean distance (or a similar metric) is used to compare popularity and sentiment scores.
Recommendation Generation: Songs are recommended based on combined similarity from both textual and numerical features. The system balances these two groups of features to provide well-rounded recommendations.
