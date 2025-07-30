import React, { useState } from 'react';

function MovieRecommender() {
    const [input, setInput] = useState('');
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchRecommendations = async () => {
        const titles = input.split(',').map(t => t.trim()).filter(t => t);
        if (titles.length === 0) {
            setError('Please enter at least one movie title.');
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const response = await fetch('http://localhost:5000/inputOne', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ list: titles }),
            });

            if (!response.ok) throw new Error('Failed to fetch');

            const data = await response.json();
            setRecommendations(data.recommendations || []);
        } catch (err) {
            setError('Error fetching recommendations.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '600px', margin: 'auto', fontFamily: 'Arial, sans-serif' }}>
            <h2>Movie Recommender</h2>
            <textarea
                rows="4"
                style={{ width: '100%' }}
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder="Enter movie titles, separated by commas"
            ></textarea>
            <button onClick={fetchRecommendations} style={{ marginTop: '10px' }}>
                Get Recommendations
            </button>
            {loading && <p>Loading...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {recommendations.length > 0 && (
                <div>
                    <h3>Recommended Movies:</h3>
                    <ul>
                        {recommendations.map((movie, index) => (
                            <li key={index}>{movie}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default MovieRecommender;
