import React, { useState } from 'react';
import { TextField, Button, Box } from '@mui/material';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSearchClick = () => {
    onSearch(query);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSearchClick();
    }
  };

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
      <TextField
        variant="outlined"
        label="Search"
        fullWidth
        sx={{ maxWidth: '800px' }}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown} // Add this line to handle Enter key press
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleSearchClick}
        sx={{ ml: 2 }}
      >
        Search
      </Button>
    </Box>
  );
};

export default SearchBar;
