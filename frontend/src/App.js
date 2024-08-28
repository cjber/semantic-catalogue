import React, { useState } from "react";
import { Box, Typography, CircularProgress, Container } from "@mui/material";
import SearchBar from "./components/SearchBar";
import ResultsGrid from "./components/ResultsGrid";
import CombinedResults from "./components/CombinedResults";
import axios from "axios";

const App = () => {
  const [results, setResults] = useState({});
  const [threadId, setThreadId] = useState(null); // State for threadId
  const [hasSearched, setHasSearched] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (query) => {
    setLoading(true);
    setHasSearched(true);

    try {
      const response = await axios.post(
        `http://localhost:8000/query?q=${encodeURIComponent(query)}`,
      );
      const { documents, thread_id } = response.data; // Destructure thread_id from the response

      // Preserve original index
      const documentsWithIndex = documents.map((doc, index) => ({
        ...doc,
        originalIndex: index,
      }));

      const groupedResults = documentsWithIndex.reduce((acc, doc) => {
        const { source } = doc.metadata;
        if (!acc[source]) {
          acc[source] = [];
        }
        acc[source].push(doc);
        return acc;
      }, {});

      setResults(groupedResults);
      setThreadId(thread_id); // Set the threadId
    } catch (error) {
      console.error("Error fetching query results:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setResults({});
    setThreadId(null);
    setHasSearched(false);
  };

  const combinedResults = Object.values(results).flat();

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography
          variant="h2"
          align="center"
          gutterBottom
          sx={{ cursor: "pointer" }}
          onClick={handleClear}
        >
          Semantic Catalogue Search
        </Typography>
        <SearchBar onSearch={handleSearch} />
        {loading && (
          <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
            <CircularProgress />
          </Box>
        )}
        {!loading && hasSearched && (
          <>
            <ResultsGrid results={results} threadId={threadId} />
            <CombinedResults results={combinedResults} threadId={threadId} />
          </>
        )}
        {!hasSearched && !loading && (
          <Typography
            variant="h6"
            sx={{ mt: 4, textAlign: "center", color: "text.secondary" }}
          >
            Please perform a search to see results.
          </Typography>
        )}
      </Box>
    </Container>
  );
};

export default App;

