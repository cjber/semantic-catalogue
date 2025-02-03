import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  CircularProgress,
  Paper,
  Tooltip,
} from "@mui/material";
import axios from "axios";

// Create a cache object to store explanations
const explanationCache = {};

function ExplanationBox({ documentId, threadId }) {
  const [explanation, setExplanation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchExplanation = async () => {
      setLoading(true);
      setError(null);
      try {
        // Check the cache before making a request
        if (explanationCache[`${documentId}-${threadId}`]) {
          setExplanation(explanationCache[`${documentId}-${threadId}`]);
          setLoading(false);
          return;
        }

        const response = await axios.get(
          `http://localhost:8000/explain/${threadId}?docid=${documentId}`,
        );
        setExplanation(response.data);
        // Store the fetched explanation in the cache
        explanationCache[`${documentId}-${threadId}`] = response.data;
      } catch (error) {
        console.error("Error fetching explanation:", error);
        setError("Failed to fetch explanation");
      } finally {
        setLoading(false);
      }
    };

    fetchExplanation();
  }, [documentId, threadId]);

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", py: 2 }}>
        <CircularProgress size={20} color="primary" />
      </Box>
    );
  }

  if (error) {
    return (
      <Typography variant="body2" color="error" sx={{ py: 1 }}>
        {error}
      </Typography>
    );
  }

  const renderExplanationWithLinks = (text, chunks) => {
    const parts = text.split(/(\[\d+\])/);
    return parts.map((part, index) => {
      const match = part.match(/\[(\d+)\]/);
      if (match) {
        const chunkIndex = parseInt(match[1]);
        return (
          <Tooltip
            key={index + 1}
            title={chunks[chunkIndex]?.page_content || "No content available"}
            arrow
            placement="top"
          >
            <Typography
              component="span"
              sx={{
                fontSize: "0.75em",
                color: "text.secondary",
                cursor: "pointer",
                "&:hover": {
                  textDecoration: "underline",
                  color: "primary.main",
                },
              }}
            >
              {`[${chunkIndex + 1}]`}
            </Typography>
          </Tooltip>
        );
      }
      return <span key={index + 1}>{part}</span>;
    });
  };

  return (
    <Paper
      elevation={0}
      sx={{ p: 2, bgcolor: "primary.main", borderRadius: 1 }}
    >
      <Typography
        variant="body2"
        sx={{ color: "secondary.contrastText", fontSize: "0.75em" }}
      >
        {explanation?.generation
          ? renderExplanationWithLinks(
              explanation.generation,
              explanation.chunks,
            )
          : "No explanation available."}
      </Typography>
    </Paper>
  );
}

export default ExplanationBox;
