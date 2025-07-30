import React, {useEffect, useState} from 'react';
import AutocompleteInput from "./Autocmoplete";

function MovieRecommender() {
    const [input, setInput] = useState('');
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [method, setMethod] = useState('http://localhost:5000/genres')

    const [titles, setTitles] = useState([]);

    const [title, setTitle] = useState('');
    const [titlesList, setTitlesList] = useState([]);

    const [query, setQuery] = useState('');

    const styles = {
        container: {
            maxWidth: '800px',
            margin: '0 auto',
            padding: '20px',
            fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            backgroundColor: '#f5f5f5',
            borderRadius: '10px',
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
        },
        header: {
            textAlign: 'center',
            color: '#333',
            marginBottom: '30px',
        },
        section: {
            backgroundColor: 'white',
            padding: '20px',
            borderRadius: '8px',
            marginBottom: '20px',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
        },
        sectionHeader: {
            color: '#444',
            marginTop: '0',
            marginBottom: '15px',
            borderBottom: '1px solid #eee',
            paddingBottom: '10px',
        },
        inputGroup: {
            display: 'flex',
            gap: '10px',
            marginBottom: '15px',
        },
        autocomplete: {
            flex: '1',
            padding: '10px',
            borderRadius: '4px',
            border: '1px solid #ddd',
            fontSize: '16px',
        },
        addButton: {
            padding: '8px 15px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '16px',
            transition: 'background-color 0.3s',
            marginLeft: '10px'
        },
        addButtonDisabled: {
            backgroundColor: '#cccccc',
            cursor: 'non-allowed',
        },
        selectedMovies: {
            marginTop: '20px',
        },
        selectedHeader: {
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
        },
        clearButton: {
            padding: '5px 10px',
            backgroundColor: '#f44336',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '14px',
        },
        movieList: {
            listStyle: 'none',
            padding: '0',
            margin: '10px 0 0 0',
        },
        movieItem: {
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '10px',
            backgroundColor: '#f9f9f9',
            marginBottom: '5px',
            borderRadius: '4px',
        },
        removeButton: {
            backgroundColor: 'transparent',
            border: 'none',
            color: '#f44336',
            cursor: 'pointer',
            fontSize: '16px',
            padding: '0 5px',
        },
        select: {
            width: '100%',
            padding: '10px',
            borderRadius: '4px',
            border: '1px solid #ddd',
            fontSize: '16px',
            backgroundColor: 'white',
        },
        recommendButton: {
            width: '100%',
            padding: '12px',
            backgroundColor: '#2196f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '16px',
            fontWeight: 'bold',
            transition: 'background-color 0.3s',
        },
        recommendButtonDisabled: {
            backgroundColor: '#cccccc',
            cursor: 'not-allowed',
        },
        error: {
            color: '#f44336',
            marginTop: '10px',
            padding: '10px',
            backgroundColor: '#ffebee',
            borderRadius: '4px',
        },
        recommendations: {
            marginTop: '20px',
        },
        recommendationList: {
            paddingLeft: '20px',
        },
        recommendationItem: {
            padding: '8px 0',
            fontSize: '16px',
        },
    };

    useEffect(() => {
        fetch('/movie.csv').then(res => res.text()).then(text => {
            const rows = text.split('\n').slice(1);
            const titlesOnly = rows.map(r => {
                const parts = r.split('"');
                return parts[1] ? parts[1].trim() : null;
            }).filter(Boolean);
            setTitles(titlesOnly.filter(Boolean));
        })
    })

    const handleAddTitle = () => {
        console.log(title)
        const trimmed = title.trim();
        if (trimmed && !titlesList.includes(trimmed)) {
            setTitlesList([...titlesList, trimmed]);
            setTitle('');
            setQuery('');
        }
    }

    const handelClearTitles = () => {
        setTitlesList([]);
    }

    const fetchRecommendations = async () => {
        if (titlesList.length === 0) {
            setError('Întroduceți cel puțin un titlu.');
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(method, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ titles: titlesList }),
            });

            if (!response.ok) throw new Error('Failed to fetch');

            const data = await response.json();
            console.log(data)
            setRecommendations(data || []);
        } catch (err) {
            setError('Error fetching recommendations.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={styles.container}>
            <h1 style={styles.header}>Movie Recommender</h1>

            <div style={styles.section}>
                <h3 style={styles.sectionHeader}>Listă de filme selectate</h3>
                <div style={styles.inputGroup}>
                    <AutocompleteInput
                        suggestions={titles}
                        onSelect={(title) => setTitle(title)}
                        query={query}
                        setQuery={setQuery}
                    />

                    <button onClick={handleAddTitle} style={styles.addButton}>
                        Adaugă titlu
                    </button>
                </div>

                {titlesList.length > 0 && (
                    <div style={styles.selectedMovies}>
                        <div style={styles.selectedHeader}>
                            <h4>Listă de filme selectate</h4>
                            <button onClick={handelClearTitles} style={styles.clearButton}>
                                Șterge
                            </button>
                        </div>
                        <ul style={styles.movieList}>
                            {titlesList.map((t, index) => (
                                <li key={index} style={styles.movieItem}>
                                    {t}
                                    <button onClick={() => setTitlesList(titlesList.filter(item => item !== t))} style={styles.removeButton}>
                                        X
                                    </button>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>

            <div style={styles.section}>
                <h3 style={styles.sectionHeader}>Metoda de recomandare</h3>
                <select value={method} onChange={(e) => setMethod(e.target.value)} style={styles.select}>
                    <option value='http://localhost:5000/knn'>KNN</option>
                    <option value='http://localhost:5000/colab'>Collaborative</option>
                    <option value='http://localhost:5000/genres'>Content-based</option>
                </select>
            </div>

            <div style={styles.section}>
                <button onClick={fetchRecommendations} style={styles.recommendButton} disabled={titlesList.length === 0 || loading}>
                    {loading ? 'Loading...' : 'Recomandări'}
                </button>

                {error && <div style={styles.error}>{error}</div>}

                {recommendations.length > 0 && (
                    <div style={styles.recommendations}>
                        <h3 style={styles.sectionHeader}>Recomandări</h3>
                        <ol style={styles.recommendationList}>
                            {recommendations.map((t, index) => (
                                <li key={index} style={styles.recommendationItem}>
                                    {t}
                                </li>
                            ))}
                        </ol>
                    </div>
                )}
            </div>

        </div>
    );
}

export default MovieRecommender;
