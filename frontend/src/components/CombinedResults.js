import React, { useState } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  IconButton,
  Link,
  Divider,
  Button,
  CircularProgress,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import LinkIcon from "@mui/icons-material/Link"; // For document URL link
import HelpOutlineIcon from "@mui/icons-material/HelpOutline"; // For explain feature
import CloseIcon from "@mui/icons-material/Close"; // For collapsing explanation
import axios from "axios";

const CombinedResults = ({ results = [], threadId }) => {
  const [expandedDocs, setExpandedDocs] = useState({});
  const [visibleCount, setVisibleCount] = useState(5); // Number of results to show initially
  const [explanations, setExplanations] = useState({});
  const [loadingExplanation, setLoadingExplanation] = useState({});
  const [showExplanation, setShowExplanation] = useState({});

  // Toggle expand state for a specific document
  const handleToggleExpand = (index) => {
    setExpandedDocs((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const handleLoadMore = () => {
    setVisibleCount((prevCount) => prevCount + 5); // Show 10 more results
  };

  // Fetch explanation for a document
  const handleFetchExplanation = async (originalIndex) => {
    if (!threadId) {
      return;
    }

    // Set loading state immediately
    setLoadingExplanation((prev) => ({
      ...prev,
      [originalIndex]: true,
    }));

    // Check if the explanation is already available
    if (explanations[`${threadId}-${originalIndex}`]) {
      setLoadingExplanation((prev) => ({
        ...prev,
        [originalIndex]: false,
      }));
      return;
    }

    try {
      const response = await axios.get(
        `http://localhost:8000/explain/${threadId}?docid=${originalIndex}`,
      );
      setExplanations((prev) => ({
        ...prev,
        [`${threadId}-${originalIndex}`]: response.data,
      }));
    } catch (error) {
      console.error("Error fetching explanation:", error);
    } finally {
      setLoadingExplanation((prev) => ({
        ...prev,
        [originalIndex]: false,
      }));
    }
  };

  // Toggle explanation visibility
  const handleToggleExplanation = (originalIndex) => {
    setShowExplanation((prev) => ({
      ...prev,
      [originalIndex]: !prev[originalIndex],
    }));

    // Fetch explanation if not already available
    if (!explanations[`${threadId}-${originalIndex}`]) {
      handleFetchExplanation(originalIndex);
    }
  };

  // Format date for display
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  if (!Array.isArray(results)) {
    console.warn("Results prop is not an array:", results);
    return <Typography variant="h6">No results to display.</Typography>;
  }

  // Slice results to only show the number of visible results
  const displayedResults = results.slice(0, visibleCount);

  return (
    <Box sx={{ mt: 4, p: 2 }}>
      {results.length === 0 ? (
        <Typography variant="h6" sx={{ textAlign: "center" }}>
          No results found.
        </Typography>
      ) : (
        <Card
          sx={{
            borderRadius: 2,
            boxShadow: 3,
            overflow: "hidden",
            width: "100%",
            backgroundColor: "background.default",
          }}
        >
          <CardContent
            sx={{
              display: "flex",
              flexDirection: "column",
              p: 3,
            }}
          >
            {displayedResults.map((doc, index) => (
              <Box key={index} sx={{ mb: 3 }}>
                <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                  <Link
                    href={doc.metadata.url}
                    target="_blank"
                    rel="noopener"
                    sx={{
                      textDecoration: "none",
                      color: "text.primary",
                      flex: 1,
                      "&:hover": {
                        textDecoration: "underline",
                      },
                    }}
                  >
                    <Typography
                      variant="h6"
                      sx={{
                        fontSize: "1.125rem",
                        fontWeight: "bold",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                      }}
                    >
                      {index + 1 + ". " + doc.metadata.title || "Untitled"}
                    </Typography>
                  </Link>
                  <IconButton
                    href={doc.metadata.url}
                    target="_blank"
                    rel="noopener"
                    sx={{
                      ml: 1,
                      color: "primary.main",
                      transition: "color 0.3s",
                      "&:hover": {
                        color: "primary.dark",
                      },
                    }}
                  >
                    <LinkIcon />
                  </IconButton>
                  <IconButton
                    onClick={() => handleToggleExpand(index)}
                    sx={{
                      ml: 2,
                      color: expandedDocs[index]
                        ? "text.primary"
                        : "primary.main",
                    }}
                  >
                    <ExpandMoreIcon
                      sx={{
                        color: "secondary.light",
                        transform: expandedDocs[index]
                          ? "rotate(180deg)"
                          : "rotate(0deg)",
                        transition: "transform 0.3s",
                      }}
                    />
                  </IconButton>
                </Box>

                {/* Date Created */}
                <Typography
                  variant="caption"
                  sx={{
                    color: "text.secondary",
                    mb: 1,
                    fontStyle: "italic",
                  }}
                >
                  {doc.metadata.date_created
                    ? `Created on: ${formatDate(doc.metadata.date_created)}`
                    : "Date not available"}
                </Typography>

                <Typography
                  variant="body2"
                  sx={{
                    fontSize: "0.875rem",
                    color: expandedDocs[index]
                      ? "text.secondary"
                      : "text.disabled", // Change color based on expansion
                    overflow: "hidden",
                    textOverflow: "none",
                    WebkitBoxOrient: "vertical",
                    WebkitLineClamp: expandedDocs[index] ? "none" : 3, // Limit lines when not expanded
                    backgroundColor: "background.default",
                    // display: "-webkit-box",
                    p: 2,
                    borderRadius: 1,
                    lineHeight: "1.5",
                    maxHeight: expandedDocs[index] ? "100em" : "5em", // Control max height for transition
                    transition: "color 0.5s ease, max-height 0.5s ease", // Add transition for color and max-height
                  }}
  dangerouslySetInnerHTML={{
    __html: doc.page_content?.startsWith("Dataset Title:")
      ? doc.page_content.slice(doc.metadata.title.length + 15, 5000).replace(/\n/g, '<p></p>')
      : (doc.page_content || "No preview available.").replace(/\n/g, '<p></p>')
  }}
                >
                </Typography>

                {/* Explain Feature */}
                <Box sx={{ mt: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={
                      showExplanation[doc.originalIndex] ? (
                        <CloseIcon />
                      ) : (
                        <HelpOutlineIcon />
                      )
                    }
                    onClick={() => handleToggleExplanation(doc.originalIndex)}
                    sx={{
                      fontWeight: "bold",
                      borderRadius: 1,
                      textTransform: "none",
                      mb: 1,
                      transition: "background-color 0.3s",
                      "&:hover": {
                        backgroundColor: "info.dark",
                      },
                    }}
                  >
                    {showExplanation[doc.originalIndex]
                      ? "Collapse Explanation"
                      : "Ask AI"}
                  </Button>

                  {showExplanation[doc.originalIndex] && (
                    <Box
                      sx={{
                        mt: 2,
                        p: 2,
                        borderRadius: 2,
                        backgroundColor: "info.light",
                        color: "info.contrastText",
                        border: "1px solid",
                        borderColor: "info.dark",
                        maxHeight: "12em",
                        overflowY: "auto",
                        textAlign: "justify",
                        scrollbarWidth: "none",
                        msOverflowStyle: "none",
                        "&::-webkit-scrollbar": {
                          display: "none",
                        },
                      }}
                    >
                      <Typography
                        variant="subtitle2"
                        sx={{ mb: 1, fontWeight: "bold" }}
                      >
                        AI Explanation
                      </Typography>
                      {loadingExplanation[doc.originalIndex] ? (
                        <Box
                          sx={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                          }}
                        >
                          <CircularProgress size={20} color="inherit" />
                        </Box>
                      ) : (
                        <Typography
                          variant="body2"
                          sx={{ fontSize: "0.875rem", lineHeight: "1.6" }}
                        >
                          {explanations[`${threadId}-${doc.originalIndex}`]
                            ?.generation || "No explanation available."}
                        </Typography>
                      )}
                    </Box>
                  )}
                </Box>
                <Divider sx={{ my: 2 }} />
              </Box>
            ))}
            {visibleCount < results.length && (
              <Button
                onClick={handleLoadMore}
                variant="contained"
                color="secondary"
                sx={{ mt: 2, alignSelf: "center" }}
              >
                Load More
              </Button>
            )}
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default CombinedResults;
