import React, { useState, useEffect } from 'react';

function AutocompleteInput({ suggestions, onSelect, query, setQuery }) {
    const [filtered, setFiltered] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);

    const handleChange = (e) => {
        const value = e.target.value;
        setQuery(value);
        const matches = suggestions
            .filter(title => title.toLowerCase().includes(value.toLowerCase()))
            .slice(0, 5); // limit suggestions
        setFiltered(matches);
        setShowSuggestions(true);
    };

    const handleSelect = (title) => {
        console.log('ok');
        setQuery(title);
        setShowSuggestions(false);
        onSelect(title);
    };

    return (
        <div style={{ position: 'relative' }}>
            <input
                type="text"
                value={query}
                onChange={handleChange}
                onBlur={() => setTimeout(() => setShowSuggestions(false), 300)} // allow click
                onFocus={() => setShowSuggestions(true)}
                placeholder="Scrie un titlu de film..."
                style={{ width: '100%', padding: '8px' }}
            />
            {showSuggestions && filtered.length > 0 && (
                <ul
                    style={{
                        position: 'absolute',
                        background: 'white',
                        border: '1px solid #ccc',
                        width: '100%',
                        listStyle: 'none',
                        padding: 0,
                        marginTop: '2px',
                        zIndex: 5,
                        maxHeight: '200px',
                        overflowY: 'auto'
                    }}
                >
                    {filtered.map((title, index) => (
                        <li
                            key={index}
                            onClick={() => handleSelect(title)}
                            style={{ padding: '6px', cursor: 'pointer' }}
                        >
                            {title}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default AutocompleteInput;
